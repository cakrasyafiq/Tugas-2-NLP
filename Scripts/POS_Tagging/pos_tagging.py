"""
235150200111040 Achmad Yusuf Hamdani Firmansyah:
Unigram Tagger Script
"""

import os
import re
from collections import defaultdict, Counter


class BayesUnigramTagger:
    def __init__(self):
        self.tag_counts = Counter()
        self.word_tag_counts = defaultdict(Counter)
        self.word_counts = Counter() 
        self.total_tokens = 0
        self.vocab = set()
        self.all_tags = set()
        self.default_tag = "NN"

    def train_from_file(self, file_path: str):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File korpus tidak ditemukan di: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            corpus_text = f.read()

        raw_tokens = corpus_text.split()
        parsed_tokens = []

        for item in raw_tokens:
            parts = item.rsplit("/", 1)
            if len(parts) == 2:
                word, tag = parts[0], parts[1]
                parsed_tokens.append((word, tag))

        self.train_from_tokens(parsed_tokens)

    def train_from_tokens(self, tagged_tokens: list):
        self.total_tokens = len(tagged_tokens)
        self.tag_counts.clear()
        self.word_tag_counts.clear()
        self.word_counts.clear()
        self.vocab.clear()
        self.all_tags.clear()

        for word, tag in tagged_tokens:
            self.tag_counts[tag] += 1
            self.word_tag_counts[word][tag] += 1
            self.word_counts[word] += 1
            self.vocab.add(word)
            self.all_tags.add(tag)

        # Menentukan default tag berdasarkan tag prior tertinggi (frekuensi terbesar)
        if self.tag_counts:
            self.default_tag = self.tag_counts.most_common(1)[0][0]

    def get_tag_prior(self, tag: str) -> float:
        if self.total_tokens == 0:
            return 0.0
        return self.tag_counts[tag] / self.total_tokens

    def get_lexical_likelihood(self, word: str, tag: str) -> float:
        count_t = self.tag_counts[tag]
        if count_t == 0:
            return 0.0
        return self.word_tag_counts[word][tag] / count_t

    def get_joint_probability(self, word: str, tag: str) -> float:
        return self.get_lexical_likelihood(word, tag) * self.get_tag_prior(tag)

    def get_word_marginal(self, word: str) -> float:
        if self.total_tokens == 0:
            return 0.0
        return self.word_counts[word] / self.total_tokens

    def get_posterior(self, word: str, tag: str) -> float:
        p_w = self.get_word_marginal(word)
        if p_w == 0.0:
            return 0.0
        return self.get_joint_probability(word, tag) / p_w

    def predict_tag(self, word: str):
        # 1. Pencocokan exact kata
        if word in self.word_counts:
            best_tag = None
            best_score = -1.0
            for tag in self.all_tags:
                score = self.get_joint_probability(word, tag)
                if score > best_score:
                    best_score = score
                    best_tag = tag
            return best_tag if best_tag is not None else self.default_tag

        # 2. Fallback case-insensitive
        w_lower = word.lower()
        lower_tags = Counter()
        for corpus_w, t_counts in self.word_tag_counts.items():
            if corpus_w.lower() == w_lower:
                for t, cnt in t_counts.items():
                    lower_tags[t] += cnt

        if lower_tags:
            best_tag = None
            best_score = -1.0
            for tag, cnt in lower_tags.items():
                likelihood = cnt / self.tag_counts[tag]
                prior = self.get_tag_prior(tag)
                score = likelihood * prior
                if score > best_score:
                    best_score = score
                    best_tag = tag
            return best_tag if best_tag is not None else self.default_tag

        # 3. Fallback Out-of-Vocabulary (OOV) -> Tag dengan prior terbesar
        return self.default_tag

    def tokenize(self, text: str) -> list:
        cleaned_text = re.sub(r"\bRp(\d+)", r"Rp \1", text)
        tokens = re.findall(r"\w+(?:-\w+)*|[^\w\s]", cleaned_text)
        return tokens

    def tag_sentence(self, sentence_input) -> list:
        if isinstance(sentence_input, str):
            tokens = self.tokenize(sentence_input)
        else:
            tokens = sentence_input

        return [(word, self.predict_tag(word)) for word in tokens]

    @staticmethod
    def load_raw_test_data(file_path: str) -> list:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File data uji mentah tidak ditemukan di: {file_path}")

        raw_sentences = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    raw_sentences.append(stripped)
        return raw_sentences

    @staticmethod
    def load_ground_truth_test_data(file_path: str) -> list:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File ground truth tidak ditemukan di: {file_path}")

        ground_truth_sentences = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                tokens_tags = []
                for token_item in stripped.split():
                    parts = token_item.rsplit("/", 1)
                    if len(parts) == 2:
                        tokens_tags.append((parts[0], parts[1]))
                if tokens_tags:
                    ground_truth_sentences.append(tokens_tags)
        return ground_truth_sentences

    def ingest_and_process_test_data(self, raw_path: str, gt_path: str = None) -> list:
        raw_sentences = self.load_raw_test_data(raw_path)
        gt_sentences = self.load_ground_truth_test_data(gt_path) if gt_path else None

        processed_test_data = []

        for idx, raw_sentence in enumerate(raw_sentences):
            tokens = self.tokenize(raw_sentence)

            if gt_sentences and idx < len(gt_sentences):
                gt_sentence = gt_sentences[idx]
                # Pasangkan token hasil tokenisasi dengan ground truth tag
                sentence_data = []
                for t_idx, word in enumerate(tokens):
                    gt_tag = gt_sentence[t_idx][1] if t_idx < len(gt_sentence) else self.default_tag
                    sentence_data.append((word, gt_tag))
                processed_test_data.append(sentence_data)
            else:
                # Jika tidak ada ground truth, pasangkan dengan placeholder None
                processed_test_data.append([(word, None) for word in tokens])

        return processed_test_data

    def evaluate(self, test_data: list):
        total_tokens = 0
        correct_tokens = 0
        results = []

        for idx, sentence in enumerate(test_data, 1):
            sent_correct = 0
            sent_details = []
            for word, true_tag in sentence:
                pred_tag = self.predict_tag(word)
                is_correct = (pred_tag == true_tag) if true_tag is not None else None
                total_tokens += 1
                if is_correct:
                    correct_tokens += 1
                    sent_correct += 1

                sent_details.append({
                    "word": word,
                    "ground_truth": true_tag,
                    "predicted": pred_tag,
                    "correct": is_correct
                })

            sent_acc = (sent_correct / len(sentence)) * 100.0 if sentence else 0.0
            results.append({
                "sentence_idx": idx,
                "length": len(sentence),
                "correct": sent_correct,
                "accuracy": sent_acc,
                "details": sent_details
            })

        overall_acc = (correct_tokens / total_tokens) * 100.0 if total_tokens > 0 else 0.0
        return {
            "total_tokens": total_tokens,
            "correct_tokens": correct_tokens,
            "overall_accuracy": overall_acc,
            "sentences": results
        }


