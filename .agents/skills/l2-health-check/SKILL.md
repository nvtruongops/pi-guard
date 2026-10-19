---
name: l2-health-check
description: Use when deciding whether a PI-Guard L2 model and its dataset evidence are ready to support a separately authorized L3 fine-tuning run.
---

# PI-Guard L2 Health Check

## When to use

Use this skill before recording whether a trained L2 and its dataset are ready to request L3 fine-tuning. Use it to audit existing authorized artifacts and reports. Do not use it to fit models, select new cutoffs, run the cascade, or evaluate a locked test set.

## Purpose

Review whether the approved dataset and L2 evidence are strong enough to request an L3 fine-tuning run. This is a read-only readiness assessment. `READY_TO_REQUEST_L3` is not training authorization and is not a claim that the cascade is safe or meets a final API target.

Use this skill with the project’s dataset, evaluation, and classifier-training guidance. Keep literature claims, local run evidence, and project acceptance criteria separate.

## Scope boundary

**In scope:** inspect the authorized train/validation manifests, provenance and label-review records, L2 run configuration, saved validation predictions/metrics, and the predeclared routing policy needed for the readiness decision.

**Out of scope:** fitting or tuning a model; selecting new cutoffs; editing or relabeling data; opening test or source-evaluation payloads; running L3 or the API cascade; changing runtime policy; and granting permission to train or publish.

If the task does not authorize a particular artifact, do not open it. Mark the evidence `NOT INSPECTED` and list the authorization or artifact needed. Never use a locked test set to select a model, cutoff, or readiness decision.

## Routing semantics to preserve

The current PI-Guard L2 router has three candidate routes and two explicit score cutoffs. For a scored window, let:

- `B = score(benign)`
- `A = score(PI) + score(JB)`

| Candidate route | Current rule |
|---|---|
| `ALLOW_CANDIDATE` | `B >= tau_allow` and `B > A` |
| `BLOCK_CANDIDATE` | `A >= tau_block` and `A > B` |
| `REVIEW_TO_L3` | Neither rule matches; ties go to REVIEW |

`tau_allow` and `tau_block` are uncalibrated score cutoffs, not calibrated probabilities. REVIEW is the residual route; it has no independent cutoff under this policy. Do not describe this as three learned thresholds. A distinct REVIEW cutoff requires a separately defined uncertainty score, route precedence, tie handling, and evaluation contract.

Use precise cutoff terminology in reports: the router has **two cutoff parameters**; a **cutoff pair** is one assigned value for each parameter; and a **selected operating point** is a pair chosen on validation under predeclared criteria. An illustrative pair such as `0.90/0.90` is neither a selected pair nor an accepted operating point. Report these counts separately.

A per-class REVIEW rate is a measurement, not a threshold:

- benign REVIEW rate = true-benign rows routed REVIEW / all true-benign rows;
- PI REVIEW rate = true-PI rows routed REVIEW / all true-PI rows;
- JB REVIEW rate = true-JB rows routed REVIEW / all true-JB rows.

These rates describe which labeled classes reach L3. L2 candidate routes are not final API decisions. Keep window-level routing counts separate from parent-request final outcomes; do not count multiple windows from one request as independent requests.

## Readiness procedure

### 1. Declare the evaluation scope

Record the task or checkpoint, dataset/version and manifest identity, label schema, supported languages, source families, L1 input/window contract, and intended L3 role. State whether the decision concerns an English-only or multilingual system. Do not generalize beyond the declared scope.

### 2. Check dataset readiness

Review authorized train/validation evidence for:

- row lineage, source/revision identifiers, and documented use basis;
- the operational definitions for benign, PI, and JB, plus how native source labels map to them;
- curator review status and unresolved or conflicting labels; cross-source mappings must have the curator review required by the dataset gate; if review is absent or its status is unknown, mark the gate `NOT READY`;
- exact duplicate and prompt-family grouping, with split separation appropriate to the claim;
- train and validation counts by true label, source family, and supported language;
- frozen split IDs/hashes and consistent normalization, truncation, windowing, and label semantics;
- adequate training support by label and source for the intended L3 task.

If L3 is meant to process only L2 REVIEW traffic, check that its planned training examples represent that incoming distribution. Do not define the L3 training subset from optimistic in-sample L2 predictions without an explicitly justified split-aware method. Validation REVIEW support and L3 training support are separate requirements; one cannot stand in for the other.

Missing rights/provenance, unresolved label semantics, split leakage, or unsupported language/source claims block a readiness pass. Report them; do not silently repair the dataset during this check.

### 3. Check the L2 run and validation evidence

