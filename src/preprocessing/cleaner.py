import re
import unicodedata


class TextCleaner:
    """Standard text normalization for Prompt Injection detection."""

    @staticmethod
    def normalize(text: str) -> str:
        if not isinstance(text, str):
            return ""
        # 1. Unicode NFKC normalization (combines decomposed characters)
        text = unicodedata.normalize("NFKC", text)
        # 2. Replace multiple consecutive spaces and newlines
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        # 3. Strip leading and trailing whitespace
        return text.strip()

    @staticmethod
    def is_valid_sample(text: str, min_len: int = 3, max_len: int = 50000) -> bool:
        """Validates if text is within acceptable bounds."""
        cleaned = TextCleaner.normalize(text)
        return min_len <= len(cleaned) <= max_len
