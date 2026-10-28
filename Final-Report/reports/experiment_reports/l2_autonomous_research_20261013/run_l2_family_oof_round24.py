"""Run complete five-fold family-OOF for the R06 WUSTL train-family package."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
TRAINING = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline" / "training_bases"
TEMPLATE = ROOT / "run_l2_family_oof_round07.py"
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_l2_source_diverse_round21_r06"
OUTPUT = TRAINING / "pi_guard_tfidf_tier1" / "runs" / "l2_wustl_jb_train_family_oof_round24_r06_full_20261013"
REPORT = ROOT / "l2_wustl_jb_train_family_oof_round24_r06.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if REPORT.exists() or OUTPUT.exists():
        raise FileExistsError("ROUND24_OOF_OUTPUT_EXISTS; inspect before choosing a new version")
    spec = importlib.util.spec_from_file_location("l2_family_oof_round24_template", TEMPLATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("OOF_TEMPLATE_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PACKAGE = PACKAGE
    module.OUTPUT = OUTPUT
    module.REPORT = REPORT
    result = module.main()
    if result != 0:
        return result
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report["report_id"] = "l2_wustl_jb_train_family_oof_round24_r06"
    report["runner_wrapper_sha256"] = sha256(Path(__file__))
    report["shared_runner_logic_path"] = str(TEMPLATE)
    report["shared_runner_logic_sha256"] = sha256(TEMPLATE)
    report["data_semantics_note"] = (
        "The pinned WUSTL-CSPL in-the-wild collection contributes 120 train-only provisional JB references after configured privacy and exact/near-duplicate exclusions. All retained rows stay in one source-family group and therefore are held out together in one OOF fold. Publisher release lineage is separately tracked, but upstream online-source ancestry is not row-addressable; this is not proof of source-disjoint generalization. Validation and test payloads were not opened by OOF."
    )
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("ROUND24_OOF_REPORT_FINALIZED", json.dumps({
        "report": str(REPORT),
        "run_path_private": str(OUTPUT),
        "train_rows": report.get("train_rows"),
        "source_families_by_label": report.get("source_families_by_label"),
        "aggregate_metrics": report.get("aggregate_metrics"),
        "validation_opened": False,
        "test_opened": False,
        "l3_run": False,
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
