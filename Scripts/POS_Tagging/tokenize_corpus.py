"""
245150207111084 Achmad Yusuf Hamdani Firmansyah:
Corpus Lead & Data Annotation
"""

import os
import re

# Path file
raw_path = os.path.join(os.path.dirname(__file__), '../../Corpus/Raw/1_raw_corpus.txt')

with open(raw_path, 'r', encoding='utf-8') as f:
    teks = f.read()

# Tokenisasi kata dan tanda baca menggunakan regex:
# Memisahkan kata (termasuk kata ulang dengan tanda hubung)

teks_bersih = re.sub(r'\bRp(\d+)', r'Rp \1', teks)
tokens = re.findall(r'\w+(?:-\w+)*|[^\w\s]', teks_bersih)

print(f"Total token terdeteksi: {len(tokens)}")
print("\n10 token pertama:")
print(tokens[:10])

# Mendefinisikan kamus kata tugas (Tagset II UI-POSTAG)
TAG_DICT = {
    'IN': {'di', 'ke', 'dari', 'pada', 'dalam', 'untuk', 'dengan', 'oleh', 'bagi', 'tentang', 'atas', 'terhadap', 'hingga', 'sampai', 'antar', 'antara', 'demi', 'saat'},
    'CC': {'dan', 'atau', 'tetapi', 'serta', 'melainkan', 'namun', 'sedangkan'},
    'SC': {'yang', 'bahwa', 'karena', 'jika', 'apabila', 'setelah', 'sebelum', 'ketika', 'sejak', 'sehingga', 'supaya', 'agar', 'meskipun', 'walaupun', 'maka'},
    'PRP': {'saya', 'ia', 'dia', 'mereka', 'kami', 'kita', 'anda', 'kamu', 'beliau', 'dirinya'},
    'PR': {'ini', 'itu', 'sini', 'situ', 'sana', 'tersebut'},
    'MD': {'akan', 'dapat', 'bisa', 'harus', 'mampu', 'sudah', 'telah', 'perlu', 'boleh', 'mesti', 'sempat', 'hendak'},
    'NEG': {'tidak', 'bukan', 'belum', 'jangan', 'tak'},
    'DT': {'para', 'sang', 'si', 'seorang', 'setiap', 'masing-masing'},
    'RB': {'sangat', 'hanya', 'justru', 'pula', 'kemudian', 'kembali', 'selalu', 'sering', 'pernah', 'kurang', 'lebih', 'turut', 'terlalu', 'segera', 'secara'},
    'RP': {'pun', 'lah', 'kah'},
    'WH': {'siapa', 'apa', 'mana', 'kapan', 'kenapa', 'mengapa', 'bagaimana', 'berapa'},
    'CD': {'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan', 'sepuluh', 'belas', 'puluh', 'ratus', 'ribu', 'juta', 'miliar', 'triliun', 'banyak', 'sebagian', 'sepertiga'},
    'OD': {'pertama', 'kedua', 'ketiga', 'keempat', 'kelima', 'keenam', 'ketujuh', 'kedelapan', 'kesembilan', 'kesepuluh'},
    'NND': {'orang', 'ton', 'lembar', 'rupiah', 'kali', 'kalinya', 'tahun', 'hari', 'bulan'}
}

PUNCTUATIONS = {'.', ',', '"', "'", '?', '!', '(', ')', ':', ';', '-', '–', '—', '/'}
SYMBOLS = {'%', '+', '@', '$', 'IDR', 'Rp'}

# Menambahkan kamus kata khusus
# Adjektiva (Kata Sifat / JJ)
ADJECTIVES = {
    'resmi', 'baru', 'lama', 'besar', 'panjang', 'penting', 'aktif', 'tinggi',
    'lengkap', 'tajam', 'padat', 'lambat', 'kompleks', 'signifikan', 'responsif',
    'profesional', 'kontroversial', 'merah', 'putih', 'gratis', 'terbuka', 'efektif',
    'mendasar', 'strategis', 'populis'
}

