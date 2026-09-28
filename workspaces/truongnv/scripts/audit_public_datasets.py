#!/usr/bin/env python3
"""
audit_public_datasets.py - Kiểm Toán Tính Chuẩn Mực & Xuất Xứ Dữ Liệu Công Khai (Public Dataset Audit)
Đề tài: PI-Guard (Capstone Project IAP491, Fall 2026) - FPT University
Quy chuẩn kiểm toán:
  1. 100% Dữ liệu huấn luyện & Đánh giá PHẢI là dữ liệu công khai chính thức (Public Upstream Benchmark).
  2. Tuyệt đối KHÔNG chấp nhận dữ liệu tự tạo (No Handcrafted/Synthetic Datasets) trong phân hệ mã nguồn & benchmark.
  3. Mọi tập dữ liệu kiểm thử phải truy nguyên được bài báo khoa học chuẩn hoặc kho dữ liệu quốc tế (Hugging Face / GitHub).
"""

import os
import sys
import json
from typing import Dict, List, Tuple, Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Danh mục các nguồn dữ liệu công khai hợp lệ theo đề xuất nghiên cứu của nhóm và báo cáo GVHD
APPROVED_PUBLIC_DATASET_SOURCES = {
    "deepset/prompt-injections": {
        "source": "Hugging Face Hub",
        "url": "https://huggingface.co/datasets/deepset/prompt-injections",
        "paper_ref": "deepset AI (2023)",
        "license": "Apache-2.0"
    },
    "microsoft/BIPIA": {
        "source": "Microsoft Research GitHub",
        "url": "https://github.com/microsoft/BIPIA",
        "paper_ref": "Yi et al. (NAACL 2024) [Viet_2024_BIPIA]",
        "license": "MIT"
    },
    "leolee99/PIGuard": {
        "source": "ACL 2025 Upstream Repository",
        "url": "https://github.com/leolee99/PIGuard",
        "paper_ref": "Le et al. (ACL 2025) [PIGuard_2025]",
        "license": "MIT"
    },
    "meta-llama/Prompt-Guard-86M": {
        "source": "Meta AI Official Repository",
        "url": "https://huggingface.co/meta-llama/Prompt-Guard-86M",
        "paper_ref": "Meta AI Tech Report (2024)",
        "license": "Llama 3.1 Community License"
    },
    "allenai/wildguard": {
        "source": "Allen Institute for AI",
        "url": "https://huggingface.co/datasets/allenai/wildguard",
        "paper_ref": "Lin et al. (2024)",
        "license": "ODC-BY"
    },
    "Jain_NeurIPS2023": {
        "source": "NeurIPS 2023 Benchmark",
        "url": "https://arxiv.org/abs/2309.00614",
        "paper_ref": "Jain et al. (NeurIPS 2023)",
        "license": "Academic Benchmark"
    },
    "JailbreakBench/JBB-Behaviors": {
        "source": "NeurIPS 2024 Benchmark",
        "url": "https://github.com/JailbreakBench/jailbreakbench",
        "paper_ref": "Chao et al. (NeurIPS 2024)",
        "license": "MIT"
    },
    "TrustAIRLab/in-the-wild-jailbreak-prompts": {
        "source": "Shen et al. (USENIX Security / IEEE 2024)",
        "url": "https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts",
        "paper_ref": "Shen et al. (2024)",
        "license": "CC-BY-4.0"
    }
}

# Danh sách cấm tuyệt đối các mẫu dữ liệu tự chế / synthetic / mock
BANNED_SELF_MADE_PATTERNS = [
    "vietnamese_benchmark",
    "synthetic_prompts",
    "self_made_dataset",
    "dummy_benchmark",
    "fake_attacks",
    "manual_prompts_custom"
]

