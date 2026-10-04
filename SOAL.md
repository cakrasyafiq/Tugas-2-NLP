> STUDY HARD.  
> DO GOOD  
> AND THE  
> GOOD LIFE  
> WILL FOLLOW.

---

# [T2] [PBA] Tugas 2 - Pemrosesan Bahasa Alami

## A. ATURAN PENGERJAAN

### Pengerjaan
* Dikerjakan berkelompok maksimal 4–5 orang (1 orang tidak dianggap berkelompok). Apabila jumlah mahasiswa ganjil, terpaksa ada (1–2) kelompok yang berjumlah 5 anggota. Jadi mayoritas 4 anggota, bukan mayoritas 5 anggota.
* Batas waktu dan pengumpulan melalui **BRONE**.
* Nama anggota dituliskan di bagian atas kode program dalam bentuk komentar:
  ```java
  /*
   * NIM_1 NAMA_1: peran_mahasiswa_1
   * NIM_2 NAMA_2: peran_mahasiswa_2
   * dst.
   */
  ```
* **Dilarang menjiplak/menyontek** dengan alasan, cara, sesedikit apapun. Kode program akan dicek dengan program pengecekan plagiarisme. Pengubahan variabel, letak kode, dll. tidak akan berpengaruh dan dianggap plagiarisme. Plagiarisme (bahkan hanya satu baris saja) tidak akan ditolerir dan dapat mendapatkan nilai E.
* Baca dan pahami soal dengan sebaik-baiknya supaya tidak ada poin nilai yang terlewatkan. Apabila ada yang tidak dimengerti segera ditanyakan ke dosen.

### Pengumpulan (Cek lagi Bagian E)
* Batas waktu pengumpulan di BRONE, perhatikan jam server.
* *Soft copy* melalui BRONE, lampirkan **SEMUA FAIL** (`.DOCX`/`PDF`, `JAVA`, dll.) terkompres dalam format **ZIP/RAR** dengan format penamaan:
  ```text
  [TX][PBA-PRODI-KELAS] Nama Mahasiswa.ZIP
  ```
  * `TX`: Kode tugas (ada di baris pertama dokumen, misal: `T1` untuk Tugas 1, ..., `TP` untuk Tugas/Proyek Akhir).
  * `PBA`: Kode mata kuliah.
  * `PRODI`: Diisi inisial prodi: `TIF` (Teknik Informatika), `TKOM` (Teknik Komputer), `SI` (Sistem Informasi).
  * `KELAS`: Diisi kode kelas (misal: `A`, `B`, `C`, dst.).
  * `Nama Mahasiswa`: Tidak perlu menuliskan semua nama anggota, cukup satu nama saja sebagai ketua kelompok/penanggung jawab unggahan.
  * *Contoh:* `[T2] [PBA-TIF-B] Elon Gates.ZIP`

#### Isi di dalam fail `.ZIP`:
1. Fail `.DOCX`/`.PDF` untuk Source Code, Screenshot output, dan penjelasan kode (seluruh jawaban soal jadi satu dokumen). Gunakan templat yang disediakan di BRONE bagian *"Informasi Dosen, Kontrak Kuliah, Nilai Keaktifan, Ketua Kelas, Template"*.
2. Fail `.py` dengan format: `T2_NoSoal_NamaMahasiswa.py` (dengan tanda *underscore*).
3. Fail lainnya yang diperlukan.

---

## B. TUJUAN TUGAS

Pada tugas ini mahasiswa diharapkan mengetahui dan memahami cara untuk melakukan pembuatan fitur POS Tag. POS Tagging otomatis yang dibuat adalah unigram tagger menggunakan Naïve Bayes sebagai dasar perhitungan peluang tag yang diprediksi. Dengan menguasai pemrosesan teks dasar maka nantinya akan mempermudah mahasiswa untuk melakukan pengolahan data berupa teks terutama dan ekstraksi fitur berupa POS Tagging di bidang pengolahan bahasa alami.

---

## C. DESKRIPSI TUGAS

Tugas ini menitikberatkan pada pembuatan POS Tagging otomatis sederhana menggunakan Naïve Bayes. POS Tagging yang dibuat adalah unigram tagger yang dapat digunakan sebagai fitur dalam pengolahan bahasa alami. Data latih yang digunakan dalam unigram tagger adalah data bahasa Indonesia yang dibuat manual oleh mahasiswa. Tugas ini penting karena merupakan dasar dari pengolahan bahasa alami, oleh karena itu tiap mahasiswa diwajibkan mengerjakan tugas dengan sebaik-baik mungkin.

---

## D. SOAL

### POS TAGGING

1. Masing-masing mahasiswa dalam satu kelompok membuat korpus minimal sebanyak 0,5–1 halaman A4 diketik dengan font Times New Roman 12, semua margin 1,5 cm (misalkan artikel diambil dari Wikipedia, berita, dll). Hasil dari masing-masing mahasiswa digabungkan dan simpan dalam berkas `1_raw_corpus.docx`.
   
   *Contoh isi berkas `.DOCX`:*
   > Ani pergi ke pasar. Dia membeli ikan sebanyak empat.

