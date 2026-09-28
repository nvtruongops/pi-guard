#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrate_to_references_study.py
------------------------------
Di chuyển có kiểm soát các thành phần nghiên cứu tham khảo ra khỏi replications/:
1. JailbreakBench_Chao_NeurIPS2024 -> references_study/harnesses/JailbreakBench_Chao_NeurIPS2024
2. Tier1_REJECTED_Ayub_CAMLIS2024 -> references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024
3. Chuẩn hóa runner run_piguard_replication.py cho Paper_ACL2025_PIGuard_HaoLi
"""

import os
import sys
import shutil
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path("d:/Work/Do-an/workspaces/truongnv")
REPLICATIONS_DIR = WORKSPACE_ROOT / "replications"
STUDY_DIR = WORKSPACE_ROOT / "references_study"
HARNESS_DIR = STUDY_DIR / "harnesses"
REJECTED_DIR = STUDY_DIR / "rejected_baselines"

HARNESS_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)

# 1. Di chuyển JailbreakBench
src_jbb = REPLICATIONS_DIR / "JailbreakBench_Chao_NeurIPS2024"
dst_jbb = HARNESS_DIR / "JailbreakBench_Chao_NeurIPS2024"
if src_jbb.exists() and not dst_jbb.exists():
    print(f"[*] Moving {src_jbb.name} -> {dst_jbb}")
    shutil.move(str(src_jbb), str(dst_jbb))
elif dst_jbb.exists():
    print(f"[+] {dst_jbb} already exists.")

# 2. Di chuyển Ayub Rejected
src_ayub = REPLICATIONS_DIR / "Tier1_REJECTED_Ayub_CAMLIS2024"
dst_ayub = REJECTED_DIR / "Tier1_REJECTED_Ayub_CAMLIS2024"
if src_ayub.exists() and not dst_ayub.exists():
    print(f"[*] Moving {src_ayub.name} -> {dst_ayub}")
    shutil.move(str(src_ayub), str(dst_ayub))
elif dst_ayub.exists():
    print(f"[+] {dst_ayub} already exists.")

# 3. Chuẩn hóa runner cho Paper_ACL2025_PIGuard_HaoLi
piguard_dir = REPLICATIONS_DIR / "Paper_ACL2025_PIGuard_HaoLi"
if piguard_dir.exists():
    runner_dst = piguard_dir / "run_piguard_replication.py"
    eval_src = piguard_dir / "eval_piguard_replication.py"
    if eval_src.exists() and not runner_dst.exists():
        print(f"[*] Creating runner alias {runner_dst.name} -> {eval_src.name}")
        shutil.copy2(str(eval_src), str(runner_dst))

print("[✔] Migration finished successfully!")
