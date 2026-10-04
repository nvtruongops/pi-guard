#!/usr/bin/env python3
"""Run the five non-PIGuard Meeting 6 local harnesses without overwriting source results."""

from __future__ import annotations

import builtins
import contextlib
import hashlib
import importlib.util
import importlib.metadata
import io
import json
import os
import platform
import random
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TRUONG_WORKSPACE = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).with_name("six_model_runs_complete")
PIGUARD_PRIOR_RESULT = Path(__file__).parents[1] / "reproduction_audit_2026-09-28" / "piguard_fresh_run.json"

RUNNERS = [
    {
        "name": "DataSentinel",
        "package": "replications/DataSentinel_Liu_SP2025",
        "script": "run_datasentinel_replication.py",
        "entrypoint": "run_datasentinel_benchmark",
        "input": "datasets/datasentinel_eval_benchmark.json",
        "source_output": "DATASENTINEL_REPLICATION_BENCHMARK_RESULTS.json",
        "method_audit": "Local canary wrapper with hand-written regex cue lists; does not execute the paper's minimax detector.",
    },
    {
        "name": "PromptShield",
        "package": "replications/PromptShield_Jacob_CCS2024",
        "script": "run_promptshield_replication.py",
        "entrypoint": "run_promptshield_benchmark",
        "input": "datasets/promptshield_eval_benchmark.json",
        "source_output": "PROMPTSHIELD_REPLICATION_BENCHMARK_RESULTS.json",
        "method_audit": "TF-IDF + LogisticRegression is fitted and scored on the same 20-row evaluation file; not the paper's detector or a held-out test.",
    },
    {
        "name": "ModernBERT",
        "package": "replications/ModernBERT_Warner_2024",
        "script": "run_modernbert_replication.py",
        "entrypoint": "run_modernbert_benchmark",
        "input": "datasets/modernbert_context_eval_benchmark.json",
        "source_output": "MODERNBERT_REPLICATION_BENCHMARK_RESULTS.json",
        "method_audit": "Whitespace token split plus regex cue detection at 512/8192 words; no ModernBERT tokenizer or weights are loaded.",
    },
    {
        "name": "SmoothLLM",
        "package": "replications/SmoothLLM_Robey_NeurIPS2023",
        "script": "run_smoothllm_replication.py",
        "entrypoint": "evaluate_smoothllm_perturbations",
        "input": "datasets/smoothllm_eval_benchmark.json",
        "source_output": "SMOOTHLLM_REPLICATION_BENCHMARK_RESULTS.json",
        "method_audit": "Runs character perturbations and timing only; it does not run a victim LLM or measure jailbreak success.",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(f"six_audit_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def normalized(path) -> str:
    return os.path.normcase(os.path.abspath(os.fspath(path)))


def record_count(value) -> int | None:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        for key in ("data", "samples", "records", "examples"):
            if isinstance(value.get(key), list):
                return len(value[key])
    return None


def package_version(distribution: str) -> str | None:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    run_started = datetime.now(timezone.utc).isoformat()
    run_records = []
    failures = []

    for cfg in RUNNERS:
        package_dir = TRUONG_WORKSPACE / cfg["package"]
        source_script = package_dir / cfg["script"]
        input_path = package_dir / cfg["input"]
        dataset = json.loads(input_path.read_text(encoding="utf-8"))
        expected_output = package_dir / cfg["source_output"]
        audit_output = OUTPUT_DIR / f"{cfg['name']}_local_harness.json"
        log_path = OUTPUT_DIR / f"{cfg['name']}_stdout.txt"
        if audit_output.exists() and log_path.exists():
            result = json.loads(audit_output.read_text(encoding="utf-8"))
            patch_note = None
            status = "completed_reused"
            run_records.append(
                {
                    "name": cfg["name"],
                    "status": status,
                    "python_version": platform.python_version(),
                    "runner_path": str(source_script),
                    "runner_sha256": sha256(source_script),
                    "input_path": str(input_path),
                    "input_sha256": sha256(input_path),
                    "input_records": record_count(dataset),
                    "output_path": str(audit_output),
                    "output_sha256": sha256(audit_output),
                    "stdout_path": str(log_path),
                    "method_audit": cfg["method_audit"],
                    "compatibility_patch": patch_note,
                    "error": None,
                    "result_top_level_keys": list(result) if isinstance(result, dict) else None,
                }
            )
            print(f"{cfg['name']}: reused completed output; rows={record_count(dataset)}")
            continue
        backup_bytes = expected_output.read_bytes() if expected_output.exists() else None
        module = load_module(cfg["name"], source_script)
        real_open = builtins.open

        def redirected_open(file, mode="r", *args, **kwargs):
            if any(flag in mode for flag in ("w", "a", "x")) and normalized(file) == normalized(expected_output):
                return real_open(audit_output, mode, *args, **kwargs)
            return real_open(file, mode, *args, **kwargs)

        captured = io.StringIO()
        status = "completed"
        error = None
        compatibility_patch = None
        if cfg["name"] == "SmoothLLM":
            random.seed(42)
            module.np.random.seed(42)
        builtins.open = redirected_open
        try:
            with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
                getattr(module, cfg["entrypoint"])()
        except Exception as exc:  # Preserve failure as evidence and continue the remaining harness audit.
            status = "failed"
            error = f"{type(exc).__name__}: {exc}"
            failures.append(cfg["name"])
            captured.write(f"\n{error}\n")
        finally:
            builtins.open = real_open
            log_path.write_text(captured.getvalue(), encoding="utf-8")

        if expected_output.exists():
            current_bytes = expected_output.read_bytes()
            if backup_bytes is None or current_bytes != backup_bytes:
                expected_output.write_bytes(backup_bytes or b"")
                status = "failed"
                error = "Runner altered its canonical output despite redirection; original bytes restored."
                failures.append(cfg["name"])
        if status.startswith("completed") and not audit_output.exists():
            status = "failed"
            error = "Runner returned without producing its redirected JSON output."
            failures.append(cfg["name"])

        output_hash = sha256(audit_output) if audit_output.exists() else None
        result = json.loads(audit_output.read_text(encoding="utf-8")) if audit_output.exists() else None
        run_records.append(
            {
                "name": cfg["name"],
                "status": status,
                "python_version": platform.python_version(),
                "runner_path": str(source_script),
                "runner_sha256": sha256(source_script),
                "input_path": str(input_path),
                "input_sha256": sha256(input_path),
                "input_records": record_count(dataset),
                "output_path": str(audit_output),
                "output_sha256": output_hash,
                "stdout_path": str(log_path),
                "method_audit": cfg["method_audit"],
                "compatibility_patch": compatibility_patch,
                "error": error,
                "result_top_level_keys": list(result) if isinstance(result, dict) else None,
            }
        )
        print(f"{cfg['name']}: {status}; rows={record_count(dataset)}; output={audit_output.name}")

    if not PIGUARD_PRIOR_RESULT.exists():
        raise FileNotFoundError(f"Missing earlier fresh PIGuard result: {PIGUARD_PRIOR_RESULT}")
    piguard_output = OUTPUT_DIR / "PIGuard_Table7_fresh.json"
    shutil.copyfile(PIGUARD_PRIOR_RESULT, piguard_output)
    piguard_payload = json.loads(piguard_output.read_text(encoding="utf-8"))
    run_records.insert(
        0,
        {
            "name": "PIGuard",
            "status": "completed_prior_fresh_run",
            "python_version": piguard_payload.get("metadata", {}).get("python_version"),
            "runner_path": str(TRUONG_WORKSPACE / "replications/Paper_ACL2025_PIGuard_HaoLi/run_piguard_replication.py"),
            "runner_sha256": sha256(TRUONG_WORKSPACE / "replications/Paper_ACL2025_PIGuard_HaoLi/run_piguard_replication.py"),
            "input_path": "Recorded in copied PIGuard result and its runner dataset paths.",
            "input_sha256": None,
            "input_records": piguard_payload.get("metadata", {}).get("total_samples"),
            "output_path": str(piguard_output),
            "output_sha256": sha256(piguard_output),
            "stdout_path": None,
            "method_audit": "Released PIGuard checkpoint inference; fresh public Table 7 subset run, not training-from-scratch. PINT unavailable.",
            "error": None,
            "result_top_level_keys": list(piguard_payload),
        },
    )

    manifest = {
        "scope": "Six Meeting 6 baseline entries K1/K2/K3/K4/K6/K10 from task README.",
        "started_at_utc": run_started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "package_versions": {
            "scikit-learn": package_version("scikit-learn"),
            "numpy": package_version("numpy"),
            "PyYAML": package_version("PyYAML"),
            "matplotlib": package_version("matplotlib"),
        },
        "working_directory": str(ROOT),
        "results": run_records,
        "failed_models": failures,
        "meta_official_checkpoint_cache_check": {
            "cached": False,
            "model_id": "meta-llama/Prompt-Guard-86M",
            "access_note": "Official Hugging Face page requires agreeing to share contact information and review access conditions; no gated terms were accepted in this run.",
        },
    }
    manifest_path = OUTPUT_DIR / "six_model_execution_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    completed_count = sum(record["status"].startswith("completed") for record in run_records)
    print(f"manifest={manifest_path}; completed={completed_count}/6; failed={failures}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

