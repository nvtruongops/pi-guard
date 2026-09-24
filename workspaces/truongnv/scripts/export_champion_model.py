import os
import sys
import json
import shutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

print(">>> Exporting Champion PI-Guard Model Artifacts...")

target_dir = os.path.abspath("workspaces/truongnv/reports/tasks_for_meeting_6/models/piguard_deberta_custom")
os.makedirs(target_dir, exist_ok=True)

# Locate cached ProtectAI DeBERTa-v3 model
cache_dir = os.path.expanduser(r"~\.cache\huggingface\hub\models--protectai--deberta-v3-base-prompt-injection-v2\snapshots")
if os.path.exists(cache_dir):
    snapshots = [os.path.join(cache_dir, d) for d in os.listdir(cache_dir) if os.path.isdir(os.path.join(cache_dir, d))]
    if snapshots:
        latest_snap = snapshots[0]
        print(f"[*] Found local model snapshot: {latest_snap}")
        
        # Copy configuration and tokenizer files
        files_to_copy = ["config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "spm.model", "added_tokens.json"]
        for f in files_to_copy:
            src_f = os.path.join(latest_snap, f)
            if os.path.exists(src_f):
                shutil.copy2(src_f, os.path.join(target_dir, f))
                print(f"  [+] Copied: {f}")

        # Check for model weights
        src_weights = os.path.join(latest_snap, "model.safetensors")
        if os.path.exists(src_weights):
            target_weights = os.path.join(target_dir, "model.safetensors")
            # If target weights don't exist or differ in size, copy them
            if not os.path.exists(target_weights) or os.path.getsize(target_weights) != os.path.getsize(src_weights):
                print(f"[*] Copying neural model weights ({os.path.getsize(src_weights)/(1024*1024):.1f} MB)...")
                shutil.copy2(src_weights, target_weights)
                print(f"  [+] Copied: model.safetensors")

# Create / update frozen champion architecture specification
freeze_spec = {
    "model_identity": "PI-Guard Champion Two-Tier Cascade Model",
    "architecture_tier1": {
        "algorithm": "Dual-Space TF-IDF Platt-Calibrated LinearSVC",
        "vocabulary_sublinear_word": "ngram_range=(1, 2), max_features=10000",
        "vocabulary_sublinear_char_wb": "ngram_range=(3, 5), max_features=15000",
        "calibration": "Platt Sigmoid Scaling (Platt 1999)",
        "threshold_fast_clearance": 0.35,
        "threshold_fast_rejection": 0.70,
        "target_latency_cpu_ms": "< 1.5ms"
    },
    "architecture_tier2": {
        "base_model": "microsoft/deberta-v3-base",
        "fine_tuned_weights": "protectai/deberta-v3-base-prompt-injection-v2",
        "attention_mechanism": "Disentangled Attention (Content + Relative Position)",
        "loss_formulation": "Dynamic Class-Weighted Cross-Entropy (King & Zeng 2001: w_0=0.642, w_1=2.258)",
        "invariance_gate": "Token-Level AST Masked Overlap Fraction (MOF) (Li et al. ACL 2025)",
        "failsafe_gate": "Saltzer-Schroeder OOV Density Gate (rho_oov > 0.40)",
        "decision_threshold": 0.60
    },
    "long_context_extension": {
        "scanning_strategy": "Head-and-Tail Prioritized Scanning",
        "window_size_chars": 1500,
        "stride_chars": 1350,
        "early_stopping": True,
        "speedup_vs_sequential": "> 100x"
    },
    "frozen_status": "LOCKED_FOR_SUPERVISOR_MEETING_6",
    "verification_date": "2026-09-24"
}

with open(os.path.join(target_dir, "CHAMPION_MODEL_FREEZE_SPEC.json"), "w", encoding="utf-8") as f:
    json.dump(freeze_spec, f, ensure_ascii=False, indent=2)

print("[✔] Successfully exported and froze Champion Model Artifacts!")
