"""Run full five-fold family-held-out OOF for the R27 JBB candidate."""
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
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_l2_jbb_round27_candidate_20261014"
OUTPUT = ADAPTER_DIR / "runs" / "l2_jbb_round27_candidate_family_oof_full_20261014"
REPORT = ROOT / "l2_jbb_round27_candidate_family_oof.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if REPORT.exists() or OUTPUT.exists():
        raise FileExistsError("R27_OOF_OUTPUT_EXISTS; inspect before creating another version")
    sys.path.insert(0, str(ADAPTER_DIR))
    spec = importlib.util.spec_from_file_location("l2_jbb_family_oof_round27_template", TEMPLATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("R27_OOF_TEMPLATE_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PACKAGE = PACKAGE
    module.OUTPUT = OUTPUT
    module.REPORT = REPORT
    result = module.main()
    if result != 0:
        return result
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report["report_id"] = "l2_jbb_round27_candidate_family_oof"
    report["runner_wrapper_sha256"] = sha256(Path(__file__))
    report["shared_runner_logic_path"] = str(TEMPLATE)
    report["shared_runner_logic_sha256"] = sha256(TEMPLATE)
    report["data_semantics_note"] = (
        "The R27 candidate adds 662 privacy-pattern-screened, exact/near-deduplicated provisional JB references from four JBB attack methods, with all 105 behavior groups and the complete JBB source family held out together in one source-family fold. This tests sensitivity to the added benchmark family but does not establish independent-source generalization or canonical labels. OOF used train rows only; validation and test payloads stayed unopened."
    )
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("R27_OOF_REPORT_FINALIZED", json.dumps({
        "report": str(REPORT),
        "run_path_private": str(OUTPUT),
        "train_rows": report.get("train_rows"),
        "source_families_by_label": report.get("source_families_by_label"),
        "aggregate_metrics": report.get("aggregate_metrics"),
        "validation_opened": False,
        "test_opened": False,
        "l3_run": False,
        "smoke_run": False,
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
