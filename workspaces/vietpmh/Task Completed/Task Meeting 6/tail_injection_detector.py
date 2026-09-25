#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workspaces/vietpmh/Task Completed/Task Meeting 6/tail_injection_detector.py
-------------------------------------------------------------------------
TASK 4: GIẢI PHÁP CHỐNG PROMPT INJECTION GIẤU Ở CUỐI TÀI LIỆU (TAIL INJECTION)
Tác giả: Phạm Minh Hoàng Việt (MSSV: SE181467)
Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) - Đại học FPT

CĂN CỨ KHOA HỌC:
1. Greshake et al. (ACM AISec 2023 - Indirect Prompt Injection):
   File PDF: Final-Report/References/Greshake_2023_Indirect_Prompt_Injection.pdf
   -> Kẻ tấn công cấy câu lệnh tiêm nhiễm vào phần cuối của tài liệu (Footer, References, End of document)
      nhằm chiếm đoạt chỉ thị khi LLM đọc hiểu toàn bộ văn bản.
2. Wallace et al. / OpenAI (2024 - Instruction Hierarchy):
   File PDF: Final-Report/References/Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf
   -> Hiện tượng Recency Bias: Câu lệnh ở cuối văn bản có sức ảnh hưởng chi phối luồng suy luận của LLM
      mạnh hơn nhiều so với phần đầu.
3. Zhou et al. (2026 - Prompt Overflow):
   File PDF: Final-Report/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf
