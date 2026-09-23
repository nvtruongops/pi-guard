# DATASET CARD: PI-Guard Tier-1 Fast-Filter Evaluation Benchmark

## 1. Overview & Provenance
- **Dataset Name**: PI-Guard Tier-1 Fast-Filter Routing Benchmark Suite
- **Scientific Foundation**: Spärck Jones (1972), Jain et al. (NeurIPS 2023 [[15]]), Saltzer & Schroeder (1975 [[16]])
- **Local Location**: `workspaces/truongnv/replications/PIGuard_Tier1_FastFilter/datasets/tier1_fastfilter_eval_benchmark.json`
- **SHA-256**: `77d927026cfebbeab32d2653cd4a6934a9fb7786f53c5383837e40915a0b522f`
- **Sample Count**: 18 items

## 2. Taxonomy & Routing Distribution
- **Obvious Direct Injections**: 4 samples (Clear malicious keywords, fast rejection target)
- **Subtle / Borderline Injections**: 2 samples (Borderline confidence, escalation target)
- **Jailbreak Intent**: 2 samples (DAN, EvilBot roleplay)
- **Benign Clear**: 5 samples (Safe conversational queries, fast clearance target)
- **Benign Overdefense Code**: 5 samples (Valid programming code containing method overriding, Git ignore)

## 3. Grounded Academic Role in PI-Guard
Demonstrates how the Tier-1 Fast-Filter screens over 80% of benign traffic in under 1.5ms with 0.0% direct false positive rate, ensuring downstream heavy models only process ambiguous queries.
