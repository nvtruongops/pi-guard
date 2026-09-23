"""
workspaces/truongnv/reports/tasks_for_meeting_6/tests/test_long_document_200k.py

Unit test and benchmark evaluating the processing of large 200,000-character documents
using PI-Guard Two-Tier Cascade Chunker.
Verifies:
1. No Out-of-Memory (OOM) or stack overflow on Commodity CPU.
2. Full document scanning speed and per-block latency.
3. Correct benign classification without False Positive triggers.
"""

import sys
import os
import time

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(TEST_DIR, "..", "src"))
DATA_DIR = os.path.abspath(os.path.join(TEST_DIR, "..", "data"))

sys.path.insert(0, SRC_DIR)
from tier2_semantic_arbiter import TwoTierCascadeGuardrail

def test_long_document_200k():
    print("=" * 80)
    print("=== [TEST 1: 200,000-Character Long Document Processing & Throughput] ===")
    print("=" * 80)

    benign_path = os.path.join(DATA_DIR, "sample_benign_200k.txt")
    assert os.path.exists(benign_path), f"File not found: {benign_path}"

    with open(benign_path, "r", encoding="utf-8") as f:
        doc_text = f.read()

    doc_length = len(doc_text)
    print(f"Loaded Benign Document: {doc_length} characters (~{doc_length//4} tokens)")

    guardrail = TwoTierCascadeGuardrail()

    # Warmup
    _ = guardrail.inspect_query("Warmup query")

    t0 = time.perf_counter()
    res = guardrail.inspect_long_document(doc_text, strategy="head_tail_priority")
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    print("\n--- Scan Results ---")
    print(f"Verdict:              {res['verdict']} (Expected: BENIGN)")
    print(f"Total Blocks:         {res['total_blocks']}")
    print(f"Scanned Blocks:       {res['scanned_blocks']}")
    print(f"Total Scanning Time:  {elapsed_ms:.2f} ms")
    print(f"Throughput:           {doc_length / (elapsed_ms / 1000.0) / 1000.0:.2f} kChars/second")
    print(f"Average Block Trễ:    {elapsed_ms / max(1, res['scanned_blocks']):.3f} ms/block")

    assert res["verdict"] == "BENIGN", f"Expected BENIGN but got {res['verdict']}"
    assert res["total_blocks"] > 100, f"Expected > 100 blocks but got {res['total_blocks']}"
    print("\n[PASS] test_long_document_200k successfully verified with ZERO memory crash!")
    return res

if __name__ == "__main__":
    test_long_document_200k()