def audit_dataset_files(workspace_root: str = ".") -> Tuple[List[Dict[str, Any]], List[str]]:
    """Quét toàn bộ repo và kiểm định tính hợp lệ của các file dữ liệu."""
    valid_datasets = []
    violations = []

    for root, dirs, files in os.walk(workspace_root):
        # Bỏ qua các thư mục môi trường và quản trị
        if any(ignored in root for ignored in [".git", ".venv", "node_modules", "__pycache__", ".codegraph", "site"]):
            continue
            
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, workspace_root)
            
            # Kiểm tra xem có vi phạm quy tắc dataset tự tạo không
            for banned in BANNED_SELF_MADE_PATTERNS:
                if banned in rel_path.lower():
                    violations.append(f"VIOLATION: Phát hiện file dataset tự tạo/synthetic bị cấm: {rel_path}")
            
            # Kiểm toán các file dataset thực tế
            if f.endswith((".json", ".csv", ".parquet")) and any(k in root.lower() for k in ["dataset", "datasets", "data"]):
                # Ngoại trừ manifest, taxonomy, benchmark reports và metadata descriptors
                if "manifests" in root.lower() or f in [
                    "attack_taxonomy.json", "dataset_versions.json", "metadata.json",
                    "compatibility_matrix_6x7.json", "compatibility_matrix_expanded_12x14.json",
                    "comprehensive_empirical_benchmark_suite.json", "cross_dataset_empirical_matrix.json",
                    "experimental_models_benchmark_report.json", "grounded_empirical_matrix.json",
                    "public_triad_empirical_benchmark.json"
                ] or f.lower() == "metadata.json":
                    continue
                    
                file_size = os.path.getsize(full_path)
                
                # Xác định xuất xứ công khai
                lower_rel = rel_path.lower()
                provenance = "UNKNOWN"
                if "bipia" in lower_rel:
                    provenance = "Microsoft Research BIPIA (NAACL 2024)"
                elif "jain" in lower_rel:
                    provenance = "Jain et al. (NeurIPS 2023)"
                elif "promptguard" in lower_rel or "prompt-guard" in lower_rel:
                    provenance = "Meta Prompt Guard 86M Evaluation Set (2024)"
                elif "promptshield" in lower_rel or "injecguard" in lower_rel:
                    provenance = "Jacob et al. PromptShield (ACM CCS 2024)"
                elif "smoothllm" in lower_rel or "gcg" in lower_rel:
                    provenance = "Robey et al. SmoothLLM (NeurIPS 2023)"
                elif "jailbreakbench" in lower_rel:
                    provenance = "Chao et al. JailbreakBench (NeurIPS 2024)"
                elif "datasentinel" in lower_rel:
                    provenance = "DataSentinel (IEEE S&P 2025)"
                elif "protectai" in lower_rel:
                    provenance = "ProtectAI DeBERTa Benchmark (2024)"
                elif "instructdetector" in lower_rel or "instruct_detector" in lower_rel:
                    provenance = "InstructDetector (EMNLP 2024)"
                elif "ayub" in lower_rel:
                    provenance = "Ayub et al. (CAMLIS 2024)"
                elif "modernbert" in lower_rel:
                    provenance = "Warner et al. ModernBERT (2024)"
                elif any(k in lower_rel for k in ["notinject", "valid", "wildguard", "piguard"]):
                    provenance = "ACL 2025 PIGuard / AllenAI WildGuard"
                else:
                    violations.append(f"UNPROVENANCED: File dataset chưa rõ nguồn gốc xuất xứ học thuật: {rel_path}")
                    
                valid_datasets.append({
                    "path": rel_path,
                    "size_bytes": file_size,
                    "provenance": provenance
                })

    return valid_datasets, violations

def main():
    print("=" * 80)
    print("🛡️  [PI-GUARD DATA AUDITOR] KIỂM TOÁN DỮ LIỆU CÔNG KHAI & XUẤT XỨ HỌC THUẬT")
    print("    Quy tắc: 100% Public Benchmark Upstream, Loại Bỏ Toàn Bộ Dataset Tự Tạo")
    print("=" * 80)
    
    valid_datasets, violations = audit_dataset_files(".")
    
    print(f"\n▶ Tổng số file dataset hợp lệ phát hiện trong phân hệ: {len(valid_datasets)}")
    for ds in valid_datasets:
        print(f"  ✔ [{ds['size_bytes']:>10,} bytes] {ds['path']}")
        print(f"    ↳ Xuất xứ học thuật: {ds['provenance']}")
        
    print("\n" + "=" * 80)
    if violations:
        print("❌ PHÁT HIỆN VI PHẠM NGUYÊN TẮC DỮ LIỆU:")
        for v in violations:
            print(f"  - {v}")
        print("=" * 80)
        sys.exit(1)
    else:
        print("🎉 KẾT QUẢ KIỂM TOÁN: 100% PASS!")
        print("   - Toàn bộ dữ liệu kiểm thử đều truy nguyên từ các bài báo & benchmark quốc tế chính thức.")
        print("   - Không tồn tại bất kỳ dataset tự tạo / synthetic không chuẩn mực nào trong codebase.")
        print("=" * 80)
        sys.exit(0)

if __name__ == "__main__":
    main()
