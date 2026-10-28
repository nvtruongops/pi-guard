"""Run the established full five-fold family-OOF protocol on R21 train rows.

Only the package/output/report paths differ from the round07 implementation.
The full, frozen training partition is used; validation and test payloads are
not opened by the OOF runner.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
TEMPLATE = ROOT / "run_l2_family_oof_round07.py"
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_l2_source_diverse_round21_r02"
OUTPUT = TRAINING / "pi_guard_tfidf_tier1" / "runs" / "l2_source_diverse_family_oof_round21_r02_full_20261013"
REPORT = ROOT / "l2_source_diverse_family_oof_round21_r02.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if REPORT.exists() or OUTPUT.exists():
        raise FileExistsError("ROUND21_OOF_OUTPUT_EXISTS; inspect before choosing a new version")
    spec = importlib.util.spec_from_file_location("l2_family_oof_round21_template", TEMPLATE)
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
    report["report_id"] = "l2_source_diverse_family_oof_round21_r02"
    report["runner_wrapper_sha256"] = sha256(Path(__file__))
    report["shared_runner_logic_path"] = str(TEMPLATE)
    report["shared_runner_logic_sha256"] = sha256(TEMPLATE)
    report["source_family_independence_note"] = (
        "R21 adds CLINC and Anthropic as separate train source families; their entire source families are held out as groups in OOF folds. ToxicChat is validation-only and is never in OOF training. Family-held-out metrics do not replace the external-source validation or the owner-approved L2 gate."
    )
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("ROUND21_OOF_REPORT_FINALIZED", json.dumps({
        "report": str(REPORT),
        "run_path_private": str(OUTPUT),
        "train_rows": report.get("train_rows"),
        "source_families_by_label": report.get("source_families_by_label"),
        "aggregate_metrics": report.get("aggregate_metrics"),
        "test_opened": False,
        "l3_run": False,
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
