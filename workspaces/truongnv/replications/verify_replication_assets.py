#!/usr/bin/env python3
"""Read-only check of retained replication and reference data.

A passing check confirms current local file bytes and record counts only. It does
not independently prove that a file was released by its attributed upstream.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
REPLICATIONS_ROOT = WORKSPACE_ROOT / 'replications'
REFERENCES_ROOT = WORKSPACE_ROOT / 'references_study'
MOVED_PREFIXES = {
    'Tier1_Candidate_Jain_NeurIPS2023/': 'local_pilots/Tier1_Candidate_Jain_NeurIPS2023/',
    'Tier1_Candidate_InstructDetector_EMNLP2024/': 'white_box_methods/Tier1_Candidate_InstructDetector_EMNLP2024/',
    'ModernBERT_Warner_2024/': 'encoder_architectures/ModernBERT_Warner_2024/',
    'SmoothLLM_Robey_NeurIPS2023/': 'jailbreak_defenses/SmoothLLM_Robey_NeurIPS2023/',
}
MOVED_DIRECTORIES = {
    'ModernBERT_Warner_2024': 'encoder_architectures/ModernBERT_Warner_2024',
    'Tier1_Candidate_Jain_NeurIPS2023': 'local_pilots/Tier1_Candidate_Jain_NeurIPS2023',
    'Tier1_Candidate_InstructDetector_EMNLP2024': 'white_box_methods/Tier1_Candidate_InstructDetector_EMNLP2024',
    'SmoothLLM_Robey_NeurIPS2023': 'jailbreak_defenses/SmoothLLM_Robey_NeurIPS2023',
}
RETAINED = {
    'Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/train.json': (76735, '806ded8bd85782a53d34faffe4fd92b3f2e0b3b431c43578ce77faea6b9ed911'),
    'Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/valid.json': (144, 'e273fd455baac8785aa15bdc058adfd609f62ed0a3022963a5395ba95efe110e'),
    'Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/NotInject_one.json': (113, 'c77abbf3de71f99f0e12809a29d8468401285ef5353b53daa6d65131c866586c'),
    'Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/NotInject_two.json': (113, '325559cd1204fd3bdf0be82599fbf8ebbacdcd4949ae8b5bf67b399193d57c03'),
    'Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/NotInject_three.json': (113, 'bc18f3ad38ad2380e57ae96d102b884af477989e2f3ff85fbc2271ed16b8db55'),
    'Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/wildguard.json': (971, '62a0f7331af19abdb43b027b815272777aac4c311b7fad25e4150618c5289f9b'),
    'Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/BIPIA_text.json': (75, 'e828d3e9e273ddf43c4b0c91e5803998f4314555d865e32bd4e0903ab746a3b9'),
    'Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/BIPIA_code.json': (50, 'ab9f0563c7674074fb1cf82cb624196e9b5e3d62ac57b324b0745d23b7e55f87'),
    'PromptShield_Jacob_CCS2024/PromptShield/camera_ready_datasets/en_dataset_no_dups/2024-11-28_evaluation_benchmark_en.json': (23369, '8b7e18426afdb4c7219d8f1a39ccfde347bc5125efb31ce4b2fb4acb2851cc16'),
    'references_study/jailbreak_defenses/SmoothLLM_Robey_NeurIPS2023/datasets/llama2_behaviors.json': (10, 'f96d53e113bb3b839c6d0c9d4b2f3ab611e5b8fb4fd4a1cc68fb852f271cf286'),
    'references_study/jailbreak_defenses/SmoothLLM_Robey_NeurIPS2023/datasets/vicuna_behaviors.json': (10, '7396b50e123775b7d7080b2c475240401fb8e41ff1f91f9d0491663a01cb4ead'),
}
COPY_PAIRS = {
}
DERIVED_CACHE = {
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/cache/minilm_notinject.npy': (520832, '9bbb4edb13b844bfb5f8b0918835022d4fc639ee23a48387ce38ecee5115cc06'),
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/cache/minilm_valid.npy': (221312, '431adda90a91b90e9c1739213733dcf1c1b99879fcc5eef07dd9fe48659cbc9b'),
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/cache/minilm_wildguard.npy': (1491584, '8dceb1e74af29ab46679287ed35bf13fcd19ccc36e1d9540a5220696ab270cd3'),
}
WITHDRAWN = ['Tier1_Candidate_Jain_NeurIPS2023/datasets/jain_attack_samples.json', 'Tier1_Candidate_Jain_NeurIPS2023/datasets/jain_benign_samples.json', 'Tier1_Candidate_Jain_NeurIPS2023/datasets/jain_eval_benchmark.json', 'Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023/dataset/jain_attack_samples.json', 'Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023/dataset/jain_benign_samples.json', 'Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023/dataset/jain_eval_benchmark.json', 'Tier1_Candidate_Jain_NeurIPS2023/JAIN_NEURIPS2023_REPLICATION_BENCHMARK_RESULTS.json', 'Tier1_Candidate_Jain_NeurIPS2023/reports/JAIN_NEURIPS2023_REPLICATION_BENCHMARK_RESULTS.json', 'Tier1_Candidate_Jain_NeurIPS2023/reports/local_tfidf_run_2026-09-29.log', 'Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023_Replication_and_Paper_Comparison.ipynb', 'Tier1_Candidate_Jain_NeurIPS2023/figures/02_empirical_plots/jain_latency_profile.png', 'Tier1_Candidate_Jain_NeurIPS2023/figures/02_empirical_plots/jain_replication_paper_vs_local_mitigation.png', 'ProtectAI_DeBERTa_v3_v2/datasets/protectai_eval_benchmark.json', 'ProtectAI_DeBERTa_v3_v2/PROTECTAI_REPLICATION_BENCHMARK_RESULTS.json', 'ProtectAI_DeBERTa_v3_v2/reports/PROTECTAI_REPLICATION_BENCHMARK_RESULTS.json', 'DataSentinel_Liu_SP2025/datasets/datasentinel_eval_benchmark.json', 'DataSentinel_Liu_SP2025/DATASENTINEL_REPLICATION_BENCHMARK_RESULTS.json', 'DataSentinel_Liu_SP2025/reports/DATASENTINEL_REPLICATION_BENCHMARK_RESULTS.json', 'PromptShield_Jacob_CCS2024/datasets/promptshield_eval_benchmark.json', 'PromptShield_Jacob_CCS2024/PROMPTSHIELD_REPLICATION_BENCHMARK_RESULTS.json', 'PromptShield_Jacob_CCS2024/reports/PROMPTSHIELD_REPLICATION_BENCHMARK_RESULTS.json', 'Tier1_Candidate_InstructDetector_EMNLP2024/datasets/bipia_code_eval.json', 'Tier1_Candidate_InstructDetector_EMNLP2024/datasets/bipia_text_eval.json', 'Tier1_Candidate_InstructDetector_EMNLP2024/InstructDetector_EMNLP2024/dataset/bipia_code_eval.json', 'Tier1_Candidate_InstructDetector_EMNLP2024/InstructDetector_EMNLP2024/dataset/bipia_text_eval.json', 'Tier1_Candidate_InstructDetector_EMNLP2024/INSTRUCTDETECTOR_EMNLP2024_REPLICATION_BENCHMARK_RESULTS.json', 'Tier1_Candidate_InstructDetector_EMNLP2024/reports/INSTRUCTDETECTOR_EMNLP2024_REPLICATION_BENCHMARK_RESULTS.json', 'Tier1_Candidate_InstructDetector_EMNLP2024/InstructDetector_EMNLP2024_Replication_and_Paper_Comparison.ipynb', 'Tier1_Candidate_InstructDetector_EMNLP2024/figures/02_empirical_plots/instructdetector_asr_reduction.png', 'Tier1_Candidate_InstructDetector_EMNLP2024/figures/02_empirical_plots/instructdetector_replication_paper_vs_local_bars.png', 'Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf', 'SmoothLLM_Robey_NeurIPS2023/datasets/smoothllm_eval_benchmark.json', 'SmoothLLM_Robey_NeurIPS2023/SMOOTHLLM_REPLICATION_BENCHMARK_RESULTS.json', 'SmoothLLM_Robey_NeurIPS2023/reports/SMOOTHLLM_REPLICATION_BENCHMARK_RESULTS.json', 'ModernBERT_Warner_2024/datasets/modernbert_context_eval_benchmark.json', 'ModernBERT_Warner_2024/MODERNBERT_REPLICATION_BENCHMARK_RESULTS.json', 'ModernBERT_Warner_2024/reports/MODERNBERT_REPLICATION_BENCHMARK_RESULTS.json', 'Tier1_Candidate_Meta_PromptGuard2024/datasets/promptguard_3class_eval.json', 'Tier1_Candidate_Meta_PromptGuard2024/Meta_PromptGuard2024/dataset/promptguard_3class_eval.json', 'Tier1_Candidate_Meta_PromptGuard2024/META_PROMPTGUARD_REPLICATION_BENCHMARK_RESULTS.json', 'Tier1_Candidate_Meta_PromptGuard2024/reports/META_PROMPTGUARD_REPLICATION_BENCHMARK_RESULTS.json', 'Tier1_Candidate_Meta_PromptGuard2024/Meta_PromptGuard2024_Replication_and_Paper_Comparison.ipynb', 'Tier1_Candidate_Meta_PromptGuard2024/figures/02_empirical_plots/promptguard_replication_paper_vs_local_bars.png', 'Tier1_Candidate_Meta_PromptGuard2024/figures/02_empirical_plots/promptguard_latency_profile.png', 'Tier1_Candidate_Meta_PromptGuard2024/__pycache__/run_promptguard_replication.cpython-314.pyc']
WITHDRAWN += [
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/datasets/train.json',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/AYUB_CAMLIS2024_REPLICATION_BENCHMARK_RESULTS.json',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/reports/AYUB_CAMLIS2024_REPLICATION_BENCHMARK_RESULTS.json',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024_Replication_and_Paper_Comparison.ipynb',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/build_ayub_notebook.py',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/cache/minilm_notinject.npy',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/cache/minilm_valid.npy',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/cache/minilm_wildguard.npy',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/figures/02_empirical_plots/ayub_latency_profile.png',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/figures/02_empirical_plots/ayub_overdefense_fpr_comparison.png',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/figures/02_empirical_plots/ayub_replication_paper_vs_local_bars.png',
]
WITHDRAWN += [
    'ProtectAI_DeBERTa_v3_v2/datasets/notinject_sample.json',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/datasets/valid.json',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/datasets/wildguard.json',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/datasets/NotInject_one.json',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/datasets/NotInject_two.json',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/datasets/NotInject_three.json',
]
DISABLED_RUNNERS = [
    'run_all_empirical_models.py',
    'run_all_triad_experiments.py',
    'DataSentinel_Liu_SP2025/run_datasentinel_replication.py',
    'ModernBERT_Warner_2024/run_modernbert_replication.py',
    'PromptShield_Jacob_CCS2024/run_promptshield_replication.py',
    'ProtectAI_DeBERTa_v3_v2/run_protectai_replication.py',
    'Tier1_Candidate_Jain_NeurIPS2023/run_jain_replication.py',
    'Tier1_Candidate_InstructDetector_EMNLP2024/run_instructdetector_replication.py',
    'SmoothLLM_Robey_NeurIPS2023/run_smoothllm_replication.py',
    'references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/run_ayub_tier1_benchmark.py',
]
META_QUARANTINE = 'Tier1_Candidate_Meta_PromptGuard2024'

def local_path(rel):
    """Resolve a pre-move replications path to its audited current location."""
    if rel.startswith('references_study/'):
        return WORKSPACE_ROOT / rel
    for old_prefix, new_prefix in MOVED_PREFIXES.items():
        if rel.startswith(old_prefix):
            return REFERENCES_ROOT / new_prefix / rel[len(old_prefix):]
    return REPLICATIONS_ROOT / rel

def record_count(value):
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict) and "goal" in value:
        return len(value["goal"])
    if isinstance(value, dict):
        return sum(len(items) for items in value.values() if isinstance(items, list))
    return -1

def main():
    failures = []
    for old_name, new_rel in MOVED_DIRECTORIES.items():
        old_path = REPLICATIONS_ROOT / old_name
        new_path = REFERENCES_ROOT / new_rel
        if old_path.exists():
            failures.append(f"MOVED source still present: replications/{old_name}")
        if not new_path.is_dir():
            failures.append(f"MOVED destination missing: references_study/{new_rel}")
    if (REPLICATIONS_ROOT / 'cache').exists():
        failures.append("MOVED cache source still present: replications/cache")
    for rel, (expected_count, expected_hash) in RETAINED.items():
        path = local_path(rel)
        if not path.is_file():
            failures.append(f"MISSING retained file: {rel}")
            continue
        data = path.read_bytes()
        try:
            count = record_count(json.loads(data))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            failures.append(f"INVALID JSON: {rel}: {exc}")
            continue
        digest = hashlib.sha256(data).hexdigest()
        if count != expected_count:
            failures.append(f"COUNT mismatch: {rel}: got {count}, expected {expected_count}")
        if digest != expected_hash:
            failures.append(f"SHA-256 mismatch: {rel}: got {digest}, expected {expected_hash}")
        if count == expected_count and digest == expected_hash:
            print(f"OK {count:>6} records  {rel}")
    for copy_rel, canonical_rel in COPY_PAIRS.items():
        copy_path = local_path(copy_rel)
        canonical_path = local_path(canonical_rel)
        if not copy_path.is_file() or not canonical_path.is_file():
            failures.append(f"MISSING source-copy pair: {copy_rel} / {canonical_rel}")
            continue
        if copy_path.read_bytes() != canonical_path.read_bytes():
            failures.append(f"BYTE mismatch in source-copy pair: {copy_rel} / {canonical_rel}")
        else:
            print(f"OK exact local copy  {copy_rel}")
    for rel in WITHDRAWN:
        if local_path(rel).exists():
            failures.append(f"WITHDRAWN file is present: {rel}")
    for rel in DISABLED_RUNNERS:
        path = local_path(rel)
        if not path.is_file() or "raise SystemExit(" not in path.read_text(encoding="utf-8"):
            failures.append(f"Legacy runner is not fail-closed: {rel}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    meta_path = REPLICATIONS_ROOT / META_QUARANTINE
    meta_state = 'present and quarantined' if meta_path.exists() else 'absent'
    print(f"PASS: {len(MOVED_DIRECTORIES)} moved reference folders verified; {len(RETAINED)} retained data files hashed; {len(COPY_PAIRS)} cross-package copies retained; {len(WITHDRAWN)} withdrawn paths absent; {len(DISABLED_RUNNERS)} legacy entry points disabled; Meta folder {meta_state}.")
    print("This checks local integrity and cleanup state; it does not independently prove upstream authorship or paper fidelity.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
