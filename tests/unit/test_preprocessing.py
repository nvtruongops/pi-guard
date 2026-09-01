import pytest
from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.obfuscation import ObfuscationGenerator

def test_text_cleaner_normalize():
    raw_text = "  Hello   world \n\n\n\n Test  "
    cleaned = TextCleaner.normalize(raw_text)
    assert cleaned == "Hello world \n\n Test"

def test_text_cleaner_is_valid():
    assert TextCleaner.is_valid_sample("Hello world") is True
    assert TextCleaner.is_valid_sample("a", min_len=5) is False

def test_obfuscation_leetspeak():
    text = "ignore"
    leet = ObfuscationGenerator.to_leetspeak(text, p=1.0)
    assert "1" in leet or "0" in leet or "3" in leet

def test_obfuscation_base64():
    text = "disregard instructions"
    wrapped = ObfuscationGenerator.to_base64_wrapped(text)
    assert "base64" in wrapped.lower()
