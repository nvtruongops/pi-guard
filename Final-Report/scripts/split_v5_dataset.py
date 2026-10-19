#!/usr/bin/env python3
"""Freeze a source-stratified, prompt-family-aware split of the v5 corpus."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def source_names(row: dict) -> set[str]:
    return {str(source["dataset"]) for source in row["sources"]}


def primary_source_stratum(row: dict) -> str:
    names = source_names(row)
    label = str(row["label"])
    if label == "benign":
        candidates = (
            ("dronefreak/PromptScreen", "PromptScreen"),
            ("hendzh/PromptShield", "PromptShield"),
            ("TrustAIRLab/in-the-wild-jailbreak-prompts", "TrustAIRLab"),
        )
    elif label == "PI":
        candidates = (
            ("dronefreak/PromptScreen", "PromptScreen"),
            ("hendzh/PromptShield", "PromptShield"),
        )
    elif label == "JB":
        if names & {"TrustAIRLab/in-the-wild-jailbreak-prompts", "WUSTL-CSPL/LLMJailbreak"}:
            return "TrustAIRLab+WUSTL"
        candidates = (
            ("JailBreakV-28K", "JailBreakV-28K"),
            ("sevdeawesome/jailbreak_success", "WhatFeatures"),
            ("dronefreak/PromptScreen", "PromptScreen"),
        )
    else:
        raise ValueError(f"Unknown class for source stratification: {label}")
    for dataset, stratum in candidates:
        if dataset in names:
            return stratum
    raise ValueError(f"No primary source stratum for {label} row {row['id']}")

ROOT = Path.cwd()
CORPUS = ROOT / "balanced_three_label.jsonl"
CORPUS_MANIFEST = ROOT / "manifest.json"
SPLITS = ROOT / "splits"
PARTITIONS = ("train", "validation", "test")
RATIOS = {"train": 0.70, "validation": 0.15, "test": 0.15}
SEED = 42
SIMILARITY_PERCENT = 85


def safe_path(path: Path) -> Path:
    root = ROOT.resolve()
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise RuntimeError(f"Path outside corpus directory: {resolved}")
    current = path
    while current != ROOT:
        if current.is_symlink() or getattr(current, "is_junction", lambda: False)():
            raise RuntimeError(f"Refusing symlink/reparse path: {current}")
        current = current.parent
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_corpus() -> tuple[list[dict], list[str], str]:
    safe_path(CORPUS)
    safe_path(CORPUS_MANIFEST)
    source_manifest = json.loads(CORPUS_MANIFEST.read_text(encoding="utf-8"))
    if source_manifest["dataset_version"] != "5.0.0":
        raise RuntimeError("Expected the approved v5.0.0 candidate corpus")
    corpus_hash = sha256_file(CORPUS)
    if corpus_hash != source_manifest["artifact_files"][CORPUS.name]["sha256"]:
        raise RuntimeError("Corpus SHA-256 differs from the v5 manifest")
    with CORPUS.open(encoding="utf-8", newline="") as stream:
        lines = list(stream)
    rows = [json.loads(line) for line in lines]
    if len(rows) != source_manifest["balancing"]["final_rows"]:
        raise RuntimeError("Corpus row count differs from the v5 manifest")
    ids: set[str] = set()
    labels: Counter[str] = Counter()
    for row in rows:
        row_id = row["id"]
        if row_id in ids:
            raise RuntimeError(f"Duplicate corpus ID: {row_id}")
        ids.add(row_id)
        label = row["label"]
        if label not in LABEL_IDS or row["label_id"] != LABEL_IDS[label]:
            raise RuntimeError(f"Invalid label mapping: {row_id}")
        if hashlib.sha256(normalize(row["text"]).encode("utf-8")).hexdigest() != row_id:
            raise RuntimeError(f"Corpus ID/text mismatch: {row_id}")
        labels[label] += 1
    if dict(labels) != source_manifest["balancing"]["final_label_counts"]:
        raise RuntimeError("Corpus label counts differ from the v5 manifest")
    return rows, lines, corpus_hash


class Groups:
    def __init__(self, count: int):
        self.parent = list(range(count))
        self.size = [1] * count

    def find(self, item: int) -> int:
        while item != self.parent[item]:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def join(self, first: int, second: int) -> bool:
        first, second = self.find(first), self.find(second)
        if first == second:
            return False
        if self.size[first] < self.size[second]:
            first, second = second, first
        self.parent[second] = first
        self.size[first] += self.size[second]
        return True


def shingle_hashes(text: str) -> set[int]:
    words = re.findall(r"\w+", normalize(text))
    if len(words) < 5:
        chunks = [" ".join(words)]
    else:
        chunks = (" ".join(words[pos:pos + 5]) for pos in range(len(words) - 4))
    return {
        int.from_bytes(hashlib.blake2b(chunk.encode("utf-8"), digest_size=8).digest(), "big")
        for chunk in chunks
    }


def prompt_groups(rows: list[dict]) -> tuple[Groups, dict[str, int]]:
    groups = Groups(len(rows))
    explicit: dict[tuple[str, str], int] = {}
    buckets: dict[tuple[int, ...], list[int]] = defaultdict(list)
    shingles: list[set[int]] = []
    explicit_joins = 0
    for index, row in enumerate(rows):
        for source in row["sources"]:
            if source["dataset"] == "sevdeawesome/jailbreak_success":
                name = source.get("prompt_name")
                if name:
                    key = (source["dataset"], str(name))
                    if key in explicit:
                        explicit_joins += groups.join(index, explicit[key])
                    else:
                        explicit[key] = index
        hashes = shingle_hashes(row["text"])
        shingles.append(hashes)
        sketch = sorted(hashes)[:12]
        for start in range(0, len(sketch) - 2, 3):
            buckets[(start // 3, *sketch[start:start + 3])].append(index)

    seen_pairs: set[int] = set()
    compared = 0
    similar_pairs = 0
    for members in buckets.values():
        if len(members) < 2:
            continue
        members.sort(key=lambda index: (len(shingles[index]), index))
        for position, left in enumerate(members):
            left_hashes = shingles[left]
            left_size = len(left_hashes)
            for right in members[position + 1:]:
                right_hashes = shingles[right]
                right_size = len(right_hashes)
                if left_size * 100 < SIMILARITY_PERCENT * right_size:
                    break
                key = min(left, right) * len(rows) + max(left, right)
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                compared += 1
                common = len(left_hashes & right_hashes)
                if common * 100 >= SIMILARITY_PERCENT * (left_size + right_size - common):
                    similar_pairs += 1
                    groups.join(left, right)
    grouped = Counter(groups.find(index) for index in range(len(rows)))
    mixed = Counter()
    for index, row in enumerate(rows):
        mixed[groups.find(index), row["label"]] += 1
    mixed_roots = {root for root, _ in mixed if sum(mixed[root, label] > 0 for label in LABEL_IDS) > 1}
    return groups, {
        "groups": len(grouped),
        "largest_group_rows": max(grouped.values()),
        "rows_in_non_singleton_groups": sum(count for count in grouped.values() if count > 1),
        "mixed_label_groups": len(mixed_roots),
        "explicit_family_joins": explicit_joins,
        "candidate_pairs_compared": compared,
        "similar_pairs_at_or_above_0_85": similar_pairs,
    }


def assign_groups(rows: list[dict], groups: Groups) -> tuple[list[str], dict]:
    members: dict[int, list[int]] = defaultdict(list)
    dimensions: list[tuple[str, str]] = []
    totals: Counter[str] = Counter()
    for index, row in enumerate(rows):
        label = row["label"]
        source = primary_source_stratum(row)
        key = (label, source)
        dimensions.append(key)
        members[groups.find(index)].append(index)
        totals["all"] += 1
        totals[f"label:{label}"] += 1
        totals[f"source:{label}:{source}"] += 1

    order = sorted(
        members.values(),
        key=lambda indices: (
            -len(indices),
            hashlib.sha256(f"{SEED}:{min(rows[i]['id'] for i in indices)}".encode()).hexdigest(),
        ),
    )
    current: dict[str, Counter[str]] = {name: Counter() for name in PARTITIONS}
    assignment = [""] * len(rows)
    for indices in order:
        counts: Counter[str] = Counter()
        for index in indices:
            label, source = dimensions[index]
            counts["all"] += 1
            counts[f"label:{label}"] += 1
            counts[f"source:{label}:{source}"] += 1

        def cost(name: str) -> float:
            ratio = RATIOS[name]
            terms = (
                ((current[name][key] + value - ratio * totals[key]) ** 2
                 - (current[name][key] - ratio * totals[key]) ** 2)
                / max(ratio * totals[key], 1.0)
                for key, value in counts.items()
            )
            total = 0.0
            for term in terms:
                total += term
            return total

        chosen = min(PARTITIONS, key=lambda name: (cost(name), PARTITIONS.index(name)))
        current[chosen].update(counts)
        for index in indices:
            assignment[index] = chosen

    if any(not name for name in assignment):
        raise RuntimeError("An input row was not assigned")
    details = {
        name: {
            "rows": current[name]["all"],
            "labels": {label: current[name][f"label:{label}"] for label in LABEL_IDS},
            "primary_source_strata": {
                key.removeprefix("source:"): value
                for key, value in sorted(current[name].items())
                if key.startswith("source:")
            },
            "source_dataset_memberships": dict(sorted(Counter(
                dataset
                for index, row in enumerate(rows) if assignment[index] == name
                for dataset in {source["dataset"] for source in row["sources"]}
            ).items())),
        }
        for name in PARTITIONS
    }
    if any(min(info["labels"].values()) == 0 for info in details.values()):
        raise RuntimeError("A split has no examples of one or more labels")
    return assignment, details


def write_split(rows: list[dict], lines: list[str], assignment: list[str],
                corpus_hash: str, group_stats: dict, details: dict) -> None:
    safe_path(SPLITS)
    if SPLITS.exists():
        raise RuntimeError(f"Locked split already exists; refusing overwrite: {SPLITS}")
    with tempfile.TemporaryDirectory(prefix=".split_v5_", dir=ROOT) as temporary:
        temp = Path(temporary)
        files = {}
        for name in PARTITIONS:
            indices = [index for index, chosen in enumerate(assignment) if chosen == name]
            jsonl = temp / f"{name}.jsonl"
            ids = temp / f"{name}.ids"
            jsonl.write_text("".join(lines[index] for index in indices), encoding="utf-8")
            ids.write_text("".join(rows[index]["id"] + "\n" for index in indices), encoding="ascii")
            files[jsonl.name] = {"rows": len(indices), "sha256": sha256_file(jsonl)}
            files[ids.name] = {"rows": len(indices), "sha256": sha256_file(ids)}
        manifest = {
            "status": "frozen_local_research_split",
            "dataset_version": "5.0.0",
            "corpus_file": CORPUS.name,
            "corpus_sha256": corpus_hash,
            "corpus_manifest_sha256": sha256_file(CORPUS_MANIFEST),
            "seed": SEED,
            "ratios": RATIOS,
            "method": "deterministic greedy label-and-source-stratified assignment of text-family groups",
            "source_membership_semantics": "Count each dataset at most once per row; a multisource row contributes once to each source dataset.",
            "grouping": {
                "explicit_family": "WhatFeatures prompt_name",
                "text": "Unicode NFKC/casefold/whitespace; five-word shingles; 12 smallest stable 64-bit hashes; four 3-hash candidate bands; exact shingle Jaccard >= 0.85",
                "limits": "Approximate candidate search is not an exhaustive semantic duplicate audit; sources without native family IDs use text similarity only.",
                **group_stats,
            },
            "splits": details,
            "files": files,
            "exclusions_from_v5": 0,
            "limitations": [
                "Split uses all v5 candidate rows for local research; it does not approve source rights, row-level PromptScreen provenance, or final label policy.",
                "No independent benign FPR holdout was created outside v5.",
                "Do not fit thresholds or select models on test rows.",
            ],
        }
        (temp / "split_manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(temp, SPLITS)


def summarize_partition(rows: list[dict]) -> dict:
    labels = Counter(str(row["label"]) for row in rows)
    strata = Counter(
        f"{row['label']}:{primary_source_stratum(row)}" for row in rows
    )
    memberships = Counter(
        dataset
        for row in rows
        for dataset in {source["dataset"] for source in row["sources"]}
    )
    return {
        "rows": len(rows),
        "labels": {label: labels[label] for label in LABEL_IDS},
        "primary_source_strata": dict(sorted(strata.items())),
        "source_dataset_memberships": dict(sorted(memberships.items())),
    }


def verify_split(rows: list[dict], corpus_hash: str, groups: Groups,
                 assignment: list[str], group_stats: dict) -> bool:
    safe_path(SPLITS)
    manifest_path = safe_path(SPLITS / "split_manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["corpus_sha256"] != corpus_hash or manifest["dataset_version"] != "5.0.0":
        raise RuntimeError("Split does not match the current v5 corpus")
    if manifest["corpus_manifest_sha256"] != sha256_file(CORPUS_MANIFEST):
        raise RuntimeError("The v5 source manifest changed after the split")
    by_id = {row["id"]: row for row in rows}
    observed: dict[str, dict] = {}
    group_partition: dict[int, str] = {}
    index_by_id = {row["id"]: index for index, row in enumerate(rows)}
    observed_details: dict[str, dict] = {}
    replay_mismatches = 0
    for name in PARTITIONS:
        jsonl_path = safe_path(SPLITS / f"{name}.jsonl")
        ids_path = safe_path(SPLITS / f"{name}.ids")
        for path in (jsonl_path, ids_path):
            if sha256_file(path) != manifest["files"][path.name]["sha256"]:
                raise RuntimeError(f"Split file hash mismatch: {path.name}")
        split_rows = [json.loads(line) for line in jsonl_path.open(encoding="utf-8")]
        observed_details[name] = summarize_partition(split_rows)
        split_ids = ids_path.read_text(encoding="ascii").splitlines()
        if [row["id"] for row in split_rows] != split_ids:
            raise RuntimeError(f"ID/JSONL order mismatch: {name}")
        if len(split_rows) != manifest["files"][jsonl_path.name]["rows"]:
            raise RuntimeError(f"Split row count mismatch: {name}")
        for row in split_rows:
            row_id = row["id"]
            if row_id in observed or by_id.get(row_id) != row:
                raise RuntimeError(f"Duplicate/changed split row: {row_id}")
            observed[row_id] = row
            index = index_by_id[row_id]
            if assignment[index] != name:
                replay_mismatches += 1
            root = groups.find(index)
            prior = group_partition.setdefault(root, name)
            if prior != name:
                raise RuntimeError(f"Prompt family crosses {prior} and {name}: {row_id}")
    if len(observed) != len(rows) or set(observed) != set(by_id):
        raise RuntimeError("Split does not cover exactly the v5 corpus IDs")
    if manifest["splits"] != observed_details:
        raise RuntimeError("Stored split distribution differs from the on-disk split files")
    grouping_replay_differences = [
        key for key, value in group_stats.items()
        if manifest["grouping"].get(key) != value
    ]
    exact_replay = replay_mismatches == 0 and not grouping_replay_differences
    print(json.dumps({
        "status": "PASS" if exact_replay else "FAIL_REPLAY_DRIFT",
        "dataset_version": "5.0.0",
        "rows": len(observed),
        "splits": {name: manifest["splits"][name]["rows"] for name in PARTITIONS},
        "hashes": "PASS",
        "exact_id_coverage": "PASS",
        "text_family_disjointness": "PASS",
        "current_algorithm_replay_mismatches": replay_mismatches,
        "grouping_replay_differences": grouping_replay_differences,
    }, ensure_ascii=False, indent=2))
    return exact_replay


def main() -> None:
    global ROOT, CORPUS, CORPUS_MANIFEST, SPLITS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset-root",
        type=Path,
        required=True,
        help="Local directory containing balanced_three_label.jsonl and manifest.json",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    candidate_root = args.dataset_root.expanduser()
    if candidate_root.is_symlink() or getattr(candidate_root, "is_junction", lambda: False)():
        parser.error("Dataset directory must not be a symlink or reparse point")
    ROOT = candidate_root.resolve()
    if not ROOT.is_dir():
        parser.error(f"Dataset directory does not exist: {ROOT}")
    CORPUS = ROOT / "balanced_three_label.jsonl"
    CORPUS_MANIFEST = ROOT / "manifest.json"
    SPLITS = ROOT / "splits"
    if not CORPUS.is_file() or not CORPUS_MANIFEST.is_file():
        parser.error("Dataset directory must contain balanced_three_label.jsonl and manifest.json")
    rows, lines, corpus_hash = load_corpus()
    groups, group_stats = prompt_groups(rows)
    assignment, details = assign_groups(rows, groups)
    if args.dry_run:
        print(json.dumps({"status": "DRY_RUN", "corpus_sha256": corpus_hash,
                          "grouping": group_stats, "splits": details},
                         ensure_ascii=False, indent=2))
    elif args.apply:
        write_split(rows, lines, assignment, corpus_hash, group_stats, details)
        if not verify_split(rows, corpus_hash, groups, assignment, group_stats):
            raise SystemExit(1)
    elif not verify_split(rows, corpus_hash, groups, assignment, group_stats):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
