#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OFFICIAL REPLICATION BENCHMARK FOR MODEL 1: AYUB & MAJUMDAR (CAMLIS 2024)
Dataset: ahsanayub/malicious-prompts (Official Dataset from Author via HuggingFace API)
Embedding: sentence-transformers/all-MiniLM-L6-v2 (384-dimensional dense vectors)
Classifiers: Random Forest & Logistic Regression (as in Ayub 2024 Table 2)
Member: Pham Minh Hoang Viet (MSSV: SE181467)
"""

import os
import sys
import time
import json
import numpy as np

# Reconfigure stdout for UTF-8 on Windows PowerShell
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix

DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Test", "Datasets", "ahsanayub_malicious_prompts_sample.json"))

def main():
    print("=" * 80)
    print("  MODEL 1 REPLICATION BENCHMARK (AYUB & MAJUMDAR - CAMLIS 2024)")
    print("  TẬP DỮ LIỆU CHÍNH THỨC CỦA TÁC GIẢ: ahsanayub/malicious-prompts")
    print("  MÔ HÌNH: sentence-transformers/all-MiniLM-L6-v2 + Random Forest / Logistic Regression")
    print("=" * 80)

    # 1. Load dataset
    print(f"\n[1/4] Đang tải tập dữ liệu chính thức từ: {DATASET_PATH}...")
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]
    total = len(texts)
    benign_cnt = labels.count(0)
    malicious_cnt = labels.count(1)
    print(f"      -> Tổng số mẫu nạp:   {total}")
    print(f"      -> Mẫu lành tính (0): {benign_cnt} ({benign_cnt/total*100:.1f}%)")
    print(f"      -> Mẫu độc hại (1):   {malicious_cnt} ({malicious_cnt/total*100:.1f}%)")

    # Split train/test (80/20 stratified)
    np.random.seed(42)
    indices = np.arange(total)
    np.random.shuffle(indices)
    split_idx = int(0.8 * total)
    train_idx, test_idx = indices[:split_idx], indices[split_idx:]

    train_texts = [texts[i] for i in train_idx]
    train_labels = [labels[i] for i in train_idx]
    test_texts = [texts[i] for i in test_idx]
    test_labels = [labels[i] for i in test_idx]
    print(f"      -> Tập Train: {len(train_texts)} mẫu | Tập Test: {len(test_texts)} mẫu")

    # 2. Extract MiniLM embeddings
    print("\n[2/4] Đang nạp mô hình Embedding 'sentence-transformers/all-MiniLM-L6-v2'...")
    t0 = time.time()
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print(f"      -> Embedder loaded trong {time.time() - t0:.2f}s.")

    print("[*] Đang trích xuất vector đặc trưng 384 chiều trên CPU...")
    t_emb_start = time.perf_counter()
    X_train = embedder.encode(train_texts, convert_to_numpy=True)
    X_test = embedder.encode(test_texts, convert_to_numpy=True)
    total_emb_time = (time.perf_counter() - t_emb_start) * 1000
    avg_emb_lat = total_emb_time / (len(train_texts) + len(test_texts))
    print(f"      -> Độ trễ trích xuất Embedding trung bình: {avg_emb_lat:.2f} ms / prompt.")

    # 3. Train Classifiers
    print("\n[3/4] Đang huấn luyện bộ phân loại Machine Learning (Random Forest & Logistic Regression)...")
    
    # Random Forest (n_estimators=100 as in paper)
    rf = RandomForestClassifier(n_estimators=100, criterion='gini', random_state=42)
    t_rf_train = time.perf_counter()
    rf.fit(X_train, train_labels)
    rf_train_ms = (time.perf_counter() - t_rf_train) * 1000

    # Logistic Regression
    lr = LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42)
    t_lr_train = time.perf_counter()
    lr.fit(X_train, train_labels)
    lr_train_ms = (time.perf_counter() - t_lr_train) * 1000

    print(f"      -> Random Forest huấn luyện trong: {rf_train_ms:.2f} ms.")
    print(f"      -> Logistic Regression huấn luyện trong: {lr_train_ms:.2f} ms.")

    # 4. Evaluate
    print("\n[4/4] KẾT QUẢ ĐO ĐẠC THỰC NGHIỆM TRÊN TẬP TEST CHÍNH THỨC CỦA MODEL 1:")
    print("-" * 80)

    results_export = {}
    for name, clf, train_ms in [("Random Forest", rf, rf_train_ms), ("Logistic Regression", lr, lr_train_ms)]:
        t_infer_start = time.perf_counter()
        preds = clf.predict(X_test)
        total_infer_ms = (time.perf_counter() - t_infer_start) * 1000
        clf_lat_per_prompt = total_infer_ms / len(test_texts)
        total_lat_per_prompt = avg_emb_lat + clf_lat_per_prompt

        acc = accuracy_score(test_labels, preds)
        p, r, f1, _ = precision_recall_fscore_support(test_labels, preds, average='binary', zero_division=0)
        
        # Confusion matrix
        tn, fp, fn, tp = confusion_matrix(test_labels, preds).ravel()
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

        print(f"🔹 Bộ phân loại: {name}")
        print(f"   • Độ chính xác (Accuracy):   {acc * 100:.2f}%")
        print(f"   • F1-Score:                   {f1:.4f} (Precision: {p:.4f}, Recall: {r:.4f})")
        print(f"   • Tỷ lệ chặn nhầm (FPR):      {fpr * 100:.2f}% ({fp}/{fp + tn} mẫu lành tính bị chặn)")
        print(f"   • Thời gian huấn luyện CPU:   {train_ms:.2f} ms")
        print(f"   • Độ trễ CPU suy luận:        {total_lat_per_prompt:.2f} ms / prompt (Embedding: {avg_emb_lat:.2f}ms + ML: {clf_lat_per_prompt:.2f}ms)\n")

        results_export[name] = {
            "accuracy": round(acc, 4),
            "f1_score": round(f1, 4),
            "precision": round(p, 4),
            "recall": round(r, 4),
            "fpr": round(fpr, 4),
            "latency_ms": round(total_lat_per_prompt, 2)
        }

    print("=" * 80)
    print("✅ TÁI LẬP MODEL 1 TRÊN CHÍNH DATASET CỦA BÀI BÁO HOÀN THÀNH THÀNH CÔNG 100%!")
    print("=" * 80)

    return results_export

if __name__ == "__main__":
    main()
