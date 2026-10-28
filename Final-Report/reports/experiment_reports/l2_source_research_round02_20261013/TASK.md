---
ArtifactMetadata:
  ArtifactType: task
  UserFacing: true
---
# English L2 public-source acquisition and component-lineage research

## Scope Boundary Declaration

Continue the attached L2 research goal and the user's request to continue research. Preserve V9, V10 and historical datasets. This round addresses public candidate acquisition and evidence gaps in aggregate source lineage; it does not assign canonical labels or select cutoffs.

IN-SCOPE: pin original publisher metadata/cards, ingest only the public Gandalf train split if its declared release and license are confirmed, apply the existing English/privacy-pattern policy, group duplicates with the existing authorized candidate corpus, create a new immutable V11 candidate version, and reuse annotation intake checks. Record component metadata separately from proof of original aggregate provenance. Record discovered unresolved dataset rights in a new sparse V12 quarantine overlay without altering parent versions.

OUT-OF-SCOPE: upstream validation/test payloads, historical locked evaluation data, synthetic generation, automatic canonical labels, legal/privacy approval, fitting before data gates, L3, commit and publication.

## Research questions and execution

- [x] Pin Gandalf and original aggregate-component metadata without downloading evaluation payloads.
- [x] Determine which original revision/split claims can actually be supported; leave unresolved claims explicit.
- [x] Download public Gandalf train only, if its metadata/license checks pass; record payload hash and original split.
- [x] Build V11 with unchanged parent references, English filtering, privacy quarantine, and duplicate-group constraints across parent/new inputs.
- [x] Create V12 with 554 explicit rights holds based on the pinned dataset/code license distinction.
- [x] Extend the existing curator intake stage only as necessary for the new packet and run fresh checks.
- [x] Verify immutable parent/source identities and write an English gate report, run ledger and L3 handoff status.

## Verified round outcome

V11 adds 492 unreviewed candidates; V12 records 554 explicit rights holds. Verification r03 passed 12 artifact checks, including immutable parents, original-record bindings, curator compatibility and governance checks. The r03 parent-ID crosswalk supersedes the earlier pilot-hold count. L2 remains NOT_READY, with zero canonical rows, no fit/test access, and no L3 handoff. See [report](REPORT.md) and [fresh verification](VERIFICATION_r03.json).

## Decision rules

Publisher-declared MIT supports private candidate intake; it is not independent legal clearance or submitter-rights adjudication. Source-level privacy, actual PI/JB/benign labels and independence remain pending. Similarity scores and source labels are provenance only. Original aggregate ingestion revision cannot be inferred from a current publisher release. A new source is provisional until lineage, curator and coverage gates pass.