2. Dari korpus yang didapat pada poin 1, lakukan anotasi berupa POS Tagging secara manual yang nantinya akan digunakan sebagai data latih untuk POS Tagging menggunakan Naïve Bayes. Simpan dalam berkas `1_tagged_corpus.txt`.
   
   Tag set yang digunakan adalah **Tag Set II dari UI-POSTAG** (baca `UI-Postag.pdf`) atau **UI POS Tagset** (baca `Tagset.pdf`). Untuk memudahkan pembuatan data latih, mahasiswa dapat menggunakan API dari UI POS Tag (`http://bahasa.cs.ui.ac.id/postag/tagger`) atau dari repository GitHub `https://github.com/andryluthfi/indonesian-postag`.

   *Contoh dari Tagset II (`UI-Postag.pdf`):*
   ```text
   Ani/PRP pergi/VB ke/IN pasar/NN ./. Dia/PRP membeli/VB ikan/NN sebanyak/ADV empat/NUM ./.
   ```

   *Contoh dari UI Tagset (`Tagset.pdf`):*
   ```text
   Ani/PRP pergi/VB ke/IN pasar/NN ./. Dia/PRP membeli/VB ikan/NN sebanyak/RB empat/CD ./.
   ```

3. Buat data uji (dari kalimat sederhana hingga kompleks) sebanyak 5 kalimat beserta *ground truth*-nya (bebas, sebisa mungkin semua kelas kata pernah muncul). Data uji ini diujikan menggunakan unigram tagger (bukan dari NLTK) yang dibuat sendiri menggunakan Naive Bayes (lihat materi pada slide) dalam bahasa Python. Tag set yang digunakan adalah **Tag Set II pada UI POS Tag**. Untuk mendapatkan peluang, dihitung dari data latih yang dibuat dari poin 1.

   *Contoh data uji:*
   ```text
   Caca/?? membeli/?? ikan/?? tuna/?? mahal/?? yang/?? dijual/?? di/?? pasar/?? untuk/?? dibuat/?? menjadi/?? sushi/?? dan/?? sashimi/?? ./. ?/??
   ```

4. Hitung akurasi dari data uji yang dibuat (yang dianotasi oleh kode Python yang dibuat) dibandingkan dengan *ground truth* (yang dianotasi sendiri dengan benar). Akurasi dihitung dengan rumus:

   $$akurasi = \frac{\text{jumlah tag data uji yang benar (hasil sistem)}}{\text{jumlah tag data uji}}$$

5. Buat perhitungan manual peluang *lexical likelihood* dan *tag prior* untuk satu kalimat dari soal nomor 3 dan hitung hasil akurasinya di file `1_manual.docx` / `1_manual.xlsx` sebagai contoh.

---

### NP-CHUNK

1. Dari 5 kalimat pertama pada data latih POS Tagging yang telah dibuat pada soal POS Tagging, lakukan NP-Chunking dengan `RegexParser` pada NLTK.
   * **a.** Buat grammar untuk mendefinisikan frasa nomina (*noun phrase* / NP).
   * **b.** Tampilkan hasil NP yang ditemukan dari grammar yang dibuat dalam bentuk string *parse tree* (bukan visualisasinya) menggunakan `parse`, misalnya:
     ```text
     (S
       (NP ...)
     )
     ```
   * **c.** Tampilkan hasil NP yang ditemukan dari grammar yang dibuat dalam bentuk IOB menggunakan `nltk.chunk.tree2conlltags`.

2. Simpan hasil NP chunking pada soal **b** ke fail `2_hasil_np_tree.txt` dan soal **c** ke fail `2_hasil_np_iob.txt`.

---

## E. PENGUMPULAN

Kompres semua berkas (masukan, termasuk misal hasil *pre-processing* maupun keluaran) berisi:
1. Source code Python (`file.py` atau Jupyter Notebook `.ipynb`)
2. Fail `1_raw_korpus.docx` berisi korpus yang digunakan pada soal POS Tagging nomor 1
3. Fail `1_tagged_corpus.txt` berisi data latih yang digunakan pada soal POS Tagging nomor 2
4. Fail `1_manual.docx` / `1_manual.xlsx` berisi data latih yang sudah dianotasi, hasil pengujian beserta perhitungan manual yang digunakan pada soal POS Tagging nomor 3 (buat dengan rapi untuk memudahkan pembacaan).
5. Fail `2_hasil_np_tree.txt` berisi hasil NP chunk dari soal NP-CHUNK nomor 1.b
6. Fail `2_hasil_np_iob.txt` berisi hasil NP chunk IOB dari soal NP-CHUNK nomor 1.c

---

> *Selamat mengerjakan sebaik-baiknya. Practice makes perfect.*