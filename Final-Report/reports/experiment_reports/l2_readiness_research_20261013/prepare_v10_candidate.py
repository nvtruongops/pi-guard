"""Build a provenance successor and a bounded review packet from real V9 candidates."""
import csv
import hashlib
import importlib.util
import io
import json
import platform
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TRAINING = ROOT / "workspaces/truongnv/pi_guard_pipeline/training_bases"
PROJECT = TRAINING / "datasets/project_training"
V9 = PROJECT / "versions/pi_guard_v9_english_source_heldout_20261013"
OUT = PROJECT / "versions/pi_guard_v10_english_readiness_20261013"
VERSION = "10.0.0-candidate-english-lineage"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def jsonl(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def binding(prompt, context):
    return hashlib.sha256(json.dumps([prompt, context], ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def main():
    if OUT.exists():
        raise RuntimeError("A candidate version cannot be overwritten")
    parent_hashes = {p.relative_to(V9).as_posix(): sha(p) for p in V9.rglob("*") if p.is_file()}
    helper_path = V9 / "tools/prepare_v9_public_english_queue.py"
    spec = importlib.util.spec_from_file_location("v9_candidate_helpers", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    manifest = json.loads((V9 / "DATASET_MANIFEST.json").read_text())
    index_path = V9 / "provenance/english_candidate_index_round02.jsonl"
    assert sha(index_path) == manifest["public_source_ingest"]["provenance_index_sha256"]
    old_index = jsonl(index_path)
    assert len({(r["pool_id"], r["candidate_id"]) for r in old_index}) == len(old_index)
    old_by_id = {(r["pool_id"], r["candidate_id"]): r for r in old_index}
    restored, texts, evidence, source_reviews = [], {}, {}, {}
    for pool in helper.CONFIG["pools"]:
        candidates, source_manifest = helper.load_pool(pool)
        pool_id = pool["pool_id"]
        source_path = helper.SOURCE_ROOT / pool_id / "manifest.json"
        evidence[source_path.relative_to(PROJECT).as_posix()] = sha(source_path)
        refs = [source_manifest["annotation_packet"]]
        if "sources" in source_manifest:
            refs += [s["output_file"] for s in source_manifest["sources"]]
        else:
            refs += [source_manifest["candidate_rows_file"]]
        for ref in refs:
            evidence[(helper.SOURCE_PACKAGE / ref["path"]).relative_to(PROJECT).as_posix()] = ref["sha256"]
        for item in candidates:
            meta = item["meta"]
            key = (pool_id, meta["candidate_id"])
            if key not in old_by_id:
                continue  # The existing language/privacy exclusions remain excluded.
            old = old_by_id[key]
            prompt, context = item["prompt_text"], item["context_text"]
            normalized = helper.digest(helper.normalize(prompt + "\n" + context).encode())
            assert normalized == old["dedup_normalized_input_sha256"], "V9 input binding changed"
            assert old["predicted_language"] == "en" and old["language_confidence"] >= 0.95
            assert not helper.EMAIL_RE.search(prompt + "\n" + context)
            assert not helper.CREDENTIAL_RE.search(prompt + "\n" + context)
            split = meta.get("upstream_split")
            aggregate = pool_id == "rubyglask_core_components"
            source_file = meta.get("source_file")
            if pool_id == "public_human_authored":
                source = next(s for s in source_manifest["sources"] if s["repo_id"] == meta["source_repository_id"])
                source_file = source["upstream_filename"]
                assert split == source["upstream_split"]
            if aggregate:
                source_file = source_manifest["source_snapshot"]["repository_file"]
            row = {
                **old,
                "parent_version": manifest["dataset_version"],
                "parent_blind_item_id": old["blind_item_id"],
                "upstream_split_recorded": split,
                "upstream_split_scope": "aggregate_container_only" if aggregate else "publisher_source",
                "original_component_split": None if aggregate else split,
                "upstream_file_recorded": source_file,
                "source_row_sha256_recorded": meta.get("source_row_sha256"),
                "collection_lineage_id": meta.get("collection_lineage_id"),
                "collection_lineage_scope": "publisher_recorded_group_not_proof_of_independence",
                "text_context_binding_sha256": binding(prompt, context),
                "curator_label": None,
                "candidate_only": True,
            }
            restored.append(row)
            texts[old["blind_item_id"]] = (prompt, context)
            review_key = (pool_id, old["source_family_id"], old["source_revision"])
            source_reviews[review_key] = {
                "pool_id": pool_id, "source_family_id": old["source_family_id"],
                "source_revision": old["source_revision"],
                "rights_evidence_recorded": old["rights_status_recorded"],
                "source_license": old["source_license"],
                "source_license_ref": old["source_license_ref"],
                "original_component_split_unresolved": aggregate,
                "source_level_privacy_review_required": old["privacy_manual_review_required"],
                "rights_lineage_decision": None, "privacy_decision": None,
                "family_independence_decision": None, "reviewer_code": None,
                "reviewed_at_utc": None, "evidence_refs": [],
            }
    restored.sort(key=lambda r: r["blind_item_id"])
    assert len(restored) == len(old_index) == 56498
    groups = defaultdict(list)
    for row in restored:
        groups[row["duplicate_group_id"]].append(row)
    cross = [{"duplicate_group_id": gid,
              "families": sorted({r["source_family_id"] for r in rs}),
              "candidate_ids": [r["blind_item_id"] for r in rs], "rows": len(rs)}
             for gid, rs in sorted(groups.items()) if len({r["source_family_id"] for r in rs}) > 1]
    # Holding a family constant still requires handling these cross-family duplicate edges.
    # Exclude cross-family groups from this pilot; preserve them in the full candidate index.
    prior_pilot = {r["blind_item_id"] for r in restored if r["review_packet"] == "round01_existing"}
    prior_pilot |= {r["blind_item_id"] for r in jsonl(V9 / "provenance/curator_key_round03.jsonl")}
    cross_groups = {r["duplicate_group_id"] for r in cross}
    selected, used_groups = [], set()
    selection_counts = Counter()
    for row in sorted(restored, key=lambda r: helper.digest(("v10-pilot|" + r["blind_item_id"]).encode())):
        family = row["source_family_id"]
        if selection_counts[family] >= 10 or row["blind_item_id"] in prior_pilot:
            continue
        prompt, context = texts[row["blind_item_id"]]
        if row["duplicate_group_id"] in cross_groups or row["duplicate_group_id"] in used_groups:
            continue
        if len(prompt) + len(context) > 8000:
            continue
        selected.append(row)
        selection_counts[family] += 1
        used_groups.add(row["duplicate_group_id"])
    sheet, pilot_key = [], []
    for row in selected:
        prompt, context = texts[row["blind_item_id"]]
        blind = "V10-" + helper.digest(("v10-blind|" + row["blind_item_id"]).encode())[:20]
        entry = {field: "" for field in helper.FIELDS}
        entry.update(blind_item_id=blind, prompt_text=prompt, context_text=context,
                     rubric_version="PI-Guard-V8-single-curator-2026-10-11")
        sheet.append(entry)
        pilot_key.append({**row, "blind_item_id": blind})
    sheet.sort(key=lambda r: r["blind_item_id"])
    pilot_key.sort(key=lambda r: r["blind_item_id"])
    families = []
    for family in sorted(selection_counts):
        rs = [r for r in restored if r["source_family_id"] == family]
        families.append({"source_family_id": family, "candidate_rows": len(rs),
                         "pilot_rows": selection_counts[family],
                         "split_recorded_counts": dict(Counter(r["upstream_split_recorded"] for r in rs)),
                         "original_component_split_unknown_rows": sum(r["original_component_split"] is None for r in rs),
                         "collection_group_recorded_rows": sum(bool(r["collection_lineage_id"]) for r in rs),
                         "canonical_label_support": None, "independence_verified": False})
    after = {p.relative_to(V9).as_posix(): sha(p) for p in V9.rglob("*") if p.is_file()}
    assert parent_hashes == after, "Parent package changed during reconstruction"
    for relative, expected in evidence.items():
        assert sha(PROJECT / relative) == expected, "Source evidence changed"
    OUT.mkdir()
    for sub in ("annotation", "provenance", "reports"):
        (OUT / sub).mkdir()
    for relative, rows in (("provenance/english_candidate_index.jsonl", restored),
                           ("provenance/curator_key_pilot.jsonl", pilot_key)):
        (OUT / relative).write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8")
    with (OUT / "annotation/source_blind_pilot.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=helper.FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(sheet)
    write_json(OUT / "provenance/SOURCE_REVIEW_TEMPLATE.json", {"status": "REVIEW_PENDING", "decisions": list(source_reviews.values())})
    write_json(OUT / "provenance/PARENT_INTEGRITY.json", {"v9_files_sha256_before_and_after_equal": parent_hashes, "source_evidence_sha256": evidence})
    write_json(OUT / "reports/LINEAGE_AND_DUPLICATE_REPORT.json", {
        "candidate_rows": len(restored), "families": families,
        "upstream_split_recorded_rows": sum(bool(r["upstream_split_recorded"]) for r in restored),
        "original_component_split_unknown_rows": sum(r["original_component_split"] is None for r in restored),
        "cross_family_groups": cross,
        "cross_family_rows": sum(r["rows"] for r in cross),
        "duplicate_resolution": "UNRESOLVED: keep grouped in one partition or explicitly exclude before freeze",
        "known_duplicate_limitation": "Inherited V9 exact/near grouping; not a semantic duplicate guarantee",
        "pilot_selection": "Up to 10 per provisional family, stable SHA256 ordering; no prior pilot or cross-family group; one row per duplicate group; <=8000 prompt+context characters",
        "pilot_representative": False,
    })
    write_json(OUT / "STATUS.json", {
        "dataset_version": VERSION, "state": "LINEAGE_RECOVERED_PILOT_AWAITING_HUMAN_REVIEW",
        "candidate_rows": len(restored), "pilot_rows": len(sheet), "canonical_rows": 0,
        "trainable": False, "frozen_split": False, "test_opened": False,
        "l2_run": False, "l3_run": False,
    })
    (OUT / "README.md").write_text(
        "# V10 English readiness candidate\n\n"
        "## Scope Boundary Declaration\n\n"
        "Private candidate provenance successor of V9. Original candidate texts are referenced from the pinned V9/source files; only the focused pilot is copied. No labels or model rows were created.\n\n"
        "The pilot is source-blind, non-representative, and not a validation set. Label the CSV without opening the provenance key or source review template. A separate source review is required before canonical use. Uncertain/hybrid or insufficient-context decisions remain quarantined.\n\n"
        "All recorded upstream splits are preserved verbatim. Aggregate-container split markers do not establish the original component split. Collection groups and duplicate groups constrain any future partition; they do not prove source independence. No split is frozen.\n\n"
        "V8 locked evaluation data and assistant proposals are excluded. Inherited English confidence >=0.95 and pattern screening are checked against unchanged source text. Pattern scans are not complete privacy reviews.\n",
        encoding="utf-8")
    files = {p.relative_to(OUT).as_posix(): {"sha256": sha(p), "bytes": p.stat().st_size} for p in OUT.rglob("*") if p.is_file()}
    write_json(OUT / "DATASET_MANIFEST.json", {
        "package_id": OUT.name, "dataset_version": VERSION, "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "parent_package_id": V9.name, "parent_manifest_sha256": sha(V9 / "DATASET_MANIFEST.json"),
        "language": "en", "candidate_rows": len(restored), "pilot_rows": len(sheet),
        "canonical_row_counts": {"train": 0, "validation": 0, "test": 0}, "trainable": False,
        "language_filter": helper.CONFIG["language_filter"],
        "data_changes": ["Recovered original split/file and collection group evidence into row provenance", "Added a bounded unchanged-text source-blind pilot; no synthetic records or canonical labels"],
        "files": files, "code_sha256": sha(Path(__file__)), "helper_sha256": sha(helper_path),
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "baseline": helper.CONFIG["baseline"], "seed": 42, "split_sha256": None,
        "gates_pending": ["human curator", "source rights/lineage/privacy decisions", "verified family independence and per-class 2/1/1 support", "duplicate resolution", "source-disjoint frozen split", "owner numeric L2 selection gates"],
        "historical_evaluation_payload_opened": False, "l2_fit": False, "l3_run": False,
    })
    print(json.dumps({"package": str(OUT), "manifest_sha256": sha(OUT / "DATASET_MANIFEST.json"),
                      "candidate_rows": len(restored), "pilot_rows": len(sheet),
                      "families": dict(selection_counts), "original_component_split_unknown_rows": sum(r["original_component_split"] is None for r in restored),
                      "cross_family_groups": len(cross), "canonical_rows": 0, "trainable": False}))


if __name__ == "__main__":
    main()
