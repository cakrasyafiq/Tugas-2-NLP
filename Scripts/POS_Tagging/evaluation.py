"""
245150200111056 Zaidan Alvi Zulfan Pramudya
Testing Suite & Accuracy Evaluator
"""

import os
from pos_tagging import BayesUnigramTagger


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    train_corpus_path = os.path.join(
        current_dir,
        "../../Corpus/Tagged/1_tagged_corpus.txt"
    )

    raw_test_path = os.path.join(
        current_dir,
        "../../Corpus/Test/test_cases.txt"
    )

    gt_test_path = os.path.join(
        current_dir,
        "../../Corpus/Test/test_cases_with_ground_truth.txt"
    )

    print("\n[1] Melatih model dari corpus...")

    tagger = BayesUnigramTagger()
    tagger.train_from_file(train_corpus_path)

    print(f"Total token training : {tagger.total_tokens}")
    print(f"Jumlah vocabulary    : {len(tagger.vocab)}")
    print(f"Jumlah tag           : {len(tagger.all_tags)}")

    print("\n[2] Membaca test cases...")

    raw_sentences = tagger.load_raw_test_data(raw_test_path)
    test_data = tagger.ingest_and_process_test_data(
        raw_test_path,
        gt_test_path
    )

    print(f"Jumlah kalimat test : {len(raw_sentences)}")

    print("\n[3] Melakukan evaluasi...")

    result = tagger.evaluate(test_data)

    for sentence in result["sentences"]:
        print("\n" + "-" * 60)
        print(
            f"Kalimat {sentence['sentence_idx']} | "
            f"Akurasi: {sentence['accuracy']:.2f}%"
        )
        print("-" * 60)

        print(
            f"{'Kata':<20}"
            f"{'Ground Truth':<15}"
            f"{'Prediksi':<15}"
            f"Status"
        )

        for item in sentence["details"]:
            status = "BENAR" if item["correct"] else "SALAH"

            print(
                f"{item['word']:<20}"
                f"{item['ground_truth']:<15}"
                f"{item['predicted']:<15}"
                f"{status}"
            )

    print("\n" + "=" * 60)
    print("HASIL AKHIR EVALUASI")
    print("=" * 60)

    print(f"Total token         : {result['total_tokens']}")
    print(f"Token benar         : {result['correct_tokens']}")
    print(f"Akurasi keseluruhan : {result['overall_accuracy']:.2f}%")

if __name__ == "__main__":
    main()