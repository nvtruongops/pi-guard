"""Add public Gandalf train candidates and original-ID evidence to a new version."""
import csv
import hashlib
import importlib.util
import json
import platform
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = ROOT / "workspaces/truongnv/pi_guard_pipeline/training_bases"
PROJECT = BASE / "datasets/project_training"
V9 = PROJECT / "versions/pi_guard_v9_english_source_heldout_20261013"
V10 = PROJECT / "versions/pi_guard_v10_english_readiness_20261013"
OUT = PROJECT / "versions/pi_guard_v11_english_gandalf_20261013"
VERSION = "11.0.0-candidate-english-gandalf"
SOURCES = HERE / "source_snapshots_r02/MANIFEST.json"
AGGREGATE = PROJECT / "history/pi_guard_v8_source_gate_20261010/corpus/candidates/rubyglask_core_components"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def binding(prompt, context):
    return hashlib.sha256(json.dumps([prompt, context], ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def main():
    if OUT.exists():
        raise RuntimeError("Never overwrite a dataset version")
    before = {f"{parent.name}/{p.relative_to(parent).as_posix()}": sha(p)
              for parent in (V9, V10) for p in parent.rglob("*") if p.is_file()}
    old_manifest = read(V10 / "DATASET_MANIFEST.json")
    for relative, ref in old_manifest["files"].items():
        assert sha(V10 / relative) == ref["sha256"]
    spec = importlib.util.spec_from_file_location("v9_ingest_helpers", V9 / "tools/prepare_v9_public_english_queue.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    source_manifest = read(SOURCES)
    source_records = {r["source_id"]: r for r in source_manifest["sources"]}
    gandalf = source_records["gandalf"]
    payload = HERE / gandalf["payload"]["path"]
    assert sha(payload) == gandalf["payload"]["sha256"]
    assert gandalf["upstream_split"] == "train" and gandalf["gated"] is False
    assert gandalf["license_recorded"] == "mit"
    import pyarrow.parquet as pq
    native = pq.read_table(payload).to_pylist()
    assert len(native) == 777 and all(set(r) == {"text", "similarity"} for r in native)
    sys.path.insert(0, str(helper.VENDOR))
    import py3langid
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    assert sha(model_path) == helper.MODEL_SHA
    identifier = LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)
    index = jsonl(V10 / "provenance/english_candidate_index.jsonl")
    text_by_id = {}
    for relative in ("annotation/round01_source_blind_pilot.csv", "annotation/round02_public_english_candidate_queue.csv"):
        with (V9 / relative).open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                assert not any(row.get(field) for field in ("curator_label", "final_label", "curator_code"))
                assert row["blind_item_id"] not in text_by_id
                text_by_id[row["blind_item_id"]] = (row["prompt_text"], row["context_text"])
    assert set(text_by_id) == {r["blind_item_id"] for r in index}
    for row in index:
        prompt, context = text_by_id[row["blind_item_id"]]
        assert binding(prompt, context) == row["text_context_binding_sha256"]
    # Recover the original-ID field omitted from the V10 overlay. A current source
    # revision is supplemental documentation only; it is not the aggregate's revision.
    aggregate_provenance_path = AGGREGATE / "provenance/source_metadata.jsonl"
    aggregate_manifest = read(AGGREGATE / "manifest.json")
    assert sha(aggregate_provenance_path) == aggregate_manifest["provenance_file"]["sha256"]
    aggregate_by_id = {r["candidate_id"]: r for r in jsonl(aggregate_provenance_path)}
    components = Counter()
    for row in index:
        row["parent_duplicate_group_id"] = row["duplicate_group_id"]
        if row["pool_id"] == "rubyglask_core_components":
            original = aggregate_by_id[row["candidate_id"]]
            sid = original["source_id"]
            assert sid == row["upstream_source_id"]
            row["aggregate_source_original_id_recorded"] = original["source_original_id"]
            row["component_current_metadata_revision"] = source_records[sid].get("revision")
            row["component_current_metadata_is_original_ingest_revision"] = False
            row["original_component_revision"] = None
            components[sid] += 1
    new, excluded = [], []
    for offset, original in enumerate(native):
        prompt = original["text"]
        record_sha = helper.digest(json.dumps(original, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())
        candidate_id = "gandalf_" + helper.digest(f"{gandalf['repository_id']}@{gandalf['revision']}#train#{offset}#{record_sha}".encode())[:24]
        blind = "v11cand_" + helper.digest(candidate_id.encode())[:24]
        if not prompt.strip():
            excluded.append({"candidate_id": candidate_id, "source_offset": offset, "reason": "empty_text"})
            continue
        language, confidence = identifier.classify(prompt.strip())
        if language != "en" or float(confidence) < 0.95:
            excluded.append({"candidate_id": candidate_id, "source_offset": offset, "reason": "not_english_or_confidence_below_0.95", "predicted_language": language, "confidence": float(confidence)})
            continue
        matches = [name for name, regex in (("email_address", helper.EMAIL_RE), ("credential_assignment", helper.CREDENTIAL_RE)) if regex.search(prompt)]
        if matches:
            excluded.append({"candidate_id": candidate_id, "source_offset": offset, "reason": "privacy_pattern_match", "patterns": matches})
            continue
        row = {"blind_item_id": blind, "candidate_id": candidate_id, "pool_id": "lakera_gandalf_train",
               "source_family_id": "lakera_gandalf_game", "source_repository_id": gandalf["repository_id"],
               "upstream_repository_id": gandalf["repository_id"], "upstream_source_id": "gandalf_ignore_instructions",
               "source_revision": gandalf["revision"], "source_record_id": f"train:{offset}:{record_sha}",
               "upstream_split_recorded": "train", "upstream_split_scope": "publisher_source", "original_component_split": "train",
               "upstream_file_recorded": gandalf["upstream_file"], "source_row_sha256_recorded": record_sha,
               "source_license": "MIT", "source_license_ref": next(d["url"] for d in gandalf["documents"] if d["path"].endswith("README.md")),
               "rights_status_recorded": "publisher_declared_MIT_private_candidate_intake_only",
               "lineage_status_recorded": "pinned_publisher_train_file_offset_and_source_record_hash",
               "source_similarity_score_provenance_only": original["similarity"],
               "dedup_normalized_input_sha256": helper.digest(helper.normalize(prompt + "\n").encode()),
               "text_context_binding_sha256": binding(prompt, ""), "collection_lineage_id": None,
               "collection_lineage_limitation": "Publisher does not provide participant or per-attempt game context identifiers",
               "predicted_language": language, "language_confidence": float(confidence),
               "privacy_pattern_screen": "clear_for_email_and_credential_patterns", "privacy_manual_review_required": True,
               "input_context_status": "prompt_only_no_per_record_system_task_context_supplied",
               "candidate_only": True, "project_label": None, "curator_label": None,
               "parent_duplicate_group_id": None}
        new.append(row)
        text_by_id[blind] = (prompt, "")
    all_rows = index + new
    grouping = [{"blind_item_id": r["blind_item_id"], "prompt_text": text_by_id[r["blind_item_id"]][0],
                 "context_text": text_by_id[r["blind_item_id"]][1]} for r in all_rows]
    print(json.dumps({"phase": "deduplicate_parent_and_new_candidates", "parent_rows": len(index), "new_rows": len(new)}), flush=True)
    raw_stats = helper.group_candidates(grouping)
    union = helper.Groups(len(all_rows))
    first = {}
    for pos, (row, computed) in enumerate(zip(all_rows, grouping)):
        for kind, group in (("parent", row["parent_duplicate_group_id"]), ("recomputed", computed["duplicate_group_id"])):
            if group is not None:
                key = (kind, group)
                if key in first:
                    union.join(pos, first[key])
                else:
                    first[key] = pos
    members = defaultdict(list)
    for pos in range(len(all_rows)):
        members[union.find(pos)].append(pos)
    cross = []
    for positions in members.values():
        group = "v11dup_" + helper.digest("\n".join(sorted(all_rows[p]["blind_item_id"] for p in positions)).encode())[:24]
        families = sorted({all_rows[p]["source_family_id"] for p in positions})
        for pos in positions:
            all_rows[pos]["duplicate_group_id"] = group
        if len(families) > 1:
            cross.append({"duplicate_group_id": group, "families": families,
                          "blind_item_ids": [all_rows[p]["blind_item_id"] for p in positions], "rows": len(positions)})
    sheet = []
    for row in new:
        prompt, context = text_by_id[row["blind_item_id"]]
        entry = {field: "" for field in helper.FIELDS}
        entry.update(blind_item_id=row["blind_item_id"], prompt_text=prompt, context_text=context,
                     rubric_version="PI-Guard-V8-single-curator-2026-10-11")
        sheet.append(entry)
    after = {f"{parent.name}/{p.relative_to(parent).as_posix()}": sha(p)
             for parent in (V9, V10) for p in parent.rglob("*") if p.is_file()}
    assert before == after, "An immutable parent changed"
    assert len(index) == 56498 and len(new) + len(excluded) == len(native)
    OUT.mkdir()
    for sub in ("annotation", "provenance", "reports", "snapshots"):
        (OUT / sub).mkdir()
    (OUT / "snapshots/gandalf_train.parquet").write_bytes(payload.read_bytes())
    assert sha(OUT / "snapshots/gandalf_train.parquet") == gandalf["payload"]["sha256"]
    for name, rows in (("provenance/english_candidate_index.jsonl", all_rows), ("provenance/curator_key_pilot.jsonl", new), ("provenance/exclusion_ledger.jsonl", excluded)):
        (OUT / name).write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8")
    with (OUT / "annotation/source_blind_pilot.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=helper.FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(sheet, key=lambda r: r["blind_item_id"]))
    write(OUT / "provenance/PARENT_INTEGRITY.json", {"parent_files_sha256_before_after_equal": before,
                                                   "aggregate_source_metadata_sha256": sha(aggregate_provenance_path)})
    write(OUT / "provenance/SOURCE_ACQUISITION.json", gandalf)
    write(OUT / "reports/INGEST_AND_LINEAGE.json", {
        "parent_rows": len(index), "downloaded_train_rows": len(native), "new_english_pattern_clear_rows": len(new),
        "excluded_counts": dict(Counter(r["reason"] for r in excluded)), "candidate_rows": len(all_rows),
        "candidate_family_counts": dict(Counter(r["source_family_id"] for r in all_rows)),
        "aggregate_original_id_restored_counts": dict(components), "original_component_split_unknown_rows": 4476,
        "current_metadata_is_original_ingest_proof": False, "raw_recomputed_duplicate_stats": raw_stats,
        "historical_duplicate_groups_preserved_as_constraints": True,
        "final_duplicate_groups": sum(len(v) > 1 for v in members.values()),
        "final_rows_in_nonsingleton_groups": sum(len(v) for v in members.values() if len(v) > 1),
        "cross_family_groups": sorted(cross, key=lambda r: r["duplicate_group_id"]),
        "cross_family_groups_with_new_source": sum("lakera_gandalf_game" in r["families"] for r in cross),
        "privacy_full_review_completed": False, "labels_created": 0, "trainable": False,
    })
    write(OUT / "STATUS.json", {"dataset_version": VERSION, "candidate_rows": len(all_rows), "new_source_candidate_rows": len(new),
                              "canonical_rows": 0, "trainable": False, "frozen_split": False, "l2_run": False, "test_opened": False, "l3_run": False})
    (OUT / "README.md").write_text(
        "# V11 English Gandalf candidate\n\n## Scope Boundary Declaration\n\n"
        "Private candidate successor of V10, adding only the pinned public Gandalf train split after the existing English and privacy-pattern filters. Parent text stays in pinned V9 files; the new-source annotation CSV contains unchanged source text. No canonical labels, partitions or model runs exist.\n\n"
        "The new-source packet is source-conditioned and is not a representative or independently blinded validation set. Source identifiers and similarity scores are omitted from the annotation sheet. Missing per-record system/task context must be recorded by the curator, never invented. Save any reviewed copy outside this immutable package.\n\n"
        "Publisher MIT and PII-filtering declarations support candidate staging only; submitter rights, residual privacy and source independence remain review gates. Source labels/similarity are not PI-Guard labels.\n\n"
        "V11 retains existing duplicate constraints and recomputes exact/near groups across old and new inputs. Original aggregate component IDs are restored, but current source revisions do not prove original aggregate ingestion revisions or splits.\n",
        encoding="utf-8")
    files = {p.relative_to(OUT).as_posix(): {"sha256": sha(p), "bytes": p.stat().st_size} for p in OUT.rglob("*") if p.is_file()}
    write(OUT / "DATASET_MANIFEST.json", {
        "package_id": OUT.name, "dataset_version": VERSION, "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "parent_package_id": V10.name, "parent_manifest_sha256": sha(V10 / "DATASET_MANIFEST.json"),
        "candidate_rows": len(all_rows), "new_source_candidate_rows": len(new), "language": "en", "trainable": False,
        "canonical_row_counts": {"train": 0, "validation": 0, "test": 0}, "files": files,
        "language_filter": helper.CONFIG["language_filter"], "privacy_screen": helper.CONFIG["privacy_screen"],
        "source_snapshot_manifest_sha256": sha(SOURCES), "source_payload_sha256": sha(payload),
        "script_sha256": sha(Path(__file__)), "helper_sha256": sha(V9 / "tools/prepare_v9_public_english_queue.py"),
        "seed": 42, "split_sha256": None, "baseline": helper.CONFIG["baseline"],
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "pyarrow": __import__("pyarrow").__version__},
        "changelog": ["Pinned public Gandalf train added as provisional unlabeled candidates", "Original component record IDs restored; historical component revision/split unresolved", "Duplicate grouping recomputed jointly, preserving historical groups"],
        "gates_pending": ["human curator", "rights/lineage/privacy review", "independent source families and per-class 2/1/1 coverage", "duplicate resolution", "frozen split", "owner numeric L2 gates"],
        "upstream_evaluation_payloads_opened": False, "historical_locked_evaluation_opened": False,
        "l2_fit": False, "l3_run": False,
    })
    print(json.dumps({"package": str(OUT), "manifest_sha256": sha(OUT / "DATASET_MANIFEST.json"),
                      "parent_rows": len(index), "new_rows": len(new), "excluded": dict(Counter(r["reason"] for r in excluded)),
                      "total_candidate_rows": len(all_rows), "cross_family_groups": len(cross),
                      "cross_family_groups_with_new_source": sum("lakera_gandalf_game" in r["families"] for r in cross),
                      "canonical_rows": 0, "trainable": False}))


if __name__ == "__main__":
    main()
