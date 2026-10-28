"""Aggregate-only qualification audit of Anthropic's human red-team attempts.

Reads the pinned red-team-attempts file and train/validation text only to count
single-turn English candidate prompts, privacy indicators, exact duplicates,
family coverage, and overlap. It never writes row text, IDs, or row hashes.
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from statistics import median
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
SOURCE_FILE = TRAINING / "datasets" / "source_audit" / "anthropic_hh_rlhf_round19" / "red_team_attempts.jsonl.gz"
ROUND07 = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
ROUND18 = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_l2_source_heldout_round18_r01"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
REPORT = ROOT / "anthropic_redteam_candidate_audit_round19.json"

REPOSITORY = "Anthropic/hh-rlhf"
REVISION = "09be8c5bbc57cb3887f3a9732ad6aa7ec602a1fa"
EXPECTED_FILE_SHA256 = "4c7b0069991460f0064f279fd400b51f3f0095697d14d7793c49b0925f80814f"
LANGUAGE_MODEL_SHA256 = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
LANGUAGE_THRESHOLD = 0.95

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "private_key": re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)"),
}
SPEAKER_RE = re.compile(r"(?m)^(Human|Assistant):[ \t]*")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def human_turns(transcript: str) -> list[str]:
    markers = list(SPEAKER_RE.finditer(transcript))
    turns: list[str] = []
    for index, marker in enumerate(markers):
        if marker.group(1) != "Human":
            continue
        end = markers[index + 1].start() if index + 1 < len(markers) else len(transcript)
        value = transcript[marker.end():end].strip()
        if value:
            turns.append(value)
    return turns


def language_identifier():
    sys.path.insert(0, str(VENDOR))
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    import py3langid

    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    if sha256_file(model_path) != LANGUAGE_MODEL_SHA256:
        raise ValueError("PINNED_LANGUAGE_MODEL_HASH_MISMATCH")
    return LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)


def package_texts(package: Path, expected_package_id: str) -> tuple[set[str], str]:
    manifest_path = package / "DATASET_MANIFEST.json"
    raw_manifest = manifest_path.read_bytes()
    manifest = json.loads(raw_manifest)
    if manifest.get("package_id") != expected_package_id:
        raise ValueError("UNEXPECTED_PACKAGE_ID:" + expected_package_id)
    texts: set[str] = set()
    for split in ("train", "validation"):
        spec = manifest["partitions"][split]["rows"]
        path = package / spec["path"]
        if sha256_file(path) != spec["sha256"]:
            raise ValueError("PACKAGE_PARTITION_HASH_MISMATCH:" + split)
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                text = normalized(row.get("text", ""))
                if text:
                    texts.add(text)
    return texts, sha256_bytes(raw_manifest)


def main() -> int:
    if sha256_file(SOURCE_FILE) != EXPECTED_FILE_SHA256:
        raise ValueError("PINNED_ANTHROPIC_FILE_HASH_MISMATCH")
    known_texts, round07_manifest_sha = package_texts(
        ROUND07, "pi_guard_l2_native_reference_round07_r01"
    )
    round18_texts, round18_manifest_sha = package_texts(
        ROUND18, "pi_guard_l2_source_heldout_round18_r01"
    )
    known_texts |= round18_texts
    identifier = language_identifier()

    counters: collections.Counter[str] = collections.Counter()
    privacy: collections.Counter[str] = collections.Counter()
    language_counts: collections.Counter[str] = collections.Counter()
    rating_counts: collections.Counter[str] = collections.Counter()
    duplicate_counts: collections.Counter[str] = collections.Counter()

    with gzip.open(SOURCE_FILE, "rt", encoding="utf-8") as stream:
        rows: list[dict[str, Any]] = json.load(stream)
    for item in rows:
        counters["source_rows"] += 1
        transcript = item.get("transcript")
        if not isinstance(transcript, str):
            counters["missing_transcript"] += 1
            continue
        turns = human_turns(transcript)
        counters["parsed_human_turns_total"] += len(turns)
        if len(turns) != 1:
            counters["not_single_turn_transcript"] += 1
            continue
        counters["single_turn_transcript"] += 1
        text = turns[0]
        if not text.strip():
            counters["empty_single_turn_prompt"] += 1
            continue

        matched = [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]
        if matched:
            counters["single_turn_privacy_pattern_match"] += 1
            for name in matched:
                privacy[name] += 1
            continue
        counters["single_turn_without_privacy_pattern"] += 1

        language, confidence = identifier.classify(text)
        if language != "en" or float(confidence) < LANGUAGE_THRESHOLD:
            counters["single_turn_non_english_or_uncertain"] += 1
            language_counts[language if float(confidence) >= LANGUAGE_THRESHOLD else "below_threshold_or_uncertain"] += 1
            continue
        counters["single_turn_english_confident"] += 1
        language_counts["en_confident"] += 1

        key = normalized(text)
        duplicate_counts[key] += 1
        if key in known_texts:
            counters["exact_overlap_with_round07_or_round18"] += 1

        rating = item.get("rating")
        rating_counts[str(rating) if rating is not None else "missing"] += 1
        member = item.get("red_team_member_id")
        if member is None or str(member).strip() == "":
            counters["single_turn_missing_red_team_member_id"] += 1
            continue
        counters["single_turn_english_private_screened_with_family_id"] += 1

    duplicate_groups = {key for key, count in duplicate_counts.items() if count > 1}
    duplicate_rows_after_first = sum(count - 1 for count in duplicate_counts.values() if count > 1)
    # Retain one member of each exact prompt group; if a duplicate crosses
    # red-team members, exclude the group because its family assignment is ambiguous.
    representative_families: dict[str, set[str]] = collections.defaultdict(set)
    # A second pass assigns eligible exact-text keys to private member groups.
    for item in rows:
        transcript = item.get("transcript")
        member = item.get("red_team_member_id")
        if not isinstance(transcript, str) or member is None:
            continue
        turns = human_turns(transcript)
        if len(turns) != 1:
            continue
        text = turns[0]
        if any(pattern.search(text) for pattern in PII_PATTERNS.values()):
            continue
        language, confidence = identifier.classify(text)
        if language != "en" or float(confidence) < LANGUAGE_THRESHOLD:
            continue
        key = normalized(text)
        if key in duplicate_counts and key not in known_texts:
            representative_families[key].add(str(member))
    del rows
    ambiguous_duplicate_groups = sum(1 for members in representative_families.values() if len(members) > 1)
    accepted_keys = {
        key for key, members in representative_families.items()
        if len(members) == 1 and duplicate_counts[key] == 1
    }
    accepted_family_sizes: collections.Counter[str] = collections.Counter()
    for key in accepted_keys:
        accepted_family_sizes[next(iter(representative_families[key]))] += 1

    counts = sorted(accepted_family_sizes.values())
    family_size_summary = {
        "min": min(counts) if counts else 0,
        "median": median(counts) if counts else 0,
        "p95": counts[min(len(counts) - 1, int(0.95 * len(counts)))] if counts else 0,
        "max": max(counts) if counts else 0,
    }
    result = {
        "audit_round": 19,
        "repository": REPOSITORY,
        "revision": REVISION,
        "source_file": "red-team-attempts/red_team_attempts.jsonl.gz",
        "source_file_sha256": EXPECTED_FILE_SHA256,
        "source_file_bytes": SOURCE_FILE.stat().st_size,
        "source_license_declared": "MIT",
        "aggregate_counters": dict(sorted(counters.items())),
        "english_confidence_threshold": LANGUAGE_THRESHOLD,
        "language_model_sha256": LANGUAGE_MODEL_SHA256,
        "language_counts_after_privacy_screen": dict(sorted(language_counts.items())),
        "privacy_pattern_counts_on_single_turn_human_input": dict(sorted(privacy.items())),
        "exact_duplicate_groups_before_exclusion": len(duplicate_groups),
        "exact_duplicate_rows_after_first_before_exclusion": duplicate_rows_after_first,
        "cross_member_duplicate_groups_excluded": ambiguous_duplicate_groups,
        "rating_counts_not_used_as_input_label": dict(sorted(rating_counts.items())),
        "eligible_unique_single_turn_english_private_screened_rows": len(accepted_keys),
        "eligible_red_team_member_families": len(accepted_family_sizes),
        "eligible_family_size_summary": family_size_summary,
        "round07_manifest_sha256": round07_manifest_sha,
        "round18_manifest_sha256": round18_manifest_sha,
        "input_unit": "one human-authored first/only utterance from a one-human-turn transcript; assistant replies excluded",
        "candidate_mapping": "red-team-attempt transcript to provisional JB-attempt reference; attempt only, not success or PI-Guard gold",
        "candidate_mapping_limit": "The source task is to red-team a model for harmful outputs but does not provide a PI-Guard jailbreak taxonomy. Keep harmful-request-only or ambiguous examples out unless the project mapping explicitly accepts the source task as JB-attempt evidence.",
        "privacy_limit": "Anthropic reports regex filtering and manual review for possible generated PII; this audit adds pattern checks on input turns only and is not full privacy clearance.",
        "split_limit": "No source-publisher train/validation split is supplied. Red-team-member grouping supports internal family holdout only; this collection may be train-only if an external validation cohort remains sealed by source.",
        "row_text_ids_or_hashes_emitted": False,
        "test_files_requested_or_opened": False,
        "pi_guard_test_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "package_admitted": False,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "aggregate_counters", "language_counts_after_privacy_screen",
        "privacy_pattern_counts_on_single_turn_human_input", "exact_duplicate_groups_before_exclusion",
        "exact_duplicate_rows_after_first_before_exclusion", "cross_member_duplicate_groups_excluded",
        "eligible_unique_single_turn_english_private_screened_rows", "eligible_red_team_member_families",
        "eligible_family_size_summary", "rating_counts_not_used_as_input_label",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
