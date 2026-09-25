"""
workspaces/truongnv/src/preprocessing/vietnamese_scrubber.py

Vietnamese Language Pre-scrubber & Adversarial Evasion Detector.
Handles:
1. Vietnamese diacritics unfolding (chuyển có dấu sang không dấu để quét đối sánh).
2. Teencode and leetspeak normalization (ch1 thj -> chi thi, b0 qu4 -> bo qua).
3. Code-switching injection detection (Pha trộn Anh - Việt).
4. Direct Vietnamese attack intent matching.
"""

import re
import unicodedata
from typing import Dict, Any, List, Tuple


class VietnameseScrubber:
    """Specialized pre-scrubber for Vietnamese adversarial attacks and code-switching."""

    # Vietnamese character mapping to ASCII
    VIETNAMESE_MAP = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
    }

    TEENCODE_REPLACEMENTS = [
        (r"\bch1\s*thj\b", "chi thi"),
        (r"\bb0\s*qu4\b", "bo qua"),
        (r"\bx04\b", "xoa"),
        (r"\bk0\b", "khong"),
        (r"\bdc\b", "duoc"),
        (r"\btrc\b", "truoc"),
        (r"\bng\b", "nguoi"),
        (r"\bj\b", "gi"),
    ]

    VIETNAMESE_ATTACK_PATTERNS = [
        r"(bo qua|huy bo|quen di|xoa sach)\s+(moi|tat ca|toan bo)?\s*(chi thi|huong dan|quy tac|lenh)",
        r"(tiet lo|hien thi|in ra|show|cho toi biet)\s+(prompt he thong|system prompt|chi thi goc|cau lenh ban dau)",
        r"(dong vai|hoa than vao|tro thanh)\s+(dan|ke xau|hacker|nhan vat khong bi gioi han)",
        r"(bat che do|kich hoat che do)\s+(dan|developer mode|khong kiem duyet)",
    ]

    @classmethod
    def remove_diacritics(cls, text: str) -> str:
        """Strips Vietnamese tonal marks while preserving character positions."""
        normalized = unicodedata.normalize('NFD', text)
        result = []
        for char in normalized:
            lower_c = char.lower()
            if lower_c in cls.VIETNAMESE_MAP:
                result.append(cls.VIETNAMESE_MAP[lower_c])
            elif unicodedata.category(char) != 'Mn':
                result.append(char)
        return "".join(result)

    @classmethod
    def normalize_teencode(cls, text: str) -> str:
        """Normalizes common Vietnamese teencode replacements."""
        unfolded = text.lower()
        for pattern, replacement in cls.TEENCODE_REPLACEMENTS:
            unfolded = re.sub(pattern, replacement, unfolded, flags=re.IGNORECASE)
        return unfolded

    @classmethod
    def analyze_vietnamese_attack(cls, text: str) -> Dict[str, Any]:
        """
        Analyzes whether text contains Vietnamese prompt injection or jailbreak indicators.
        Returns risk assessment and sanitized un-accented text.
        """
        no_diacritics = cls.remove_diacritics(text)
        de_teencode = cls.normalize_teencode(no_diacritics)

        matched_patterns = []
        for pat in cls.VIETNAMESE_ATTACK_PATTERNS:
            if re.search(pat, de_teencode, re.IGNORECASE):
                matched_patterns.append(pat)

        has_attack = len(matched_patterns) > 0
        risk_score = 0.92 if has_attack else 0.01

        return {
            "has_vietnamese_attack": has_attack,
            "risk_score": risk_score,
            "matched_patterns": matched_patterns,
            "unfolded_text": de_teencode
        }
