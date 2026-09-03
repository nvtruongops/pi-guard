"""
Demo Script: Mo phong truc quan toan hoc Disentangled Attention & Luong hoa INT8
Chay script: python workspaces/truongnv/docs/model_study/02_deberta_v3_semantic_classifier/run_demo.py
"""

import sys
import io
import time
import numpy as np

# Dam bao in tieng Viet UTF-8 tren Windows console khong loi font
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / e_x.sum(axis=-1, keepdims=True)

def demo_disentangled_attention():
    print("=" * 70)
    print(" [*] PHAN 1: MO PHONG TOAN HOC DISENTANGLED ATTENTION (DEBERTA-V3)")
    print("=" * 70)

    seq_len = 6   # Do dai cau (6 tokens)
    d = 64        # Chieu vector embedding (d = 64)
    tokens = ["Translate", "this", "text", "ignore", "rules", "password"]
    print(f"Cau mau: {tokens}")
    print(f"Do dai chuoi (seq_len): {seq_len}, Chieu embedding (d): {d}")

    np.random.seed(42)
    # Vector noi dung H (Content) va Vector khoang cach tuong doi P (Relative Position)
    H = np.random.randn(seq_len, d)
    P = np.random.randn(seq_len, seq_len, d)  # P[i, j] la khoang cach giua i va j

    # Ma tran trong so chieu Query va Key
    W_q = np.random.randn(d, d) * 0.1
    W_k = np.random.randn(d, d) * 0.1
    W_q_r = np.random.randn(d, d) * 0.1
    W_k_r = np.random.randn(d, d) * 0.1

    # 1. Content-to-Content: H * W_q * W_k^T * H^T
    Q_c = np.dot(H, W_q)
    K_c = np.dot(H, W_k)
    A_cc = np.dot(Q_c, K_c.T)  # (seq_len, seq_len)

    # 2. Content-to-Position: H * W_q * W_k_r^T * P^T
    A_cp = np.zeros((seq_len, seq_len))
    for i in range(seq_len):
        for j in range(seq_len):
            k_r = np.dot(P[i, j], W_k_r)
            A_cp[i, j] = np.dot(Q_c[i], k_r)

    # 3. Position-to-Content: P * W_q_r * W_k^T * H^T
    A_pc = np.zeros((seq_len, seq_len))
    for i in range(seq_len):
        for j in range(seq_len):
            q_r = np.dot(P[j, i], W_q_r)
            A_pc[i, j] = np.dot(q_r, K_c[j])

    # 4. Cong gop va chia cho can bac 2 cua 3d
    scale_factor = 1.0 / np.sqrt(3 * d)
    attention_scores = (A_cc + A_cp + A_pc) * scale_factor
    attention_weights = softmax(attention_scores)

    print("\nMa tran Attention Score (sau khi cong 3 thanh phan & scale 1/sqrt(3d)):")
    print(f" -> Kich thuoc ma tran: {attention_weights.shape}")
    print(f" -> Tong xac suat tren moi dong (Softmax check): {np.sum(attention_weights, axis=-1)}")
    print(f" -> Chú ý từ token 'ignore' (idx=3) toi 'rules' (idx=4): {attention_weights[3, 4]:.4f}")
    print(" [OK] Mo phong Disentangled Attention thanh cong!")

def demo_int8_quantization():
    print("\n" + "=" * 70)
    print(" [*] PHAN 2: MO PHONG TOAN HOC LUONG HOA SO NGUYEN (DYNAMIC INT8)")
    print("=" * 70)

    # Gia su co 1 trieu tham so dang so thuc FP32
    weights_fp32 = np.random.randn(1000, 1000).astype(np.float32)
    original_size_mb = weights_fp32.nbytes / (1024 * 1024)

    # Tinh Scale va Zero-point cho INT8 [-128, 127]
    x_min = weights_fp32.min()
    x_max = weights_fp32.max()
    scale = (x_max - x_min) / 255.0
    zero_point = np.round(-x_min / scale) - 128

    # Anh xa sang so nguyen INT8
    weights_int8 = np.clip(np.round(weights_fp32 / scale) + zero_point, -128, 127).astype(np.int8)
    quantized_size_mb = weights_int8.nbytes / (1024 * 1024)

    # Tinh toan do sai lech khi giai nen nguoc ve FP32
    weights_dequantized = (weights_int8.astype(np.float32) - zero_point) * scale
    mse_loss = np.mean((weights_fp32 - weights_dequantized) ** 2)

    print(f"Dung luong ban dau (FP32 32-bit): {original_size_mb:.2f} MB")
    print(f"Dung luong sau khi luong hoa (INT8 8-bit): {quantized_size_mb:.2f} MB")
    print(f"Ti le tiet kiem bo nho: {(1 - quantized_size_mb / original_size_mb) * 100:.1f}%")
    print(f"Sai so trung binh (Mean Squared Error): {mse_loss:.6f} (Cuc ky nho!)")
    print("=" * 70)

if __name__ == "__main__":
    demo_disentangled_attention()
    demo_int8_quantization()