ADJECTIVES.update({'tertinggal', 'terdepan', 'terluar', 'publik', 'total', 'swasta'})

# Kata benda yang berawalan me-, di-, ber-, ter- (agar tidak salah jadi VB)
NOUN_EXCEPTIONS = {
    'menteri', 'dimensi', 'dinamika', 'distribusi', 'berita', 'berkas',
    'tersangka', 'periode', 'moratorium'
}

# Kata depan berawalan me-
PREP_EXCEPTIONS = {'melalui', 'mengenai'}

# Tambahan kata tugas dan Adverbia
TAG_DICT['RB'].update({'juga', 'kembali', 'bahkan', 'hampir', 'langsung'})
TAG_DICT['IN'].update({'sebagai', 'tanpa', 'selama', 'bersama'})
TAG_DICT['CD'].update({'beberapa', 'seluruh', 'semua', 'sepuluh', 'sejumlah'})
TAG_DICT['VB'] = {'adalah', 'merupakan'}

# Daftar Nama penting (tetap NNP meski di awal kalimat)
PROPER_NAMES = {
    'Prabowo', 'Subianto', 'Rocky', 'Gerung', 'Kejaksaan', 'Kementerian',
    'Presiden', 'BGN', 'Purbaya', 'Suahasil', 'Indonesia', 'Jakarta', 'Agung'
}

def tag_token(token, is_start_of_sentence=False):
    lower_t = token.lower()
    
    # 1. Tanda Baca
    if token in PUNCTUATIONS:
        return 'Z'
    
    # 2. Simbol
    if token in SYMBOLS or token == 'Rp':
        return 'SYM'
        
    # 3. Penanganan gabungan Rp + angka (misal Rp335 -> pisah atau tandai)
    if token.startswith('Rp') and len(token) > 2 and token[2:].isdigit():
        return 'CD'
    
    # 4. Angka Kardinal & Ordinal
    if token.isdigit():
        return 'CD'
    if lower_t.startswith('ke-') or lower_t in TAG_DICT['OD']:
        return 'OD'
        
    # 5. Pengecualian Khusus (Preposisi & Kata Benda)
    if lower_t in PREP_EXCEPTIONS:
        return 'IN'
    if lower_t in NOUN_EXCEPTIONS:
        return 'NN'
    if lower_t in ADJECTIVES:
        return 'JJ'
    
    # 6. Kamus Kata Tugas
    for tag, words in TAG_DICT.items():
        if lower_t in words:
            return tag
    
     # 7. Nama Diri (termasuk jika di awal kalimat / nama khusus)
    if token in PROPER_NAMES or token == 'Merdeka':
        return 'NNP'
    # 8. Verba berimbuhan
    if lower_t.startswith(('me', 'ber', 'di', 'ter')) and len(lower_t) > 4:
        return 'VB'
    
    # 9. Proper Noun umum lainnya (huruf kapital)
    if token.isupper() and len(token) > 1:
        return 'NNP'
    if token[0].isupper() and not is_start_of_sentence:
        return 'NNP'
    
    # Default: Nomina
    return 'NN'

# Melakukan tagging pada seluruh token
tagged_tokens = []
is_start = True

for t in tokens:
    tag = tag_token(t, is_start_of_sentence=is_start)
    tagged_tokens.append(f"{t}/{tag}")
    # Jika token adalah titik/tanda seru/tanya, token berikutnya adalah awal kalimat
    is_start = t in {'.', '!', '?'}

# Gabungkan token (baris baru setelah titik/akhir kalimat)
output_text = ""
for t in tagged_tokens:
    output_text += t + " "
    if t.endswith(('./Z', '?/Z', '!/Z')):
        output_text += "\n"

# Path output
output_path = os.path.join(os.path.dirname(__file__), '../../Corpus/Tagged/1_tagged_corpus.txt')

# Simpan file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(output_text.strip() + "\n")

print(f"\nBerhasil membuat korpus teranotasi di: {output_path}")
print("\nSampel 10 kata teranotasi pertama:")
print(" ".join(tagged_tokens[:10]))