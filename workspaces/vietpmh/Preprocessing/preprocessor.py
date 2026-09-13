#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workspaces/vietpmh/Preprocessing/preprocessor.py
------------------------------------------------
Module Tiền Xử Lý & Khử Nhiễu Đối Kháng Nâng Cao (Advanced Multi-Codec Preprocessor)
Kiến trúc: Configurable Feature Flags & Defense-in-Depth Pipeline
Phân hệ: Transformer & Evasion Defense (Phạm Minh Hoàng Việt - SE181851)
Đề tài: PI-Guard (FPT University IAP491 Capstone Project)

Căn cứ khoa học:
- Unicode NFKC: ISO/IEC 10646 & NIST AI 100-2e2025
- Invisible / Zero-Width Stripping: Boucher et al. (IEEE S&P 2022) & Jain et al. (NeurIPS 2023)
- Multi-Codec De-obfuscation (Base64, Hex, ROT13, URL): Yuan et al. (ICLR 2024 - CipherChat)
- Shannon Entropy Whitelisting: Shannon (1948) & OWASP LLM01 Mitigation
- Sliding Window Chunking: Beltagy et al. (2020) & He et al. (ICLR 2023 - DeBERTaV3)
"""

import base64
import codecs
import math
import re
import unicodedata
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple, Union


class PromptPreprocessor:
    """
    Bộ tiền xử lý đầu vào đa năng bảo toàn ngữ nghĩa với kiến trúc Feature Flags linh hoạt.
    Hỗ trợ 2 chế độ chính:
    - Fast Mode (Siêu tốc < 0.5ms): Chỉ chạy Unicode, Zero-width và Base64 cơ bản.
    - Hardened Mode (Phòng thủ thép): Bật toàn bộ Multi-Codec (Hex, URL, ROT13, Binary), 
      Universal Delimiters, Entropy Whitelisting và Sliding Window Chunking.
    """

    def __init__(
        self,
        model_name_or_path: str = "microsoft/deberta-v3-base",
        max_length: int = 512,
        stride: int = 256,
        # --- Configurable Feature Flags ---
        enable_unicode_normalization: bool = True,
        enable_invisible_stripping: bool = True,
        enable_delimiter_normalization: bool = True,
        enable_base64_decoding: bool = True,
        enable_multi_codec: bool = True,
        enable_entropy_check: bool = True,
        enable_sliding_window: bool = True,
        tokenizer: Optional[Any] = None
    ) -> None:
        """
        Khởi tạo preprocessor với các cờ tính năng (Feature Flags).
        """
        self.model_name_or_path = model_name_or_path
        self.max_length = max_length
        self.stride = stride

        # Feature Flags
        self.enable_unicode_normalization = enable_unicode_normalization
        self.enable_invisible_stripping = enable_invisible_stripping
        self.enable_delimiter_normalization = enable_delimiter_normalization
        self.enable_base64_decoding = enable_base64_decoding
        self.enable_multi_codec = enable_multi_codec
        self.enable_entropy_check = enable_entropy_check
        self.enable_sliding_window = enable_sliding_window

        self._tokenizer = tokenizer

        # --- TẬP MẪU REGEX KHỬ NHIỄU ---
        # 1. Ký tự điều khiển ẩn Unicode thực tế (Boucher et al., IEEE S&P 2022)
        self.raw_invisible_pattern = re.compile(
            r"[\u200B-\u200F\u2028-\u202F\u2060-\u206F\uFEFF\u00AD\u0080-\u009F]"
        )

        # 2. Chuỗi ký tự thoát dạng văn bản ("\\u200B", "\\uFEFF")
        self.escaped_invisible_pattern = re.compile(
            r"\\u(?:200[b-fB-F]|202[8-9a-fA-F]|206[0-9a-fA-F]|[fF][eE][fF][fF]|00[aA][dD]|00[89][0-9a-fA-F])",
            re.IGNORECASE
        )

        # 3. Phân mảnh từ nâng cao bởi các dấu phân cách: khoảng trắng, _, -, ., /
        self.delimited_word_pattern = re.compile(
            r"(^|[\s\(\[\{])((?:[\w\u00C0-\u1EF9][\s_\-\.\/]){2,}[\w\u00C0-\u1EF9])(?=[\s\)\]\},!\?]|$)",
            re.UNICODE
        )

        # 4. Base64 RFC 4648 Pattern (độ dài >= 16)
        self.base64_pattern = re.compile(
            r"(?:(?<=\s)|(?<=^))(?:[A-Za-z0-9+/]{4}){3,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})(?=(?:\s|$|[.,!?;]))"
        )

        # 5. Hexadecimal Escaped Pattern: \x49\x67... hoặc 0x49 0x67... (khớp chuỗi hex liên tục)
        self.hex_escaped_pattern = re.compile(
            r"(?:\\x[0-9a-fA-F]{2}[\s]*){3,}|(?:0x[0-9a-fA-F]{2}[\s,]+){2,}0x[0-9a-fA-F]{2}"
        )

        # 6. URL Percent-Encoding Pattern: %49%67%6e%6f%72%65
        self.url_encoded_pattern = re.compile(
            r"(?:%[0-9a-fA-F]{2}(?:%[0-9a-fA-F]{2}|[\s\w])*){3,}"
        )

        # 7. Binary String Pattern: 01001001 01100111... (8-bit bytes)
        self.binary_pattern = re.compile(
            r"\b(?:[01]{8}[\s,]+){2,}[01]{8}\b"
        )

        # Từ điển từ khóa chỉ thị phổ biến để kiểm chứng giải mã ROT13/Caesar
        self.rot13_target_keywords = {
            "ignore", "system", "prompt", "instructions", "bypass", "jailbreak",
            "assistant", "rules", "password", "override", "dan", "developer"
        }

    @property
    def tokenizer(self):
        """Lazy loading tokenizer khi cần mã hóa tensor"""
        if self._tokenizer is None:
            try:
                from transformers import AutoTokenizer
                self._tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
            except Exception as e:
                raise RuntimeError(
                    f"Không thể tải tokenizer '{self.model_name_or_path}'. "
                    f"Vui lòng cài đặt 'transformers' và 'torch' hoặc truyền tokenizer trực tiếp. Chi tiết: {e}"
                )
        return self._tokenizer

    # =========================================================================
    # 1. THUẬT TOÁN ĐO ĐỘ HỖN LOẠN (SHANNON ENTROPY)
    # =========================================================================
    @staticmethod
    def calculate_entropy(text: str) -> float:
        """
        Tính toán Shannon Entropy của chuỗi ký tự:
        H(X) = - sum(P(x) * log2(P(x)))
        """
        if not text:
            return 0.0
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = -sum(p * math.log2(p) for p in prob)
        return entropy

    # =========================================================================
    # 2. CÁC HÀM TIỀN XỬ LÝ & CHUẨN HÓA CỐT LÕI
    # =========================================================================
    def normalize_unicode(self, text: str) -> str:
        """Chuẩn hóa Unicode theo chuẩn NFKC (ISO/IEC 10646 & NIST AI 100-2e2025)."""
        if not text or not self.enable_unicode_normalization:
            return text
        return unicodedata.normalize("NFKC", text)

    def strip_invisible_characters(self, text: str) -> str:
        """Loại bỏ ký tự tàng hình và mã điều khiển hướng văn bản (IEEE S&P 2022)."""
        if not text or not self.enable_invisible_stripping:
            return text
        text = self.raw_invisible_pattern.sub("", text)
        text = self.escaped_invisible_pattern.sub("", text)
        return text

    def normalize_delimiters(self, text: str) -> str:
        """
        Nhận diện và gộp các từ bị băm bởi khoảng trắng, gạch dưới, gạch ngang, chấm, gạch chéo.
        Ví dụ: "i_g_n_o_r_e", "i-g-n-o-r-e", "i.g.n.o.r.e", "x i n   c h à o".
        """
        if not text or not self.enable_delimiter_normalization:
            return text

        def collapse_delimiters(match: re.Match) -> str:
            prefix = match.group(1)
            matched_str = match.group(2)
            if re.match(r"^\d+[\.\-\/]\d+", matched_str):
                return prefix + matched_str
            collapsed = re.sub(r"[\s_\-\.\/]+", "", matched_str)
            return prefix + collapsed

        return self.delimited_word_pattern.sub(collapse_delimiters, text)

    # =========================================================================
    # 3. BỘ GIẢI MÃ ĐA MÃ HÓA CÓ ĐIỀU KIỆN AN TOÀN (MULTI-CODEC DE-OBFUSCATION)
    # =========================================================================
    def safe_base64_deobfuscate(self, text: str) -> Tuple[str, bool]:
        """Giải mã Base64 có kiểm định 3 lớp an toàn và Shannon Entropy check."""
        if not text or not self.enable_base64_decoding:
            return text, False

        detected = False

        def decode_callback(match: re.Match) -> str:
            nonlocal detected
            candidate = match.group(0).strip()
            try:
                decoded_bytes = base64.b64decode(candidate, validate=True)
                decoded_text = decoded_bytes.decode("utf-8", errors="strict")
                
                printable_count = sum(1 for c in decoded_text if c.isprintable() or c in "\r\n\t ")
                is_printable = len(decoded_text) >= 4 and (printable_count / len(decoded_text)) >= 0.90
                
                entropy_ok = True
                if self.enable_entropy_check:
                    ent = self.calculate_entropy(decoded_text)
                    entropy_ok = (ent < 5.2)

                if is_printable and entropy_ok:
                    detected = True
                    return f"{candidate} [DECODED_BASE64: {decoded_text.strip()}]"
            except Exception:
                pass
            return candidate

        cleaned = self.base64_pattern.sub(decode_callback, text)
        return cleaned, detected

    def safe_hex_deobfuscate(self, text: str) -> Tuple[str, bool]:
        """Giải mã chuỗi Hex (ví dụ: \\x49\\x67\\x6e\\x6f\\x72\\x65 hoặc 0x49 0x67...)."""
        if not text or not self.enable_multi_codec:
            return text, False

        detected = False

        def decode_callback(match: re.Match) -> str:
            nonlocal detected
            candidate = match.group(0).strip()
            try:
                hex_digits = re.sub(r"[\\x0\s,]", "", candidate)
                decoded_bytes = bytes.fromhex(hex_digits)
                decoded_text = decoded_bytes.decode("utf-8", errors="strict")
                
                printable_count = sum(1 for c in decoded_text if c.isprintable() or c in "\r\n\t ")
                if len(decoded_text) >= 3 and (printable_count / len(decoded_text)) >= 0.85:
                    detected = True
                    return f"{candidate} [DECODED_HEX: {decoded_text.strip()}]"
            except Exception:
                pass
            return candidate

        cleaned = self.hex_escaped_pattern.sub(decode_callback, text)
        return cleaned, detected

    def safe_url_deobfuscate(self, text: str) -> Tuple[str, bool]:
        """Giải mã URL Percent-Encoding (ví dụ: %49%67%6e%6f%72%65%20rules)."""
        if not text or not self.enable_multi_codec:
            return text, False

        detected = False

        def decode_callback(match: re.Match) -> str:
            nonlocal detected
            candidate = match.group(0).strip()
            try:
                decoded_text = urllib.parse.unquote(candidate)
                if decoded_text != candidate and all(c.isprintable() or c in "\r\n\t " for c in decoded_text):
                    detected = True
                    return f"{candidate} [DECODED_URL: {decoded_text.strip()}]"
            except Exception:
                pass
            return candidate

        cleaned = self.url_encoded_pattern.sub(decode_callback, text)
        return cleaned, detected

    def safe_rot13_deobfuscate(self, text: str) -> Tuple[str, bool]:
        """
        Nhận diện và giải mã ROT13 / Caesar Cipher (Yuan et al., ICLR 2024).
        Chỉ kích hoạt khi sau giải mã xuất hiện các từ khóa chỉ thị hệ thống mục tiêu.
        """
        if not text or not self.enable_multi_codec or len(text) < 10:
            return text, False

        try:
            rot13_decoded = codecs.decode(text, "rot_13")
            words_in_decoded = set(re.findall(r"\b[A-Za-z]{3,}\b", rot13_decoded.lower()))
            
            hit_keywords = words_in_decoded.intersection(self.rot13_target_keywords)
            if len(hit_keywords) >= 2:
                return f"{text} [DECODED_ROT13: {rot13_decoded.strip()}]", True
        except Exception:
            pass

        return text, False

    def safe_binary_deobfuscate(self, text: str) -> Tuple[str, bool]:
        """Giải mã chuỗi nhị phân 8-bit (ví dụ: 01001001 01100111...)."""
        if not text or not self.enable_multi_codec:
            return text, False

        detected = False

        def decode_callback(match: re.Match) -> str:
            nonlocal detected
            candidate = match.group(0).strip()
            try:
                bits_list = re.findall(r"[01]{8}", candidate)
                chars = [chr(int(b, 2)) for b in bits_list]
                decoded_text = "".join(chars)
                if all(32 <= ord(c) <= 126 for c in decoded_text):
                    detected = True
                    return f"{candidate} [DECODED_BINARY: {decoded_text.strip()}]"
            except Exception:
                pass
            return candidate

        cleaned = self.binary_pattern.sub(decode_callback, text)
        return cleaned, detected

    # =========================================================================
    # 4. SLIDING WINDOW CHUNKING (CHỐNG TRUNCATION > 512 TOKENS)
    # =========================================================================
    def get_sliding_windows(self, text: str) -> List[str]:
        """
        Chia nhỏ văn bản dài thành các cửa sổ con có độ đè lấn (Overlapping Windows).
        """
        words = text.split()
        window_size_words = int(self.max_length * 0.7)
        stride_words = int(self.stride * 0.7)

        if len(words) <= window_size_words:
            return [text]

        windows = []
        for i in range(0, len(words), stride_words):
            chunk = " ".join(words[i:i + window_size_words])
            if chunk:
                windows.append(chunk)
            if i + window_size_words >= len(words):
                break
        return windows

    # =========================================================================
    # 5. QUY TRÌNH TỔNG HỢP (PIPELINE EXECUTION)
    # =========================================================================
    def clean(self, raw_prompt: str) -> Dict[str, Any]:
        """
        Thực thi toàn bộ quy trình tiền xử lý theo cấu hình Feature Flags.
        """
        if not isinstance(raw_prompt, str):
            raw_prompt = str(raw_prompt)

        text = raw_prompt
        codec_hits = []

        # 1. Unicode Normalization
        text = self.normalize_unicode(text)

        # 2. Invisible Stripping
        text = self.strip_invisible_characters(text)

        # 3. Delimiter Normalization
        text = self.normalize_delimiters(text)

        # 4. Multi-Codec De-obfuscation
        text, has_b64 = self.safe_base64_deobfuscate(text)
        if has_b64:
            codec_hits.append("Base64")

        text, has_hex = self.safe_hex_deobfuscate(text)
        if has_hex:
            codec_hits.append("Hexadecimal")

        text, has_url = self.safe_url_deobfuscate(text)
        if has_url:
            codec_hits.append("URL-Encoding")

        text, has_bin = self.safe_binary_deobfuscate(text)
        if has_bin:
            codec_hits.append("Binary")

        text, has_rot13 = self.safe_rot13_deobfuscate(text)
        if has_rot13:
            codec_hits.append("ROT13-Cipher")

        # 5. Whitespace Compaction
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n", "\n\n", text).strip()

        # Sliding window check
        windows = self.get_sliding_windows(text) if self.enable_sliding_window else [text]

        return {
            "original_prompt": raw_prompt,
            "cleaned_prompt": text,
            "detected_codecs": codec_hits,
            "has_encoded_payload": (len(codec_hits) > 0),
            "is_altered": (text != raw_prompt.strip()),
            "num_windows": len(windows),
            "windows": windows
        }

    def encode(
        self,
        raw_prompt: Union[str, List[str]],
        return_tensors: str = "pt",
        use_sliding_window: bool = False
    ) -> Dict[str, Any]:
        """
        Mã hóa chuỗi sang PyTorch Tensors (input_ids, attention_mask).
        """
        if isinstance(raw_prompt, str):
            prompts = [raw_prompt]
            single_input = True
        else:
            prompts = raw_prompt
            single_input = False

        cleaned_records = [self.clean(p) for p in prompts]
        
        if use_sliding_window and single_input and cleaned_records[0]["num_windows"] > 1:
            target_texts = cleaned_records[0]["windows"]
        else:
            target_texts = [r["cleaned_prompt"] for r in cleaned_records]

        encoded_outputs = self.tokenizer(
            target_texts,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors=return_tensors
        )

        result: Dict[str, Any] = {
            "input_ids": encoded_outputs["input_ids"],
            "attention_mask": encoded_outputs["attention_mask"],
            "cleaned_texts": target_texts if not single_input or use_sliding_window else target_texts[0],
            "metadata": cleaned_records if not single_input else cleaned_records[0]
        }

        if "token_type_ids" in encoded_outputs:
            result["token_type_ids"] = encoded_outputs["token_type_ids"]

        return result
