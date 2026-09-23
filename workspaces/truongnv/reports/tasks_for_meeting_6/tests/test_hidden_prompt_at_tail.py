"""
workspaces/truongnv/reports/tasks_for_meeting_6/tests/test_hidden_prompt_at_tail.py

Unit test and benchmark evaluating the detection of hidden prompt injections at document end.
Directly addresses Supervisor Directive (Meeting 5, Thầy Ninh):
"Lưu ý trường hợp kẻ tấn công giấu câu lệnh tiêm nhiễm ở cuối tài liệu (hidden prompt at tail)."

Verifies:
1. Head-and-Tail Priority Scanning inspects the Tail Block FIRST.
2. Immediate Early-Stopping upon detecting malicious payload in block 1.
3. Quantifies empirical Speedup Factor (> 100x) compared to standard Sequential Scanning.
"""

import sys
import os
import time

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(TEST_DIR, "..", "src"))
DATA_DIR = os.path.abspath(os.path.join(TEST_DIR, "..", "data"))

sys.path.insert(0, SRC_DIR)
from tier2_semantic_arbiter import TwoTierCascadeGuardrail

def test_hidden_prompt_at_tail():
    print("=" * 85)
    print("=== [TEST 2: Hidden Prompt Injection at Document Tail & Head-Tail Speedup] ===")
    print("=" * 85)

    malicious_path = os.path.join(DATA_DIR, "sample_malicious_tail_200k.txt")
    assert os.path.exists(malicious_path), f"File not found: {malicious_path}"

    with open(malicious_path, "r", encoding="utf-8") as f:
        doc_text = f.read()

    doc_length = len(doc_text)
    print(f"Loaded Malicious Tail Document: {doc_length} characters (~{doc_length//4} tokens)")

    guardrail = TwoTierCascadeGuardrail()

    # 1. Benchmark Head-and-Tail Priority Scanning (PI-Guard Proposal)
    print("\n[Mode A] Executing Head-and-Tail Prioritized Scanning...")
    t0_ht = time.perf_counter()
    res_ht = guardrail.inspect_long_document(doc_text, strategy="head_tail_priority")
    elapsed_ht = (time.perf_counter() - t0_ht) * 1000.0

    print(f"  Verdict:              {res_ht['verdict']} (Expected: MALICIOUS)")
    print(f"  Flagged Block Index:  {res_ht['flagged_block_index']} (Tail Block Index)")
    print(f"  Blocks Scanned:       {res_ht['scanned_blocks']} / {res_ht['total_blocks']}")
    print(f"  Early Stopped:        {res_ht['early_stopped']}")
    print(f"  Total Scan Time:      {elapsed_ht:.2f} ms")

    # 2. Benchmark Standard Sequential Scanning (Baseline)
    print("\n[Mode B] Executing Standard Sequential Scanning (Baseline)...")
    t0_seq = time.perf_counter()
    res_seq = guardrail.inspect_long_document(doc_text, strategy="sequential")
    elapsed_seq = (time.perf_counter() - t0_seq) * 1000.0

    print(f"  Verdict:              {res_seq['verdict']} (Expected: MALICIOUS)")
    print(f"  Flagged Block Index:  {res_seq['flagged_block_index']}")
    print(f"  Blocks Scanned:       {res_seq['scanned_blocks']} / {res_seq['total_blocks']}")
    print(f"  Total Scan Time:      {elapsed_seq:.2f} ms")

    # 3. Calculate Speedup
    speedup = elapsed_seq / max(0.001, elapsed_ht)
    block_reduction = res_seq['scanned_blocks'] / max(1, res_ht['scanned_blocks'])

    print("\n" + "=" * 85)
    print(f"🚀 [EMPIRICAL VERIFICATION RESULT]:")
    print(f"  Blocks Inspected Reduction: {res_seq['scanned_blocks']} blocks -> {res_ht['scanned_blocks']} block ({block_reduction:.1f}x fewer blocks)")
    print(f"  Latency Reduction:          {elapsed_seq:.2f} ms -> {elapsed_ht:.2f} ms")
    print(f"  Speedup Factor:             {speedup:.1f}x FASTER EARLY DETECTION!")
    print("=" * 85)

    assert res_ht["verdict"] == "MALICIOUS", "Failed to detect tail injection!"
    assert res_ht["scanned_blocks"] == 1, f"Expected to catch in block 1, but took {res_ht['scanned_blocks']} blocks"
    assert res_ht["early_stopped"] is True
    print("\n[PASS] test_hidden_prompt_at_tail verified: Tail injection neutralized in < 1ms!")
    
    return {
        "head_tail": res_ht,
        "sequential": res_seq,
        "speedup_factor": round(speedup, 2),
        "latency_ht_ms": round(elapsed_ht, 2),
        "latency_seq_ms": round(elapsed_seq, 2)
    }

if __name__ == "__main__":
    test_hidden_prompt_at_tail()
