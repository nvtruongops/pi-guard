"""Record a data/code-license discrepancy as a sparse immutable candidate overlay."""
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PROJECT = ROOT / "workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training"
PARENT = PROJECT / "versions/pi_guard_v11_english_gandalf_20261013"
OUT = PROJECT / "versions/pi_guard_v12_english_rights_overlay_20261013"
VERSION = "12.0.0-candidate-english-rights-overlay"
CARD = HERE / "source_snapshots_r02/do_not_answer/README.md"
EVIDENCE_URL = "https://huggingface.co/datasets/LibrAI/do-not-answer/blob/74e74f2e4507ef256fe536f78a776f4a1ff67955/README.md"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if OUT.exists():
        raise ValueError("Never overwrite a dataset version")
    parent_manifest = json.loads((PARENT / "DATASET_MANIFEST.json").read_text())
    before = {p.relative_to(PARENT).as_posix(): sha(p) for p in PARENT.rglob("*") if p.is_file()}
    for relative, ref in parent_manifest["files"].items():
        assert before[relative] == ref["sha256"]
    card = CARD.read_text(encoding="utf-8")
    assert "license: apache-2.0" in card
    assert "All datasets in this repository are released under" in card
    assert "Creative Commons Attribution-NonCommercial-ShareAlike 4.0" in card
    assert "All source files in this repository are released under the Apache 2.0 license" in card
    index_path = PARENT / "provenance/english_candidate_index.jsonl"
    rows = [json.loads(line) for line in index_path.read_text(encoding="utf-8").splitlines()]
    affected = [r for r in rows if r["source_family_id"] == "rubyglask_do_not_answer"]
    assert len(affected) == 554 and all(r["upstream_source_id"] == "do_not_answer" for r in affected)
    holds = [{"blind_item_id": r["blind_item_id"], "candidate_id": r["candidate_id"],
              "source_family_id": r["source_family_id"], "parent_duplicate_group_id": r["duplicate_group_id"],
              "disposition": "RIGHTS_QUARANTINE_PENDING_SOURCE_REVIEW",
              "reason": "aggregate_and_card_metadata_Apache_2_0_do_not_resolve_distinct_dataset_CC_BY_NC_SA_4_0_notice",
              "publisher_notice_ref": EVIDENCE_URL, "publisher_card_sha256": sha(CARD),
              "human_rights_review_decision": None, "canonical_label": None} for r in affected]
    OUT.mkdir()
    (OUT / "provenance").mkdir()
    (OUT / "provenance/rights_quarantine.jsonl").write_text(
        "".join(json.dumps(row, separators=(",", ":")) + "\n" for row in holds), encoding="utf-8")
    write(OUT / "provenance/PARENT_INTEGRITY.json", {"parent_files_sha256": before})
    write(OUT / "provenance/RIGHTS_EVIDENCE.json", {
        "publisher_card_url": EVIDENCE_URL, "publisher_card_sha256": sha(CARD),
        "card_metadata_license": "Apache-2.0", "dataset_notice": "CC-BY-NC-SA-4.0", "source_code_notice": "Apache-2.0",
        "interpretation": "A distinct dataset notice conflicts with treating the metadata/code license as sufficient dataset-use evidence",
        "legal_clearance_claim": False, "use_is_illegal_claim": False,
        "release_condition": "A source reviewer records a supported dataset-use basis and obligations in a new candidate version",
        "existing_labels_changed": False,
    })
    write(OUT / "STATUS.json", {"dataset_version": VERSION, "candidate_rows_including_holds": len(rows),
        "explicit_rights_quarantined_rows": len(holds), "candidate_rows_not_in_this_explicit_hold": len(rows) - len(holds),
        "not_in_this_hold_does_not_mean_eligible": True, "canonical_rows": 0, "trainable": False,
        "frozen_split": False, "test_opened": False, "l2_run": False, "l3_run": False})
    (OUT / "README.md").write_text(
        "# V12 English rights overlay\n\n## Scope Boundary Declaration\n\n"
        "This sparse candidate version references the immutable V11 index and applies an explicit rights hold to 554 Do-Not-Answer-derived records. It copies no prompt text and creates no labels or partitions. The parent V11 Gandalf annotation packet remains a separate unreviewed candidate packet.\n\n"
        "Do-Not-Answer's pinned card declares Apache-2.0 in metadata but distinguishes a CC-BY-NC-SA-4.0 dataset notice from Apache-2.0 source-code terms. The aggregate's Apache-2.0 field is not treated as sufficient evidence to resolve this discrepancy. This is a research rights gate, not a legal conclusion that a particular use is prohibited.\n\n"
        "Resolve both the parent index and rights overlay before any future canonicalization. Rows outside this particular hold still need curator, privacy, lineage, independence, coverage and frozen-split gates. The overlay is not directly consumable by the legacy annotation checker or model runner. Save reviewed rights decisions separately and create another version for accepted changes.\n",
        encoding="utf-8")
    assert before == {p.relative_to(PARENT).as_posix(): sha(p) for p in PARENT.rglob("*") if p.is_file()}
    files = {p.relative_to(OUT).as_posix(): {"sha256": sha(p), "bytes": p.stat().st_size} for p in OUT.rglob("*") if p.is_file()}
    write(OUT / "DATASET_MANIFEST.json", {
        "package_id": OUT.name, "dataset_version": VERSION, "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "schema": "candidate_rights_overlay_v1", "parent_package_id": PARENT.name,
        "parent_manifest_sha256": sha(PARENT / "DATASET_MANIFEST.json"),
        "parent_index": {"path_from_project_training": str(index_path.relative_to(PROJECT)).replace("\\", "/"), "sha256": sha(index_path), "rows": len(rows)},
        "overlay": {"path": "provenance/rights_quarantine.jsonl", "sha256": sha(OUT / "provenance/rights_quarantine.jsonl"), "rows": len(holds)},
        "candidate_rows_including_holds": len(rows), "explicit_rights_quarantined_rows": len(holds),
        "candidate_rows_not_in_this_explicit_hold": len(rows) - len(holds),
        "canonical_row_counts": {"train": 0, "validation": 0, "test": 0}, "trainable": False,
        "files": files, "script_sha256": sha(Path(__file__)), "baseline": parent_manifest["baseline"],
        "seed": 42, "split_sha256": None, "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "changelog": ["Added explicit rights quarantine for Do-Not-Answer records based on pinned publisher dataset/code license distinction", "Parent records and all earlier versions remain unchanged"],
        "l2_fit": False, "test_opened": False, "l3_run": False,
    })
    print(json.dumps({"package": str(OUT), "manifest_sha256": sha(OUT / "DATASET_MANIFEST.json"),
                      "rights_quarantined_rows": len(holds), "candidate_rows_including_holds": len(rows),
                      "candidate_rows_not_in_this_hold": len(rows) - len(holds), "trainable": False}))


if __name__ == "__main__":
    main()
