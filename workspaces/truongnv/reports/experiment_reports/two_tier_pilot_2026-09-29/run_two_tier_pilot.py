"""Source-mapped two-tier PI-Guard pilot; outputs live beside this script."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import platform
import random
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import sklearn
import torch
import transformers
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import FeatureUnion, Pipeline
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup


SEED = 42
MODEL_ID = "microsoft/deberta-v3-base"
MODEL_REVISION = "8ccc9b6f36199bec6961081d44eb72fb3f7353f"
JAILBREAK_DATASET = "jackhhao/jailbreak-classification"
JAILBREAK_REVISION = "2f2ceeb39658696fd3f462403562b6eea5306287"
CLASSES = ["benign", "prompt_injection", "jailbreak"]
CLASS_ID = {name: index for index, name in enumerate(CLASSES)}

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
REPO = HERE.parents[4]
PIGUARD_DIR = WORKSPACE / "replications/Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025"
PIGUARD_TRAIN = PIGUARD_DIR / "datasets/train.json"
PROMPTSHIELD_EVAL = (
    WORKSPACE
    / "replications/PromptShield_Jacob_CCS2024/PromptShield/camera_ready_datasets/en_dataset_no_dups/2024-11-28_evaluation_benchmark_en.json"
)
DATA_DIR = HERE / "data"
MODEL_DIR = HERE / "models/deberta_v3_source_mapped_3class"
RESULTS_PATH = HERE / "two_tier_pilot_results.json"
T1_MODEL_PATH = HERE / "tier1_tfidf_word_char.joblib"

BENIGN_TRAIN_SOURCES = {
    "chatbot_instruction_prompts",
    "open-instruct",
    "grok-conversation-harmless",
    "ultrachat_200k",
    "no_robots",
    "xtest-v2-copy",
    "awesome-chatgpt-prompts",
}
PI_TRAIN_SOURCES = {
    "safe-guard-prompt-injection",
    "prompt-injections",
    "InjecAgent",
    "StruQ",
}
JB_TRAIN_SOURCES = {"jailbreak-classification", "vigil-jailbreak-ada-002"}
T1_HELDOUT_SOURCES = {
    "Alpaca",
    "over-defense",
    "BIPIA",
    "Prompt-Injection-Mixed-Techniques",
    "ChatGPT-Jailbreak-Prompts",
    "LLM Augmented set",
}
T2_AMBIGUOUS_SOURCES = {"TaskTracker", "Question Set", "hackaprompt-dataset"}


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", str(text)).casefold().split())


def digest(text: str) -> str:
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def download_jailbreak_data():
    exported = {}
    paths = {split: DATA_DIR / f"jailbreak_classification_{split}.jsonl" for split in ("train", "test")}
    if all(path.is_file() for path in paths.values()):
        for split, path in paths.items():
            exported[split] = [json.loads(line) for line in path.read_text(encoding="utf-8").split("\n") if line]
    else:
        dataset = load_dataset(JAILBREAK_DATASET, revision=JAILBREAK_REVISION)
        for split, path in paths.items():
            rows = [dict(row) for row in dataset[split]]
            write_jsonl(path, rows)
            exported[split] = rows
    assert len(exported["train"]) == 1044 and len(exported["test"]) == 262
    assert all(set(row) == {"prompt", "type"} for split in exported.values() for row in split)
    grouped_types = collections.defaultdict(set)
    for row in exported["train"]:
        grouped_types[normalize(row["prompt"])].add(row["type"])
    conflicting = {key: sorted(values) for key, values in grouped_types.items() if len(values) != 1}
    assert not conflicting, f"Pinned jailbreak source has contradictory normalized labels: {len(conflicting)}"
    train_types = {key: next(iter(values)) for key, values in grouped_types.items()}
    piguard_source_rows = [row for row in load_json(PIGUARD_TRAIN) if row["source"] == "jailbreak-classification"]
    assert len(piguard_source_rows) == len(exported["train"])
    assert all(train_types.get(normalize(row["prompt"])) == ("jailbreak" if int(row["label"]) else "benign") for row in piguard_source_rows)
    write_json(
        DATA_DIR / "jailbreak_classification_source_manifest.json",
        {
            "dataset_id": JAILBREAK_DATASET,
            "revision": JAILBREAK_REVISION,
            "train_rows": len(exported["train"]),
            "test_rows": len(exported["test"]),
            "train_sha256": file_sha256(paths["train"]),
            "test_sha256": file_sha256(paths["test"]),
            "piguard_train_rows_exactly_label_matched_after_normalization": len(piguard_source_rows),
            "normalization_duplicates_same_label": len(exported["train"]) - len(train_types),
        },
    )
    return exported, {normalize(k): v for k, v in train_types.items()}


def load_bipia() -> list[dict]:
    rows = []
    for filename, variant in (("BIPIA_text.json", "BIPIA_text"), ("BIPIA_code.json", "BIPIA_code")):
        grouped = load_json(PIGUARD_DIR / "datasets" / filename)
        for category, prompts in grouped.items():
            for index, prompt in enumerate(prompts):
                rows.append(
                    {
                        "text": prompt,
                        "expected": "prompt_injection",
                        "dataset": variant,
                        "variant": category,
                        "record_id": f"{variant}:{category}:{index}:{digest(prompt)[:12]}",
                    }
                )
    return rows


def build_evaluation_sets(jailbreak_splits: dict[str, list[dict]]) -> dict[str, list[dict]]:
    sets: dict[str, list[dict]] = {}
    promptshield_rows = load_json(PROMPTSHIELD_EVAL)
    ps = []
    for index, row in enumerate(promptshield_rows):
        text = row["instruction"] + ("\n" + row["input"] if row.get("input", "") else "")
        ps.append(
            {
                "text": text,
                "expected": "prompt_injection" if int(row["flag"]) == 1 else "benign",
                "dataset": "PromptShield_camera_ready",
                "variant": row.get("type", "unspecified"),
                "record_id": f"promptshield:{index}:{digest(text)[:12]}",
            }
        )
    # Keep a deterministic class-stratified pilot slice. The complete, author-provided file remains the input.
    by_class = collections.defaultdict(list)
    for row in ps:
        by_class[row["expected"]].append(row)
    selected = []
    for label in ("benign", "prompt_injection"):
        selected.extend(sorted(by_class[label], key=lambda row: row["record_id"])[:200])
    sets["PromptShield_camera_ready_400_stratified"] = selected

    sets["BIPIA_text_and_code"] = load_bipia()

    piguard_valid = load_json(PIGUARD_DIR / "datasets/valid.json")
    valid_rows = []
    for index, row in enumerate(piguard_valid):
        source = row.get("source", "unspecified")
        if int(row["label"]) == 0:
            expected = "benign"
        elif source == "PINT_jailbreak":
            expected = "jailbreak"
        elif source in {"BIPIA_text", "BIPIA_code", "PINT_public_prompt_injection", "PINT_internal_prompt_injection"}:
            expected = "prompt_injection"
        else:
            raise ValueError(f"No source-level 3-class mapping for PIGuard valid source={source!r}")
        text = row["prompt"]
        valid_rows.append(
            {
                "text": text,
                "expected": expected,
                "dataset": "PIGuard_valid_144",
                "variant": source,
                "record_id": f"piguard-valid:{index}:{digest(text)[:12]}",
            }
        )
    sets["PIGuard_valid_144"] = valid_rows

    jbb_rows = []
    for index, row in enumerate(jailbreak_splits["test"]):
        expected = "jailbreak" if row["type"] == "jailbreak" else "benign"
        text = row["prompt"]
        jbb_rows.append(
            {
                "text": text,
                "expected": expected,
                "dataset": "jailbreak-classification_test",
                "variant": row["type"],
                "record_id": f"jailbreak-classification:test:{index}:{digest(text)[:12]}",
            }
        )
    sets["jailbreak_classification_test_262"] = jbb_rows

    notinject = []
    for filename in ("NotInject_one.json", "NotInject_two.json", "NotInject_three.json"):
        rows = load_json(PIGUARD_DIR / "datasets" / filename)
        for index, row in enumerate(rows):
            text = row["prompt"]
            notinject.append(
                {
                    "text": text,
                    "expected": "benign",
                    "dataset": "NotInject",
                    "variant": row.get("category", filename),
                    "record_id": f"notinject:{filename}:{index}:{digest(text)[:12]}",
                }
            )
    sets["NotInject_official_339"] = notinject

    wildguard = []
    for index, row in enumerate(load_json(PIGUARD_DIR / "datasets/wildguard.json")):
        text = row["prompt"]
        if int(row["label"]) != 0:
            continue
        wildguard.append(
            {
                "text": text,
                "expected": "benign",
                "dataset": "WildGuard",
                "variant": "benign",
                "record_id": f"wildguard:{index}:{digest(text)[:12]}",
            }
        )
    sets["WildGuard_benign_971"] = wildguard
    return sets


def source_classes(row: dict, jail_types: dict[str, str]) -> tuple[int | None, int | None]:
    """Return (binary_label, tri_class_id); None means source is not class-pure for that task."""
    source = row["source"]
    binary = int(row["label"])
    if source in BENIGN_TRAIN_SOURCES and binary == 0:
        return binary, CLASS_ID["benign"]
    if source == "jailbreak-classification":
        typ = jail_types.get(normalize(row["prompt"]))
        if typ not in {"benign", "jailbreak"}:
            return binary, None
        return binary, CLASS_ID["benign" if typ == "benign" else "jailbreak"]
    if source in PI_TRAIN_SOURCES and binary == 1:
        return binary, CLASS_ID["prompt_injection"]
    if source == "vigil-jailbreak-ada-002" and binary == 1:
        return binary, CLASS_ID["jailbreak"]
    return binary, None


def build_splits(jail_types: dict[str, str], eval_sets: dict[str, list[dict]]):
    rows = load_json(PIGUARD_TRAIN)
    assert len(rows) == 76735
    assert file_sha256(PIGUARD_TRAIN) == "806ded8bd85782a53d34faffe4fd92b3f2e0b3b431c43578ce77faea6b9ed911"

    # All raw external test texts, not only the selected PromptShield pilot slice, are blocked from training.
    eval_rows_for_overlap = [row for group in eval_sets.values() for row in group]
    full_ps = load_json(PROMPTSHIELD_EVAL)
    for index, row in enumerate(full_ps):
        text = row["instruction"] + ("\n" + row["input"] if row.get("input", "") else "")
        eval_rows_for_overlap.append({"text": text, "record_id": f"promptshield-full:{index}"})
    blocked_hashes = {digest(row["text"]) for row in eval_rows_for_overlap}

    train_counts = collections.Counter()
    normalized_labels = collections.defaultdict(set)
    for row in rows:
        text = row.get("prompt", "")
        if normalize(text):
            normalized_labels[digest(text)].add(int(row["label"]))
    conflict_hashes = {key for key, labels in normalized_labels.items() if len(labels) > 1}

    heldout = []
    t1_pool = []
    t2_by_class = collections.defaultdict(list)
    for index, row in enumerate(rows):
        text = row.get("prompt", "")
        if not normalize(text) or digest(text) in conflict_hashes or digest(text) in blocked_hashes:
            continue
        source = row["source"]
        if source in {"Alpaca", "Prompt-Injection-Mixed-Techniques", "ChatGPT-Jailbreak-Prompts"}:
            tri = {"Alpaca": "benign", "Prompt-Injection-Mixed-Techniques": "prompt_injection", "ChatGPT-Jailbreak-Prompts": "jailbreak"}[source]
            heldout.append({"text": text, "label": CLASS_ID[tri], "source": source, "index": index, "record_id": f"piguard-train:{source}:{index}:{digest(text)[:12]}"})
            continue
        if source in T1_HELDOUT_SOURCES:
            continue
        binary, tri_id = source_classes(row, jail_types)
        t1_pool.append({"text": text, "label": binary, "source": source, "index": index, "record_id": f"piguard-train:{source}:{index}:{digest(text)[:12]}"})
        if tri_id is not None and source not in T2_AMBIGUOUS_SOURCES:
            t2_by_class[tri_id].append({"text": text, "label": tri_id, "source": source, "index": index, "record_id": f"piguard-train:{source}:{index}:{digest(text)[:12]}"})

    # Drop normalized duplicates, preserving only a single deterministic record per class.
    def unique_by_digest(items):
        result = {}
        for item in sorted(items, key=lambda x: (x["record_id"], x["source"])):
            result.setdefault(digest(item["text"]), item)
        return list(result.values())

    t1_pool = unique_by_digest(t1_pool)
    t2_by_class = {label: unique_by_digest(items) for label, items in t2_by_class.items()}
    heldout_label_by_hash = collections.defaultdict(set)
    for item in heldout:
        heldout_label_by_hash[digest(item["text"])].add(item["label"])
    heldout_conflicts = {key for key, labels in heldout_label_by_hash.items() if len(labels) > 1}
    heldout = [item for item in heldout if digest(item["text"]) not in heldout_conflicts]
    val_by_class = collections.defaultdict(list)
    for item in unique_by_digest(heldout):
        val_by_class[item["label"]].append(item)
    validation_hashes = {digest(item["text"]) for group in val_by_class.values() for item in group}
    t1_pool = [item for item in t1_pool if digest(item["text"]) not in validation_hashes]
    t2_by_class = {
        label: [item for item in items if digest(item["text"]) not in validation_hashes]
        for label, items in t2_by_class.items()
    }
    assert set(t2_by_class) == {0, 1, 2}, {k: len(v) for k, v in t2_by_class.items()}
    assert all(len(val_by_class[i]) > 0 for i in range(3)), {k: len(v) for k, v in val_by_class.items()}
    assert all(digest(row["text"]) not in blocked_hashes for rows_ in t2_by_class.values() for row in rows_)

    # Deterministic class-balanced T2 subset: capped by the smallest source-backed class.
    n_per_class = min(600, *(len(t2_by_class[i]) for i in range(3)))
    assert n_per_class >= 300, f"Insufficient source-pure training rows: { {k: len(v) for k,v in t2_by_class.items()} }"
    t2_train = []
    for label in range(3):
        ordered = sorted(t2_by_class[label], key=lambda item: digest(item["record_id"]))
        t2_train.extend(ordered[:n_per_class])

    # Bound the validation pass deterministically while retaining all 79 source-held-out jailbreaks.
    t2_validation = []
    for label in range(3):
        cap = 500 if label != CLASS_ID["jailbreak"] else 200
        ordered = sorted(val_by_class[label], key=lambda item: digest(item["record_id"]))
        t2_validation.extend(ordered[:cap])
    t1_validation = t2_validation

    assert not ({digest(x["text"]) for x in t1_pool} & {digest(x["text"]) for x in t1_validation})
    assert not ({digest(x["text"]) for x in t2_train} & {digest(x["text"]) for x in t2_validation})
    train_counts.update(item["source"] for item in t1_pool)
    return t1_pool, t1_validation, t2_train, t2_validation, blocked_hashes, conflict_hashes, train_counts, len(heldout_conflicts)


def fit_tfidf(train_rows, validation_rows):
    if T1_MODEL_PATH.is_file():
        pipeline = joblib.load(T1_MODEL_PATH)
    else:
        pipeline = Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("word", TfidfVectorizer(ngram_range=(1, 3), max_features=20000, sublinear_tf=True, dtype=np.float32)),
                            ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=30000, sublinear_tf=True, dtype=np.float32)),
                        ]
                    ),
                ),
                ("classifier", LogisticRegression(C=2.0, max_iter=300, class_weight="balanced", random_state=SEED, solver="liblinear")),
            ]
        )
        pipeline.fit([x["text"] for x in train_rows], [x["label"] for x in train_rows])
        joblib.dump(pipeline, T1_MODEL_PATH, compress=3)
    v_texts = [x["text"] for x in validation_rows]
    v_scores = pipeline.predict_proba(v_texts)[:, list(pipeline.named_steps["classifier"].classes_).index(1)]
    benign_scores = [score for score, row in zip(v_scores, validation_rows) if row["label"] == CLASS_ID["benign"]]
    attack_scores = [score for score, row in zip(v_scores, validation_rows) if row["label"] != CLASS_ID["benign"]]

    # Route positives to Tier 2; choose the strongest threshold that keeps Tier-1 validation benign FPR <= 1.5%.
    candidates = sorted(set(float(x) for x in np.r_[benign_scores, attack_scores]))
    best = None
    for threshold in candidates:
        fpr = float(np.mean(np.asarray(benign_scores) >= threshold))
        attack_recall = float(np.mean(np.asarray(attack_scores) >= threshold))
        if fpr <= 0.015 and (best is None or attack_recall > best["attack_route_recall"] or (attack_recall == best["attack_route_recall"] and threshold > best["threshold"])):
            best = {"threshold": threshold, "benign_fpr": fpr, "attack_route_recall": attack_recall}
    assert best is not None
    val_all = np.asarray(v_scores)
    val_labels = np.asarray([row["label"] != CLASS_ID["benign"] for row in validation_rows], dtype=int)
    val_pred = (val_all >= best["threshold"]).astype(int)
    return pipeline, best, {
        "rows": len(validation_rows),
        "benign_rows": len(benign_scores),
        "attack_rows": len(attack_scores),
        "threshold": best["threshold"],
        "benign_fpr_at_route_threshold": best["benign_fpr"],
        "attack_route_recall": best["attack_route_recall"],
        "classification_report": classification_report(val_labels, val_pred, labels=[0, 1], target_names=["benign", "attack"], output_dict=True, zero_division=0),
    }


class PromptDataset(Dataset):
    def __init__(self, rows):
        self.rows = rows

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        row = self.rows[index]
        return row["text"], int(row["label"])


def collate_text(tokenizer):
    def collate(batch):
        texts, labels = zip(*batch)
        tokens = tokenizer(list(texts), truncation=True, max_length=256, padding=True, return_tensors="pt")
        tokens["labels"] = torch.tensor(labels, dtype=torch.long)
        return tokens
    return collate


def train_deberta(train_rows, validation_rows):
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.set_num_threads(min(14, os.cpu_count() or 1))
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        num_labels=3,
        id2label={i: name for i, name in enumerate(CLASSES)},
        label2id={name: i for i, name in enumerate(CLASSES)},
    )
    batch_size = 4
    train_loader = DataLoader(PromptDataset(train_rows), batch_size=batch_size, shuffle=True, collate_fn=collate_text(tokenizer))
    val_loader = DataLoader(PromptDataset(validation_rows), batch_size=8, shuffle=False, collate_fn=collate_text(tokenizer))
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    total_steps = len(train_loader)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=max(1, int(total_steps * 0.06)), num_training_steps=total_steps)
    started = time.perf_counter()
    model.train()
    losses = []
    for step, batch in enumerate(train_loader, start=1):
        batch = {key: value for key, value in batch.items()}
        output = model(**batch)
        loss = output.loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad(set_to_none=True)
        losses.append(float(loss.detach().cpu()))
        if step == 1 or step % 25 == 0 or step == total_steps:
            print(f"deberta_train step={step}/{total_steps} loss={losses[-1]:.5f}", flush=True)
    train_seconds = time.perf_counter() - started

    model.eval()
    val_logits, val_labels = [], []
    with torch.inference_mode():
        for batch in val_loader:
            labels = batch.pop("labels")
            val_logits.append(model(**batch).logits.cpu())
            val_labels.extend(labels.tolist())
    predictions = torch.cat(val_logits).argmax(dim=1).numpy()
    validation_metrics = {
        "rows": len(validation_rows),
        "accuracy": float(np.mean(predictions == np.asarray(val_labels))),
        "confusion_matrix_labels_0_1_2": confusion_matrix(val_labels, predictions, labels=[0, 1, 2]).tolist(),
        "classification_report": classification_report(val_labels, predictions, labels=[0, 1, 2], target_names=CLASSES, output_dict=True, zero_division=0),
    }
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(MODEL_DIR, safe_serialization=True)
    tokenizer.save_pretrained(MODEL_DIR)
    return tokenizer, model, {
        "base_model": MODEL_ID,
        "base_revision": MODEL_REVISION,
        "classes": CLASSES,
        "train_rows": len(train_rows),
        "balanced_rows_per_class": len(train_rows) // 3,
        "validation_metrics": validation_metrics,
        "epochs": 1,
        "batch_size": batch_size,
        "max_length": 256,
        "learning_rate": 2e-5,
        "seed": SEED,
        "mean_training_loss": float(np.mean(losses)),
        "train_seconds": train_seconds,
    }


def batched_model_predict(model, tokenizer, texts, batch_size=8):
    outputs = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            batch_texts = texts[start : start + batch_size]
            tokens = tokenizer(batch_texts, truncation=True, max_length=256, padding=True, return_tensors="pt")
            outputs.extend(model(**tokens).logits.softmax(-1).cpu().numpy())
    return np.asarray(outputs)


def evaluate_cascade(t1, threshold, tokenizer, model, eval_sets):
    all_predictions = []
    per_dataset = {}
    routed_texts = []
    for dataset_name, rows in eval_sets.items():
        texts = [row["text"] for row in rows]
        expected = [CLASS_ID[row["expected"]] for row in rows]
        t1_scores = t1.predict_proba(texts)[:, list(t1.named_steps["classifier"].classes_).index(1)]
        route_indices = np.flatnonzero(t1_scores >= threshold).tolist()
        predictions = np.full(len(rows), CLASS_ID["benign"], dtype=int)
        if route_indices:
            t2_probabilities = batched_model_predict(model, tokenizer, [texts[index] for index in route_indices])
            predictions[route_indices] = t2_probabilities.argmax(axis=1)
        metrics = {
            "rows": len(rows),
            "accuracy": float(np.mean(predictions == np.asarray(expected))),
            "routed_to_deberta": len(route_indices),
            "route_fraction": len(route_indices) / max(1, len(rows)),
            "confusion_matrix_labels_0_1_2": confusion_matrix(expected, predictions, labels=[0, 1, 2]).tolist(),
            "classification_report": classification_report(expected, predictions, labels=[0, 1, 2], target_names=CLASSES, output_dict=True, zero_division=0),
        }
        by_variant = {}
        groups = collections.defaultdict(list)
        for index, row in enumerate(rows):
            groups[row["variant"]].append(index)
        for variant, indices in groups.items():
            y = np.asarray(expected)[indices]
            p = predictions[indices]
            by_variant[variant] = {
                "rows": len(indices),
                "accuracy": float(np.mean(y == p)),
                "expected_class": CLASSES[int(y[0])] if len(set(y.tolist())) == 1 else "mixed",
                "recall": float(np.mean(y == p)) if len(set(y.tolist())) == 1 else None,
            }
        metrics["by_variant"] = by_variant
        per_dataset[dataset_name] = metrics
        all_predictions.extend(
            {
                "dataset": row["dataset"],
                "record_id": row["record_id"],
                "variant": row["variant"],
                "expected": row["expected"],
                "predicted": CLASSES[int(predictions[index])],
                "tier1_attack_score": float(t1_scores[index]),
                "sent_to_tier2": bool(index in set(route_indices)),
            }
            for index, row in enumerate(rows)
        )
        for i, row in enumerate(rows):
            routed_texts.append((row, float(t1_scores[i])))

    # Request-level latency on a deterministic, class-stratified, cross-source slice; includes TF-IDF, tokenization and DeBERTa when routed.
    by_expected = collections.defaultdict(list)
    for row, _ in routed_texts:
        by_expected[row["expected"]].append(row)
    latency_rows = []
    for label in CLASSES:
        candidates = sorted(by_expected[label], key=lambda row: row["record_id"])
        latency_rows.extend(candidates[:20])
    random.Random(SEED).shuffle(latency_rows)
    latencies_ms = []
    for row in latency_rows:
        start = time.perf_counter()
        score = t1.predict_proba([row["text"]])[0, list(t1.named_steps["classifier"].classes_).index(1)]
        if score >= threshold:
            tokens = tokenizer(row["text"], truncation=True, max_length=256, return_tensors="pt")
            with torch.inference_mode():
                model(**tokens)
        latencies_ms.append((time.perf_counter() - start) * 1000.0)
    latency_summary = {
        "rows": len(latencies_ms),
        "class_stratified_rows_per_class": 20,
        "includes_tfidf_and_tokenization_and_conditional_deberta": True,
        "mean_ms": float(np.mean(latencies_ms)),
        "median_ms": float(np.median(latencies_ms)),
        "p95_ms_nearest_rank": float(np.quantile(latencies_ms, 0.95, method="higher")),
        "max_ms": float(np.max(latencies_ms)),
        "route_fraction": float(np.mean([t1.predict_proba([row["text"]])[0, list(t1.named_steps["classifier"].classes_).index(1)] >= threshold for row in latency_rows])),
    }
    return per_dataset, all_predictions, latency_summary


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    pinned_data, jail_types = download_jailbreak_data()
    eval_sets = build_evaluation_sets(pinned_data)
    t1_rows, validation_rows, t2_rows, t2_validation, blocked_hashes, conflict_hashes, source_counts, heldout_conflict_count = build_splits(jail_types, eval_sets)

    training_manifest = []
    for row in t1_rows:
        training_manifest.append({"tier": "T1", "record_id": row["record_id"], "source": row["source"], "binary_label": row["label"]})
    for row in t2_rows:
        training_manifest.append({"tier": "T2", "record_id": row["record_id"], "source": row["source"], "class": CLASSES[row["label"]]})
    write_jsonl(HERE / "training_manifest.jsonl", training_manifest)
    write_jsonl(HERE / "evaluation_manifest.jsonl", [{key: value for key, value in row.items() if key != "text"} for rows in eval_sets.values() for row in rows])

    t1, threshold_info, t1_validation_metrics = fit_tfidf(t1_rows, validation_rows)
    print(f"tier1 rows={len(t1_rows)} validation={len(validation_rows)} threshold={threshold_info['threshold']:.8f} val_attack_route_recall={threshold_info['attack_route_recall']:.4f}", flush=True)

    tokenizer, model, t2_train_info = train_deberta(t2_rows, t2_validation)
    print("deberta_finetune_complete", flush=True)
    per_dataset, predictions, latency = evaluate_cascade(t1, threshold_info["threshold"], tokenizer, model, eval_sets)
    write_jsonl(HERE / "evaluation_predictions.jsonl", predictions)

    upstream_paths = [
        PIGUARD_TRAIN,
        PROMPTSHIELD_EVAL,
        PIGUARD_DIR / "datasets/valid.json",
        PIGUARD_DIR / "datasets/BIPIA_text.json",
        PIGUARD_DIR / "datasets/BIPIA_code.json",
        PIGUARD_DIR / "datasets/NotInject_one.json",
        PIGUARD_DIR / "datasets/NotInject_two.json",
        PIGUARD_DIR / "datasets/NotInject_three.json",
        PIGUARD_DIR / "datasets/wildguard.json",
        DATA_DIR / "jailbreak_classification_train.jsonl",
        DATA_DIR / "jailbreak_classification_test.jsonl",
    ]
    results = {
        "status": "completed",
        "scope_boundary": {
            "in_scope": "A source-mapped, exploratory two-tier pilot in workspaces/truongnv; run real TF-IDF and DeBERTa checkpoints and compare on held-out data.",
            "out_of_scope": "Full PIGuard paper retraining, Meta Prompt Guard reproduction, private PINT reproduction, multilingual robustness claims, or any Review 2 task specification not present in the workspace.",
            "class_mapping": "PIGuard labels are binary. Three-class T2 labels are derived only from explicitly selected dataset/source names and are a project pilot mapping, not author-published three-class labels.",
        },
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "scikit_learn": sklearn.__version__,
            "cpu_threads": torch.get_num_threads(),
            "cuda_available": torch.cuda.is_available(),
        },
        "sources": {
            str(path.relative_to(REPO)): {"sha256": file_sha256(path), "bytes": path.stat().st_size}
            for path in upstream_paths
        },
        "dataset_construction": {
            "piguard_train_rows_verified": 76735,
            "piguard_train_sha256_verified": True,
            "normalized_duplicate_label_conflict_hashes_dropped": len(conflict_hashes),
            "source_heldout_validation_label_conflicts_dropped": heldout_conflict_count,
            "normalized_hashes_blocked_for_external_test_overlap": len(blocked_hashes),
            "tier1_train_rows": len(t1_rows),
            "tier1_train_class_counts": dict(collections.Counter("attack" if row["label"] == 1 else "benign" for row in t1_rows)),
            "tier1_train_source_counts": dict(sorted(collections.Counter(row["source"] for row in t1_rows).items())),
            "tier1_and_t2_validation_class_counts": dict(collections.Counter(CLASSES[row["label"]] for row in validation_rows)),
            "tier2_train_class_counts": dict(collections.Counter(CLASSES[row["label"]] for row in t2_rows)),
            "excluded_from_tri_class_mapping": sorted(T2_AMBIGUOUS_SOURCES),
            "excluded_synthetic_source": "LLM Augmented set",
            "external_test_overlap_rows_dropped_from_training": True,
        },
        "tier1": {
            "model": "word (1,3) + char_wb (3,5) TF-IDF + LogisticRegression",
            "training_rows": len(t1_rows),
            "calibration": t1_validation_metrics,
            "threshold_selection": "maximize validation attack routing recall subject to held-out benign route FPR <= 1.5%",
            "route_threshold": threshold_info["threshold"],
            "heldout_metrics": t1_validation_metrics,
        },
        "tier2": t2_train_info,
        "cascade_evaluation": {
            "decision_rule": "T1 score below threshold -> fast-pass benign; otherwise DeBERTa predicts benign/PI/jailbreak.",
            "per_dataset": per_dataset,
            "request_level_latency": latency,
            "limitations": [
                "PromptShield uses a deterministic 400-row class-balanced pilot slice, not all 23,369 rows; the full paper dataset remains locally available and a ProtectAI comparator was run on all rows separately.",
                "No verified multilingual prompt-injection test set was available. PINT has only 144 public validation rows; authors do not publish the full PINT benchmark.",
                "Encoding and exfiltration coverage comes from small BIPIA category slices; it does not establish robustness against adaptive attacks.",
                "The source-derived tri-class mapping is not a gold-standard ontology. Treat this as exploratory evidence, not a finalized model result.",
                "CPU P95 is measured on a deterministic 60-request class-stratified subset, not a deployment traffic distribution.",
            ],
        },
        "artifacts": {
            "tier1_model": str((HERE / "tier1_tfidf_word_char.joblib").relative_to(REPO)),
            "tier2_model_dir": str(MODEL_DIR.relative_to(REPO)),
            "training_manifest": str((HERE / "training_manifest.jsonl").relative_to(REPO)),
            "evaluation_manifest": str((HERE / "evaluation_manifest.jsonl").relative_to(REPO)),
            "predictions": str((HERE / "evaluation_predictions.jsonl").relative_to(REPO)),
        },
    }
    write_json(RESULTS_PATH, results)
    print(f"results={RESULTS_PATH}", flush=True)


if __name__ == "__main__":
    main()

