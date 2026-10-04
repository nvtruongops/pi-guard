"""Run the PIDS-Bench release's DeBERTa training code on a frozen data copy."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import runpy
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


EXPECTED = {
    "train.csv": "859124bfffe20483b337956efcb11c6bdaf6191835150f51a5e6da272ee5a2eb",
    "val.csv": "1445c0b33c220078d967fa34bb4da5e2981842ce288925b8f2542a4f9352cc64",
    "test.csv": "149092dc6a7a83d3da73e8c7b413ea5e215e3f96c5565767b6db56b3b7835d96",
    "eval_subsets/hard_benign_test.csv": "e3ddb1e6e9e04e1097b7bcf9a6f5e05b0a8d73e8d71b8d867f7ed85b89472cee",
    "eval_subsets/balanced_subtype_test.csv": "210e339329081b97ce95d2dfe4f4581e19bc83dd16a23b86cd36bd15b9ff2023",
    "eval_subsets/obfuscated_attacks.csv": "b151322f05ef83922c734c589804fc7eab53331b61b5ad153c72aaf683f7c691",
    "ood/domain_ood.csv": "d14acb99a69ac10559fde9ee22d0f20aa7a5816c4f48f279838d12ed0a6944f0",
    "ood/structural_ood.csv": "63d56a8ebbd0639404158b51b35863fc87b02e9869ee2526f5f90eaa48108dad",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def filtered_hard_benign(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        if not fields or "text" not in fields or "label" not in fields:
            raise ValueError(f"Unexpected CSV columns: {fields}")
        rows = list(reader)
    kept = [row for row in rows if (row.get("text") or "").strip()]
    if any(row["label"] != "0" for row in kept):
        raise ValueError("hard_benign_test contains a non-benign row")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(kept)
    return len(rows), len(kept)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--stage-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=16)
    parser.add_argument("--dynamic-padding", action="store_true")
    parser.add_argument("--resume-from-checkpoint", type=Path)
    args = parser.parse_args()

    upstream = args.upstream.resolve()
    run_dir = args.run_dir.resolve()
    stage_dir = args.stage_dir.resolve()
    resume_checkpoint = args.resume_from_checkpoint.resolve() if args.resume_from_checkpoint else None
    source_data = upstream / "data" / "pids_bench_v3"
    run_dir.mkdir(parents=True, exist_ok=True)
    if resume_checkpoint and not all(
        (resume_checkpoint / name).is_file()
        for name in ("trainer_state.json", "model.safetensors", "optimizer.pt", "scheduler.pt")
    ):
        raise SystemExit(f"Incomplete Trainer checkpoint: {resume_checkpoint}")
    if stage_dir.exists():
        raise SystemExit(f"Refusing to overwrite staged input: {stage_dir}")

    hashes = {}
    for rel, expected in EXPECTED.items():
        actual = sha256(source_data / rel)
        if actual != expected:
            raise SystemExit(f"Frozen data mismatch for {rel}: {actual} != {expected}")
        hashes[rel] = actual

    staged_data = stage_dir / "data" / "pids_bench_v3"
    staged_data.parent.mkdir(parents=True)
    shutil.copytree(source_data, staged_data)
    original_rows, kept_rows = filtered_hard_benign(
        staged_data / "eval_subsets" / "hard_benign_test.csv"
    )
    if (original_rows, kept_rows) != (1472, 808):
        raise SystemExit(f"Unexpected hard-benign row counts: {original_rows} -> {kept_rows}")

    config = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "upstream_remote": "https://github.com/ShirePyDev/Prompt-Injection-Detection-System",
        "upstream_commit": subprocess.check_output(
            ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True
        ).strip(),
        "python": sys.version,
        "platform": platform.platform(),
        "seed": args.seed,
        "epochs": 3,
        "learning_rate": 2e-5,
        "max_length": 512,
        "microbatch": args.batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "effective_batch_size": args.batch_size * args.gradient_accumulation_steps,
        "precision": "FP32",
        "dynamic_padding": args.dynamic_padding,
        "original_csv_sha256": hashes,
        "hard_benign_original_rows": original_rows,
        "hard_benign_retained_rows": kept_rows,
        "hard_benign_omitted_blank_text_rows": original_rows - kept_rows,
        "hard_benign_staged_csv_sha256": sha256(
            staged_data / "eval_subsets" / "hard_benign_test.csv"
        ),
        "data_adjustment": "Filtered blank/license-redacted text only in staged hard_benign_test; train/val/test and other eval files remain byte-identical.",
        "status": "running",
    }
    config_path = run_dir / "run_config.json"
    if resume_checkpoint:
        if not config_path.is_file():
            raise SystemExit(f"Cannot resume without the original run config: {config_path}")
        previous = json.loads(config_path.read_text(encoding="utf-8"))
        for key in ("upstream_commit", "seed", "microbatch", "gradient_accumulation_steps", "original_csv_sha256"):
            if previous.get(key) != config.get(key):
                raise SystemExit(f"Resume provenance mismatch for {key}")
        config = {**previous, **config}
        config["started_utc"] = previous["started_utc"]
        config["resumed_utc"] = datetime.now(timezone.utc).isoformat()
        config["resume_from_checkpoint"] = str(resume_checkpoint)
        config["status"] = "resumed"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    source_script = upstream / "src" / "baselines" / "deberta_v3.py"
    sys.path.insert(0, str((upstream / "src").resolve()))
    old_cwd = Path.cwd()
    os.chdir(stage_dir)
    try:
        namespace = runpy.run_path(str(source_script), run_name="pids_deberta_v3")
        if resume_checkpoint:
            trainer_class = namespace["Trainer"]
            original_train = trainer_class.train

            def resume_train(trainer, *train_args, **train_kwargs):
                return original_train(
                    trainer,
                    *train_args,
                    resume_from_checkpoint=str(resume_checkpoint),
                    **train_kwargs,
                )

            trainer_class.train = resume_train
        if args.dynamic_padding:
            def dynamic_tokenize_splits(dataset, tokenizer):
                out = {}
                for split in dataset:
                    def tokenize_batch(batch):
                        return tokenizer(batch["text"], truncation=True, padding=False, max_length=512)
                    remove = [col for col in dataset[split].column_names if col != "label"]
                    out[split] = dataset[split].map(
                        tokenize_batch, batched=True, remove_columns=remove
                    )
                return namespace["DatasetDict"](out)

            namespace["tokenize_splits"] = dynamic_tokenize_splits
        namespace["run_train"](
            num_epochs=3,
            batch_size=args.batch_size,
            lr=2e-5,
            seed=args.seed,
            gradient_accumulation_steps=args.gradient_accumulation_steps,
            out_dir=run_dir / "deberta_v3",
        )
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["status"] = "completed"
        config["completed_utc"] = datetime.now(timezone.utc).isoformat()
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    finally:
        os.chdir(old_cwd)


if __name__ == "__main__":
    main()
