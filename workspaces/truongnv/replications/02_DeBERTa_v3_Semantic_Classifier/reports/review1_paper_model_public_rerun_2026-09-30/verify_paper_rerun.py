"""Verify the pinned PIGuard checkpoint on PIGuard release evaluation assets."""

from __future__ import annotations

import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
WORKSPACE = RUN_DIR.parents[3]
PAPER_RUN = RUN_DIR / "run_manifest.json"
OUT_PATH = RUN_DIR / "verification_results.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_gzip_jsonl(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def expected_paper_rows(manifest: dict[str, Any]) -> dict[str, tuple[str, str, int]]:
    expected: dict[str, tuple[str, str, int]] = {}
    for filename, item in manifest["dataset_files"].items():
        path = WORKSPACE / Path(item["path"])
        if sha256_file(path) != item["sha256"]:
            raise AssertionError(f"Dataset hash mismatch: {filename}")
        value = read_json(path)
        if filename.startswith("NotInject_"):
            subset = filename.removesuffix(".json")
            for index, row in enumerate(value):
                expected[f"{subset}:{index}"] = ("NotInject", subset, 0)
        elif filename.startswith("BIPIA_"):
            subset = filename.removesuffix(".json")
            for category, payloads in value.items():
                for index, _payload in enumerate(payloads):
                    expected[f"{subset}:{category}:{index}"] = ("BIPIA_payload", subset, 1)
        elif filename == "wildguard.json":
            for index, _row in enumerate(value):
                expected[f"WildGuard_benign:{index}"] = ("WildGuard_benign", "WildGuard_benign", 0)
        else:
            raise AssertionError(f"Unexpected paper-benchmark dataset: {filename}")
    if len(expected) != manifest["input_rows"]:
        raise AssertionError(f"Expected {manifest['input_rows']} rows from sources; built {len(expected)}")
    return expected


def check_close(actual: float, recorded: float, label: str) -> None:
    if abs(actual - recorded) > 1e-10:
        raise AssertionError(f"{label}: recomputed={actual}, manifest={recorded}")


def verify_paper_checkpoint_outputs() -> dict[str, Any]:
    manifest = read_json(PAPER_RUN)
    expected = expected_paper_rows(manifest)
    model_summaries: dict[str, Any] = {}
    for model_key, run in manifest["model_runs"].items():
        if run["requested_revision"] != run["resolved_revision"]:
            raise AssertionError(f"Unpinned model resolution for {model_key}")
        path = RUN_DIR / run["predictions_path"]
        if sha256_file(path) != run["predictions_sha256"]:
            raise AssertionError(f"Prediction hash mismatch for {model_key}")
        predictions = read_gzip_jsonl(path)
        by_id = {row["id"]: row for row in predictions}
        if len(predictions) != run["expected_row_count"] or len(by_id) != len(predictions):
            raise AssertionError(f"Prediction count/uniqueness mismatch for {model_key}")
        if set(by_id) != set(expected):
            raise AssertionError(f"Source row identity mismatch for {model_key}")
        for row_id, row in by_id.items():
            benchmark, subset, label = expected[row_id]
            if (row["benchmark"], row["subset"], row["label"]) != (benchmark, subset, label):
                raise AssertionError(f"Label or subset mismatch for {model_key}:{row_id}")
            if row["prediction"] not in (0, 1):
                raise AssertionError(f"Invalid binary prediction for {model_key}:{row_id}")

        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in predictions:
            groups[row["subset"]].append(row)
        notinject = {
            subset: {
                "n": len(groups[subset]),
                "correct_benign": sum(row["prediction"] == 0 for row in groups[subset]),
                "benign_accuracy": sum(row["prediction"] == 0 for row in groups[subset]) / len(groups[subset]),
            }
            for subset in ("NotInject_one", "NotInject_two", "NotInject_three")
        }
        bipia = {
            subset: {
                "n": len(groups[subset]),
                "attack_flags": sum(row["prediction"] == 1 for row in groups[subset]),
                "attack_recall": sum(row["prediction"] == 1 for row in groups[subset]) / len(groups[subset]),
            }
            for subset in ("BIPIA_text", "BIPIA_code")
        }
        wildguard = groups["WildGuard_benign"]
        wildguard_accuracy = sum(row["prediction"] == 0 for row in wildguard) / len(wildguard)
        recorded = run["metrics"]
        check_close(
            sum(item["correct_benign"] for item in notinject.values()) / sum(item["n"] for item in notinject.values()),
            recorded["NotInject"]["accuracy"], f"{model_key} NotInject",
        )
        check_close(
            sum(item["attack_flags"] for item in bipia.values()) / sum(item["n"] for item in bipia.values()),
            recorded["BIPIA_payload"]["attack_recall"], f"{model_key} BIPIA pooled",
        )
        check_close(wildguard_accuracy, recorded["WildGuard_benign"]["accuracy"], f"{model_key} WildGuard")
        model_summaries[model_key] = {
            "model_id": run["model_id"],
            "revision": run["resolved_revision"],
            "parameter_count": run["parameter_count"],
            "max_length": run["max_length"],
            "rows": len(predictions),
            "prediction_sha256": run["predictions_sha256"],
            "NotInject": notinject,
            "BIPIA_payload": {
                "subsets": bipia,
                "official_equal_subset_macro_attack_recall": sum(item["attack_recall"] for item in bipia.values()) / 2,
                "pooled_attack_recall": sum(item["attack_flags"] for item in bipia.values()) / sum(item["n"] for item in bipia.values()),
            },
            "WildGuard_benign": {"n": len(wildguard), "benign_accuracy": wildguard_accuracy},
        }
    return {
        "status": "verified",
        "input_rows": len(expected),
        "dataset_sha256_checks": len(manifest["dataset_files"]),
        "models": model_summaries,
    }


def main() -> None:
    output = {"paper_checkpoint_benchmark": verify_paper_checkpoint_outputs()}
    OUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