def main():
    # --------------------------------------------------------------------------
    # 1. INISIALISASI PATH DAN LATIHAN MODEL (DATA LATIH)
    # --------------------------------------------------------------------------
    current_dir = os.path.dirname(os.path.abspath(__file__))
    train_corpus_path = os.path.join(current_dir, "../../Corpus/Tagged/1_tagged_corpus.txt")
    raw_test_path = os.path.join(current_dir, "../../Corpus/Test/test_cases.txt")
    gt_test_path = os.path.join(current_dir, "../../Corpus/Test/test_cases_with_ground_truth.txt")

    print("=" * 80)
    print("PROGRAM POS TAGGING - UNIGRAM TAGGER DENGAN TEOREMA BAYES")
    print("=" * 80)
    print(f"[Tahap 1] Memuat dan melatih model dari korpus: {train_corpus_path}")

    tagger = BayesUnigramTagger()
    tagger.train_from_file(train_corpus_path)

    print("\n--- STATISTIK DATA LATIH ---")
    print(f"Total token (N)            : {tagger.total_tokens}")
    print(f"Jumlah kosakata unik (|V|) : {len(tagger.vocab)}")
    print(f"Jumlah kelas tag unik      : {len(tagger.all_tags)}")
    print(f"Daftar kelas tag unik      : {sorted(tagger.all_tags)}")
    print(f"Tag dengan prior tertinggi : {tagger.default_tag} (P = {tagger.get_tag_prior(tagger.default_tag):.4f})")

    # --------------------------------------------------------------------------
    # 2. TAHAP TEST DATA INGESTION
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("[Tahap 2] TEST DATA INGESTION DARI CORPUS/TEST")
    print("=" * 80)
    print(f"Membaca raw string dari        : {raw_test_path}")
    print(f"Membaca ground truth dari      : {gt_test_path}")

    raw_sentences = tagger.load_raw_test_data(raw_test_path)
    print(f"\nBerhasil membaca {len(raw_sentences)} kalimat uji mentah:")
    for idx, sentence in enumerate(raw_sentences, 1):
        print(f"  {idx}. {sentence}")

    # Melakukan ingestion dan pra-pemrosesan (tokenisasi serta pencocokan ground truth)
    test_data = tagger.ingest_and_process_test_data(raw_test_path, gt_test_path)
    print(f"\nProses tokenisasi selesai. Total kalimat siap dievaluasi: {len(test_data)}")

    # --------------------------------------------------------------------------
    # 3. PREDIKSI POS TAG DAN EVALUASI AKURASI
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("[Tahap 3] HASIL EVALUASI PREDIKSI PADA DATA UJI")
    print("=" * 80)

    eval_result = tagger.evaluate(test_data)

    for res in eval_result["sentences"]:
        idx = res["sentence_idx"]
        print(f"\n>>> Kalimat {idx} (Jumlah token: {res['length']}, Akurasi: {res['accuracy']:.2f}%):")
        raw_words = [item["word"] for item in res["details"]]
        print(f"Teks: \"{' '.join(raw_words)}\"")
        print(f"{'Kata':<15} | {'Ground Truth':<12} | {'Hasil Prediksi':<15} | {'Status':<6}")
        print("-" * 55)
        for item in res["details"]:
            status = "BENAR" if item["correct"] else "SALAH"
            print(f"{item['word']:<15} | {item['ground_truth']:<12} | {item['predicted']:<15} | {status:<6}")

    print("\n" + "=" * 80)
    print("RINGKASAN AKURASI KESELURUHAN DATA UJI")
    print("=" * 80)
    print(f"Total token data uji   : {eval_result['total_tokens']}")
    print(f"Total prediksi benar   : {eval_result['correct_tokens']}")
    print(f"Akurasi Keseluruhan    : {eval_result['overall_accuracy']:.2f}%")
    print(f"Rumus Akurasi          : ({eval_result['correct_tokens']} / {eval_result['total_tokens']}) * 100%")


if __name__ == "__main__":
    main()