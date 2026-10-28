"""Run full five-fold source-family OOF for the private R28 candidate."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
TRAINING = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline" / "training_bases"
ADAPTER_DIR = TRAINING / "pi_guard_tfidf_tier1"
TEMPLATE = ROOT / "run_l2_family_oof_round07.py"
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_l2_blackboxnlp_round28_candidate_r03_20261014"
OUTPUT = ADAPTER_DIR / "runs" / "l2_blackboxnlp_round28_candidate_r03_family_oof_20261014"
REPORT = ROOT / "l2_blackboxnlp_family_oof_round28.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if REPORT.exists() or OUTPUT.exists():
        raise FileExistsError("R28_OOF_OUTPUT_EXISTS; inspect before creating another version")
    sys.path.insert(0, str(ADAPTER_DIR))
    spec = importlib.util.spec_from_file_location("l2_blackboxnlp_family_oof_round07_template", TEMPLATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("R28_OOF_TEMPLATE_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PACKAGE = PACKAGE
    module.OUTPUT = OUTPUT
    module.REPORT = REPORT
    result = module.main()
    if result != 0:
        return result
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report["report_id"] = "l2_blackboxnlp_family_oof_round28_r03"
    report["runner_wrapper_sha256"] = sha256(Path(__file__))
    report["shared_runner_logic_path"] = str(TEMPLATE)
    report["shared_runner_logic_sha256"] = sha256(TEMPLATE)
    report["data_semantics_note"] = (
        "This full five-fold OOF uses only frozen training rows. The 6,551 added BlackboxNLP prompts are one algorithmic benchmark family derived from 300 seed groups and 35 attack methods; all rows in the family are held out together in one source-family fold. This is a diagnostic of one benchmark family, not independent-source or canonical-label evidence. Validation and test payloads were not used."
    )
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("R28_OOF_REPORT_FINALIZED", json.dumps({
        "report": str(REPORT),
        "run_path_private": str(OUTPUT),
        "train_rows": report.get("train_rows"),
        "source_families_by_label": report.get("source_families_by_label"),
        "aggregate_metrics": report.get("aggregate_metrics"),
        "validation_used": False,
        "test_opened": False,
        "l3_run": False,
        "smoke_run": False,
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