"""

import os
import sys
import time
import json
from typing import Dict, Any, List, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from block_analyzer_200k import HierarchicalTextAnalyzer, generate_synthetic_200k_document
from two_tier_combination_engine import TwoTierCascadeOrchestrator, load_local_datasets


class TailInjectionDefenseEngine:
    """
    CƠ CHẾ PHÒNG THỦ CHỐNG TẤN CÔNG GIẤU Ở ĐUÔI TÀI LIỆU (TAIL-INJECTION DEFENSE)
    So sánh 2 chiến lược quét:
    1. Sequential Scan: Quét tuần tự từ Block 0 -> Block N-1 (Chậm, tốn tài nguyên).
    2. Tail-and-Head Prioritized Scanning với Early-Stopping:
       Quét ưu tiên Block cuối (N-1) trước, rồi đến Block đầu (0), rồi xen kẽ vào giữa.
       Ngay khi phát hiện mã độc -> Ngắt sớm tức thì (Short-Circuit), tăng tốc độ phát hiện gấp hàng chục lần.
    """
    def __init__(self, block_size_chars: int = 1500, overlap_chars: int = 150):
        self.chunker = HierarchicalTextAnalyzer(block_size_chars=block_size_chars, overlap_chars=overlap_chars)
        self.orchestrator = TwoTierCascadeOrchestrator(theta_low=0.15, theta_high=0.85)

        # Huấn luyện Tầng 1
        notinject, malicious = load_local_datasets()
        train_texts = [x["prompt"] for x in notinject[:50]] + [x["text"] for x in malicious[:100]]
        train_labels = [0] * len(notinject[:50]) + [int(x["label"]) for x in malicious[:100]]
        self.orchestrator.fit_tier1(train_texts, train_labels)

    def scan_sequential_with_early_stop(self, text: str) -> Dict[str, Any]:
        """Chiến lược 1: Quét tuần tự từ Block 0 đến Block N-1."""
        blocks = self.chunker.chunk_document_into_blocks(text)
        total_blocks = len(blocks)

        t0 = time.perf_counter()
        blocks_scanned = 0
        detected_at_block = -1
        is_blocked = False

        for i, blk in enumerate(blocks):
            blocks_scanned += 1
            res = self.orchestrator.inspect(blk["content"])
            if res["decision"] == "BLOCK":
                is_blocked = True
                detected_at_block = i
                break

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "strategy": "Sequential Scan",
            "total_blocks": total_blocks,
            "blocks_scanned": blocks_scanned,
            "blocks_saved": total_blocks - blocks_scanned,
            "detected_at_block": detected_at_block,
            "verdict": "BLOCK" if is_blocked else "ALLOW",
            "elapsed_ms": round(elapsed_ms, 3)
        }

    def scan_tail_prioritized_with_early_stop(self, text: str) -> Dict[str, Any]:
        """
        Chiến lược 2 (Đột phá của PI-Guard): Quét Ưu Tiên Đuôi-Đầu (Tail-First Order).
        Thứ tự quét: [N-1, 0, N-2, 1, N-3, 2, ...]
        Bắt ngay đòn tấn công giấu ở cuối tài liệu tại Block đầu tiên quét.
        """
        blocks = self.chunker.chunk_document_into_blocks(text)
        total_blocks = len(blocks)

        # Xây dựng thứ tự quét ưu tiên Đuôi - Đầu
        priority_indices = []
        left = 0
        right = total_blocks - 1

        while left <= right:
            if right >= left:
                priority_indices.append(right)
                right -= 1
            if left <= right:
                priority_indices.append(left)
                left += 1

        t0 = time.perf_counter()
        blocks_scanned = 0
        detected_at_block = -1
        is_blocked = False

        for idx in priority_indices:
            blocks_scanned += 1
            res = self.orchestrator.inspect(blocks[idx]["content"])
            if res["decision"] == "BLOCK":
                is_blocked = True
                detected_at_block = idx
                break

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "strategy": "Tail-and-Head Prioritized Scan",
            "total_blocks": total_blocks,
            "blocks_scanned": blocks_scanned,
            "blocks_saved": total_blocks - blocks_scanned,
            "detected_at_block": detected_at_block,
            "verdict": "BLOCK" if is_blocked else "ALLOW",
            "elapsed_ms": round(elapsed_ms, 3)
        }


def main():
    print("=" * 80)
    print("  TASK 4: THỰC NGHIỆM ĐO ĐẠC GIẢI PHÁP CHỐNG PROMPT GIẤU Ở CUỐI (TAIL INJECTION)")
    print("  Đối chuẩn: Quét Tuần Tự (Sequential) vs. Quét Ưu Tiên Đuôi-Đầu (Tail-First)")
    print("=" * 80)

    # 1. Sinh văn bản 200,000 ký tự có cấy câu lệnh tiêm nhiễm vào đoạn đuôi
    print("\n[1/3] Đang khởi tạo tài liệu 200,000 ký tự có cấy Tail Injection...")
    malicious_tail_doc = generate_synthetic_200k_document(tail_injection=True)

    # 2. Khởi tạo Engine
    print("[2/3] Khởi tạo TailInjectionDefenseEngine...")
    engine = TailInjectionDefenseEngine()

    # 3. Đo đạc hai chiến lược
    print("\n[3/3] Thực thi đo đạc so sánh hiệu năng:")
    
    print("  [*] Đang chạy Chiến lược 1: Quét tuần tự (Sequential Scan)...")
    res_seq = engine.scan_sequential_with_early_stop(malicious_tail_doc)
    print(f"      -> Phát hiện mã độc tại Block {res_seq['detected_at_block']} (đã duyệt {res_seq['blocks_scanned']}/{res_seq['total_blocks']} blocks)")
    print(f"      -> Thời gian thực thi: {res_seq['elapsed_ms']} ms")

    print("\n  [*] Đang chạy Chiến lược 2: Quét ưu tiên Đuôi-Đầu (Tail-First Scan)...")
    res_tail = engine.scan_tail_prioritized_with_early_stop(malicious_tail_doc)
    print(f"      -> Phát hiện mã độc tại Block {res_tail['detected_at_block']} (chỉ cần duyệt {res_tail['blocks_scanned']}/{res_tail['total_blocks']} blocks)")
    print(f"      -> Thời gian thực thi: {res_tail['elapsed_ms']} ms")

    # Tính toán tốc độ tăng tốc
    speedup = round(res_seq["elapsed_ms"] / res_tail["elapsed_ms"], 2) if res_tail["elapsed_ms"] > 0 else 0.0

    metrics = {
        "author": "Pham Minh Hoang Viet (vietpmh)",
        "task": "Task 4 (Meeting 6): Hidden Prompt at Tail Defense Solution",
        "document_length_chars": len(malicious_tail_doc),
        "total_blocks": res_seq["total_blocks"],
        "sequential_scan": res_seq,
        "tail_prioritized_scan": res_tail,
        "speedup_factor": f"{speedup}x",
        "blocks_saved_pct": round((res_seq["blocks_scanned"] - res_tail["blocks_scanned"]) / res_seq["total_blocks"] * 100.0, 2)
    }

    out_file = os.path.join(CURRENT_DIR, "task4_tail_detection_metrics.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("  KẾT QUẢ ĐỐI CHUẨN THỰC NGHIỆM TASK 4")
    print("=" * 80)
    print(f"• Số blocks cần quét của Quét Tuần Tự:         {res_seq['blocks_scanned']} blocks  (Thời gian: {res_seq['elapsed_ms']} ms)")
    print(f"• Số blocks cần quét của Quét Ưu Tiên Đuôi:    {res_tail['blocks_scanned']} block   (Thời gian: {res_tail['elapsed_ms']} ms)")
    print(f"• Hiệu quả tăng tốc độ phát hiện (Speedup):    TĂNG TỐC GẤP {speedup} LẦN!")
    print(f"• Tiết kiệm tài nguyên CPU:                    Bỏ qua {metrics['blocks_saved_pct']}% số blocks không cần quét")
    print(f"[✓] Đã xuất kết quả số hóa Task 4 ra: {out_file}")


if __name__ == "__main__":
    main()