Confirm that the saved run identifies the exact dataset version/split, fit IDs, class order, model/vectorizer configuration, seed, and input/window contract. Check that validation predictions are tied to the same validation IDs and contain no train/test substitution.

Require validation metrics with integer supports and denominators, including:

- confusion matrix and precision, recall, and F1 for benign, PI, and JB separately;
- the complete predeclared `tau_allow × tau_block` sweep, or a documented reason it is not applicable;
- the selected validation operating point and selection rationale, if one exists;
- counts, denominators, and rates for PI early-ALLOW, JB early-ALLOW, pooled attack early-ALLOW, benign early-BLOCK, and REVIEW for each true label;
- REVIEW total/load, plus source-family and language breakdowns where available;
- route unit (window or request) and source of every reported number.

Cutoffs must be selected on authorized validation data, never on test. A repeated identical run establishes repeatability only; it does not establish model quality. An illustrative or unselected cutoff pair is descriptive evidence, not a passing operating point.

### 4. Compare results with predeclared gates

Before interpreting a validation sweep, locate the acceptance criteria that were recorded before inspecting the sweep. They must define, with units and denominators:

- maximum PI and JB early-ALLOW rates;
- maximum benign early-BLOCK rate;
- acceptable REVIEW workload/capacity;
- minimum per-class validation REVIEW support for conditional L3 assessment;
- minimum per-class/source training support for the intended L3 task;
- the final API-level targets to evaluate after the cascade is frozen.

Do not invent limits from observed results. The project’s benign final API FPR target is not automatically the same as L2 window-level early-BLOCK rate. The full API aggregation determines final request outcomes and must be evaluated separately.

If these limits are absent, mark `NOT READY`; request that the owner predeclare them before a new validation selection. If the available validation data are too narrow or small for the stated scope, mark `NOT READY` or narrow the claim. Do not compensate by opening test. Confirm that test/source-evaluation data were not used for selection only from authorized run metadata, an access record, or an owner attestation; never open the payload to confirm. If prior-use status is unknown, do not report a readiness pass.

### 5. Issue a bounded decision

Use exactly one status:

- **`READY_TO_REQUEST_L3`** — dataset and L2 evidence pass all stated gates; at least one validation-selected operating point meets the predeclared limits; classwise REVIEW validation support and L3 training support are adequate; test/source-evaluation payloads were not used for selection. This status permits a request for separate L3 authorization only.
- **`NOT_READY`** — a required gate is unmet, missing, too weak for the declared scope, or lacks predeclared limits. List each blocker and the next evidence needed.
- **`INVALID_EVIDENCE`** — evidence is contradictory, cannot be tied to the stated dataset/split, has missing denominators or broken lineage, or records that a locked test/source-evaluation set influenced selection. Explain which claim is invalid and what fresh evidence is required.

Never turn `READY_TO_REQUEST_L3` into an instruction to train automatically. A human must authorize L3 training as a separate task.

## Required report format

```markdown
# L2 Health Check

## Scope Boundary Declaration
- Task/checkpoint:
- Dataset and split identity:
- Supported languages/sources:
- In scope:
- Out of scope / not inspected:

## Decision
- Status: READY_TO_REQUEST_L3 | NOT_READY | INVALID_EVIDENCE
- L3 training authorized: No; separate authorization required.

## Evidence
| Gate | Status | Evidence path/ID | Counts and denominators | Limitation |
|---|---|---|---|---|

## L2 route summary
| True label | ALLOW count/rate | REVIEW count/rate | BLOCK count/rate | Unit |
|---|---:|---:|---:|---|

## Blockers and next evidence
- ...

## Test boundary
- Test/source-evaluation payload inspected by this check: No (this skill does not open them)
- Prior use for model or cutoff selection: Verified no / reported yes (evidence invalidated) / unknown (readiness not established)
```

Use exact counts and denominators. Label missing measurements as `NOT AVAILABLE`; never infer or fabricate them. Link each conclusion to the authorized artifact that supports it.

## Common mistakes

- Treating the three candidate routes as three independent cutoffs.
- Calling a REVIEW percentage “low” or “good” without a predeclared workload and class-support criterion.
- Treating the 1.5% final API benign FPR target as an L2 early-BLOCK limit.
- Reporting pooled accuracy or Macro-F1 without per-class support, route errors, and source/language slices.
- Calling inherited source mappings curator-adjudicated gold labels.
- Calling an illustrative cutoff selected or a validation result a test result.
- Using test results to decide whether L3 should be trained, then presenting the same test as untouched final evaluation.
- Treating a readiness pass as authorization to train L3.