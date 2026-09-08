## Checkkk
 RQ1 — GENERALIZATION & DATA INTEGRITY
"To what extent does group-aware data splitting mitigate benchmark optimism and reveal the true out-of-distribution (OOD) generalization of guardrail classifiers?"

Hypothesis ($H_1$): Standard random splitting induces data leakage due to semantically redundant prompt templates, artificially inflating test metrics. Group-aware splitting exposes genuine OOD performance degradation.
Evaluation Protocol:
Compare Random Split vs. Group-Aware / Cluster-based Split.
Evaluate on unseen attack families (OOD test set).
Metrics: Macro-$F_1$, Precision, Recall, and Generalization Gap ($\Delta F_1 = F_1^{\text{Random}} - F_1^{\text{Group}}$).
🔹 RQ2 — DEFENSE EFFECTIVENESS (THE LAYERED HYPOTHESIS)
"Does a multi-layer defense architecture provide superior robustness against diverse prompt injection and jailbreak attacks compared to individual single-layer mechanisms?"

Hypothesis ($H_2$): A multi-layer architecture (combining syntax normalization, character-level baseline, and semantic transformer) yields lower Attack Success Rate ($ASR$) and higher detection recall than any single-layer baseline alone across both direct and obfuscated perturbations.
Evaluation Protocol:
Compare Single-Layer (e.g., Only Regex, Only TF-IDF, or Only DeBERTa) vs. Multi-Layer (PI-Guard).
Attack Spectrum Breakdown:
Direct Attacks (Standard Injections & Persona Jailbreaks).
Obfuscated Attacks (Leetspeak, Inter-token Spacing via JailGuard).
Encoded Attacks (Base64 Smuggling).
Metrics: Attack Success Rate ($ASR \downarrow$), Recall / TPR ($\uparrow$), False Positive Rate ($FPR \downarrow$).
🔹 RQ3 — DEPLOYMENT PRACTICALITY & PERFORMANCE TRADE-OFF
"Can the proposed guardrail satisfy the operational triad of low evasion rate, negligible benign over-defense, and low-latency inference for inline deployment?"

Hypothesis ($H_3$): The proposed guardrail can simultaneously maintain strong defensive capabilities and sub-30ms P95 latency on commodity multi-core CPU hardware without requiring expensive GPU infrastructure.
Operational Invariants (Target Criteria):
Security (Evasion Bound): $ASR_{guardrail} < 5.0%$ (Recall $> 95.0%$).
Usability (Over-defense Bound): $FPR < 1.5%$ on clean & noisy benign prompts.
Inference Latency (Runtime): $P_{95} \text{ latency} < 30\text{ ms}$ on standard multi-core CPU.