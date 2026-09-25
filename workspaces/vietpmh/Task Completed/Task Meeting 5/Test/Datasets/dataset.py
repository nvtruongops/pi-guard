#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATASET LOADER FOR AHSANAYUB/MALICIOUS-PROMPTS
Supports both direct HuggingFace API and local JSON cache.
"""

import os
import json
import urllib.request

DATASET_CACHE_PATH = os.path.join(os.path.dirname(__file__), "ahsanayub_malicious_prompts_sample.json")

def load_malicious_prompts_from_api(length=100, offset=0):
    url = f"https://datasets-server.huggingface.co/rows?dataset=ahsanayub%2Fmalicious-prompts&config=default&split=train&offset={offset}&length={length}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        return [r["row"] for r in data.get("rows", [])]

def get_dataset(num_samples=200):
    if os.path.exists(DATASET_CACHE_PATH):
        with open(DATASET_CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        rows = []
        for offset in range(0, num_samples, 100):
            batch = load_malicious_prompts_from_api(length=min(100, num_samples - len(rows)), offset=offset)
            rows.extend(batch)
        with open(DATASET_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        return rows

if __name__ == "__main__":
    data = get_dataset(100)
    print(f"Loaded {len(data)} samples from ahsanayub/malicious-prompts")
    print("Sample 1:", data[0]["text"][:100], "...")
