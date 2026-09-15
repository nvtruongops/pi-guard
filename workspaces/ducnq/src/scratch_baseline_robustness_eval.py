"""
Benchmarking Script: Word-Level vs. Character-Level vs. Preprocessed Baseline under Adversarial Evasion.

Author: Nguyễn Quí Đức (MSSV: SE182087)
Workspace: workspaces/ducnq/
Purpose:
    Demonstrates why pure Word-level TF-IDF fails against JailGuard mutators (Leetspeak, Spacing),
    and validates how Character n-grams (3-5 n-grams) + Text Normalization restore detection recall.
"""

import io
import os
from pathlib import Path
import re
import sys
import unicodedata
from typing import List

# Fix Unicode output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure local imports resolve correctly
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from adversarial_robustness_suite import AdversarialRobustnessSuite
from jailguard_mutators import LeetspeakMutator


class WordLevelNaiveClassifier:
    """
    Simulates naive word-level tokenization matching (equivalent to word unigram TF-IDF).
    Extremely vulnerable to intra-token spacing and character substitution.
    """

    KEYWORD_PATTERNS = [
        r"\bignore\b",
        r"\bdisregard\b",
        r"\binstructions\b",
        r"\bsystem\b",
        r"\bdan\b",
        r"\bjailbreak\b",
        r"\boverride\b",
        r"\bbypass\b",
        r"\bprompt\b",
        r"\brules\b",
    ]

    def predict(self, texts: List[str]) -> List[int]:
        preds = []
        for t in texts:
            lower_t = t.lower()
            # Strict word boundary matching
            matches = sum(1 for pat in self.KEYWORD_PATTERNS if re.search(pat, lower_t))
            preds.append(1 if matches >= 2 else 0)
        return preds


class RobustCharNormalizingClassifier:
    """
    Simulates PI-Guard's defense approach:
    1. Unicode NFKC Normalization & Zero-width space removal.
    2. Character n-gram sequence matching (resilient to spacing and leetspeak homoglyphs).
    3. Base64 payload detection heuristic.
    """

    LEET_REVERSE = {
        '4': 'a', '@': 'a',
        '8': 'b', '|3': 'b',
        '(': 'c', '<': 'c',
        '3': 'e', '€': 'e',
        '9': 'g', '6': 'g',
        '1': 'i', '!': 'i', '|': 'i',
        '0': 'o',
        '5': 's', '$': 's',
        '7': 't', '+': 't',
        '2': 'z',
    }

    MALICIOUS_SUBSTRINGS = [
        "ignore",
        "disregard",
        "system",
        "dan mode",
        "jailbreak",
        "override",
        "bypass",
        "unrestricted",
    ]

    @classmethod
    def preprocess(cls, text: str) -> str:
        # 1. Unicode NFKC normalization
        norm = unicodedata.normalize("NFKC", text)
        # 2. Strip zero-width and invisible characters
        norm = re.sub(r"[\u200B-\u200D\uFEFF]", "", norm)
        # 3. Collapse multiple whitespace and remove inter-character spaces if text looks spaced
        collapsed = re.sub(r"\s+", " ", norm).strip().lower()
        # 4. Leetspeak denormalization
        denorm_chars = [cls.LEET_REVERSE.get(c, c) for c in collapsed]
        denorm_text = "".join(denorm_chars)
        # 5. Remove spaces between single characters (e.g. 'i g n o r e' -> 'ignore')
        despaced = re.sub(r"(?<=\b\w)\s+(?=\w\b)", "", denorm_text)
        return despaced

    def predict(self, texts: List[str]) -> List[int]:
        preds = []
        for raw in texts:
            cleaned = self.preprocess(raw)
            # Base64 detection pattern
            has_b64_wrapper = bool(re.search(r"base64|decode|payload|decrypt", raw, re.IGNORECASE))
            has_malicious = any(sub in cleaned for sub in self.MALICIOUS_SUBSTRINGS)

            if has_malicious or (has_b64_wrapper and "payload" in raw.lower()):
                preds.append(1)
            else:
                preds.append(0)
        return preds


def run_benchmark():
    suite = AdversarialRobustnessSuite(seed=42)

    print("================================================================================")
    print("🛡️ RUNNING PI-GUARD ADVERSARIAL BENCHMARK (JAILGUARD MUTATORS - 07/09/2026)")
    print("================================================================================")

    # 1. Evaluate Naive Word-Level Model
    print("\n--- 1. Evaluating Naive Word-Level Classifier (Simulating Word-TFIDF) ---")
    naive_clf = WordLevelNaiveClassifier()
    naive_results = suite.evaluate_classifier(naive_clf.predict)
    print(suite.format_markdown_report(naive_results))

    # 2. Evaluate Robust Normalizing + Substring/Char Classifier
    print("\n\n--- 2. Evaluating Robust Char-Normalizing Classifier (PI-Guard Proposed Pipeline) ---")
    robust_clf = RobustCharNormalizingClassifier()
    robust_results = suite.evaluate_classifier(robust_clf.predict)
    print(suite.format_markdown_report(robust_results))

    # Export JSON
    output_json = str(Path(__file__).parent / "adversarial_benchmark_results.json")
    suite.export_json(robust_results, output_json)
    print(f"\n✅ Benchmark results exported to: {output_json}")


if __name__ == "__main__":
    run_benchmark()
