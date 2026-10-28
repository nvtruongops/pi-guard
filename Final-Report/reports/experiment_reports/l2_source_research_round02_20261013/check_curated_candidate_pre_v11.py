"""Check V10 human review intake without fitting, selecting cutoffs, or opening test.

The existing fit_l2_v8.build_model/evaluate remain the baseline implementation.
This intake stage binds annotations to actual source text and never accepts native
labels or assistant proposals as curator evidence. It writes a new audit only.
"""
import argparse
import csv
import hashlib
import json
import platform
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "datasets/project_training/versions/pi_guard_v10_english_readiness_20261013"
LABELS = {"benign", "PI", "JB"}
QUARANTINE = {"hybrid", "uncertain", "insufficient_context"}
RUBRIC = "PI-Guard-V8-single-curator-2026-10-11"
DECISIONS = ("curator_label", "is_injection", "is_safety_bypass", "confidence", "rationale_code",
             "context_sufficient", "annotated_at_utc", "final_label", "label_status", "curator_code")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(prompt, context):
    return hashlib.sha256(json.dumps([prompt, context], ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def boolean(value):
    values = {"true": True, "1": True, "false": False, "0": False}
    return values.get(str(value).strip().lower())


def decision(row):
    values = {key: (row.get(key) or "").strip() for key in DECISIONS}
    if not any(values.values()):
        return "unreviewed", None
    if any(not value for value in values.values()) or row.get("rubric_version") != RUBRIC:
        return "invalid_incomplete_or_wrong_rubric", None
    try:
        timestamp = datetime.fromisoformat(values["annotated_at_utc"].replace("Z", "+00:00"))
        if timestamp.utcoffset() is None or timestamp > datetime.now(timezone.utc):
            return "invalid_annotation_time", None
    except ValueError:
        return "invalid_annotation_time", None
    label = values["curator_label"]
    if label != values["final_label"] or label not in LABELS | QUARANTINE:
        return "invalid_label", None
    injection, bypass, context = [boolean(values[key]) for key in ("is_injection", "is_safety_bypass", "context_sufficient")]
    if None in (injection, bypass, context):
        return "invalid_rubric_flags", None
    if label in QUARANTINE or not context:
        return "quarantine_curator_decision", label
    expected = {"benign": (False, False), "PI": (True, False), "JB": (False, True)}
    if (injection, bypass) != expected[label] or values["label_status"] != "single_curator_reviewed":
        return "invalid_rubric_flags_or_status", None
    return "complete_single_curator_annotation", label


def inspect(package, annotations=None, attestation=None):
    manifest = load_json(package / "DATASET_MANIFEST.json")
    if manifest.get("dataset_version") != "10.0.0-candidate-english-lineage" or manifest.get("trainable") is not False:
        raise ValueError("Expected the immutable V10 candidate package")
    for relative, ref in manifest["files"].items():
        path = package / relative
        if path.is_symlink() or not path.resolve().is_relative_to(package.resolve()) or sha(path) != ref["sha256"]:
            raise ValueError("Candidate artifact integrity failure")
    annotation_path = annotations or package / "annotation/source_blind_pilot.csv"
    with annotation_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fieldnames = reader.fieldnames
        rows = list(reader)
    expected_fields = ["blind_item_id", "prompt_text", "context_text", "curator_label", "is_injection",
                       "is_safety_bypass", "confidence", "rationale_code", "context_sufficient", "rubric_version",
                       "annotated_at_utc", "final_label", "label_status", "curator_code", "curator_notes"]
    if fieldnames != expected_fields:
        raise ValueError("Unexpected annotation fields: source/model labels cannot enter this intake")
    key_path = package / "provenance/curator_key_pilot.jsonl"
    keys = [json.loads(line) for line in key_path.read_text(encoding="utf-8").splitlines() if line]
    by_id = {row["blind_item_id"]: row for row in keys}
    ids = [row.get("blind_item_id") for row in rows]
    if len(ids) != len(set(ids)) or set(ids) != set(by_id):
        raise ValueError("Missing, extra or duplicate annotation IDs")
    counts, per_family, reviewed = Counter(), defaultdict(Counter), []
    for row in rows:
        key = by_id[row["blind_item_id"]]
        if binding(row["prompt_text"], row["context_text"]) != key["text_context_binding_sha256"]:
            raise ValueError("Annotation text/context differs from pinned source record")
        status, label = decision(row)
        counts[status] += 1
        per_family[key["source_family_id"]][status] += 1
        if status == "complete_single_curator_annotation":
            reviewed.append({"blind_item_id": row["blind_item_id"], "source_family_id": key["source_family_id"],
                             "duplicate_group_id": key["duplicate_group_id"], "label": label,
                             "curator_code": row["curator_code"]})
    groups = defaultdict(set)
    for row in reviewed:
        groups[row["duplicate_group_id"]].add(row["label"])
    conflicts = sorted(group for group, labels in groups.items() if len(labels) > 1)
    eligible = [r for r in reviewed if r["duplicate_group_id"] not in conflicts]
    human_attested = False
    if attestation:
        receipt = load_json(attestation)
        human_attested = (
            receipt.get("annotation_file_sha256") == sha(annotation_path)
            and receipt.get("annotation_actor") == "human"
            and receipt.get("rubric_version") == RUBRIC
            and bool(receipt.get("curator_code"))
            and all(r["curator_code"] == receipt["curator_code"] for r in reviewed)
            and bool(reviewed)
        )
    blockers = ["SOURCE_REVIEW_NOT_APPROVED", "SOURCE_INDEPENDENCE_NOT_VERIFIED",
                "PER_CLASS_TRAIN_VAL_TEST_2_1_1_NOT_ESTABLISHED", "FROZEN_SOURCE_DISJOINT_SPLIT_MISSING",
                "L2_NUMERIC_ACCEPTANCE_GATE_UNSPECIFIED"]
    if not reviewed:
        blockers.insert(0, "HUMAN_CURATOR_DECISIONS_MISSING")
    if not human_attested:
        blockers.insert(0, "HUMAN_ANNOTATION_ATTESTATION_MISSING_OR_INVALID")
    if any(key.startswith("invalid") for key in counts):
        blockers.insert(0, "ANNOTATION_VALIDATION_ERRORS")
    if conflicts:
        blockers.insert(0, "DUPLICATE_GROUP_LABEL_CONFLICT")
    return {
        "status": "BLOCKED", "health_check_status": "NOT_READY", "pipeline_stage": "curator_annotation_intake",
        "dataset_version": manifest["dataset_version"], "dataset_manifest_sha256": sha(package / "DATASET_MANIFEST.json"),
        "annotation_file_sha256": sha(annotation_path), "key_sha256": sha(key_path),
        "review_counts": dict(counts), "per_family_review_counts": dict(per_family),
        "complete_annotation_class_counts": dict(Counter(r["label"] for r in reviewed)),
        "human_attestation_recorded": human_attested,
        "attestation_limitation": "An owner-supplied human receipt records provenance; field values alone cannot prove authorship",
        "nonconflicting_complete_annotations": len(eligible),
        "canonical_model_rows_emitted": 0, "duplicate_conflicting_group_ids": conflicts,
        "blockers": blockers, "fit_performed": False, "test_opened": False, "l3_run": False,
        "script_sha256": sha(Path(__file__)), "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def self_check(package):
    result = inspect(package)
    assert result["review_counts"] == {"unreviewed": result["review_counts"]["unreviewed"]}
    assert result["canonical_model_rows_emitted"] == 0 and result["fit_performed"] is False
    with (package / "annotation/source_blind_pilot.csv").open(encoding="utf-8", newline="") as stream:
        real_row = next(csv.DictReader(stream))
    # Negative checks modify only metadata in memory; they never create corpus rows or labels on disk.
    assert decision({**real_row, "final_label": "PI"})[0] == "invalid_incomplete_or_wrong_rubric"
    try:
        boolean("approved")
        assert boolean("approved") is None
        inspect(package, package / "provenance/curator_key_pilot.jsonl")
    except (ValueError, csv.Error):
        pass
    else:
        raise AssertionError("Provenance cannot substitute for the blind annotation sheet")
    assert all(not flag for flag in (result["test_opened"], result["l3_run"], result["fit_performed"]))
    return {"self_check": "PASS", "checks": ["real blank pilot stays blocked", "partial decision rejected",
            "nonboolean review flag rejected", "source sidecar cannot substitute for annotation CSV", "no fit/test/L3"],
            "dataset_manifest_sha256": result["dataset_manifest_sha256"], "script_sha256": sha(Path(__file__))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=DEFAULT)
    parser.add_argument("--annotations", type=Path, help="A reviewed copy; do not edit the immutable packet")
    parser.add_argument("--curator-attestation", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="A new run JSON; never overwrite")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.output.exists() or args.output.resolve().is_relative_to(args.package.resolve()):
        raise ValueError("Write a new audit outside the immutable dataset")
    result = self_check(args.package) if args.self_check else inspect(args.package, args.annotations, args.curator_attestation)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
