# README and ingress architecture documentation design

## Goal

Bring PI-Guard-owned, actively maintained README files and the documentation landing page into line with the current Review 2 evidence, and make the Review 1 ingress diagram explicit about L2 route candidates, L3 dispatch, and threshold status.

## Scope

- Update maintained project and folder-index README files in the repository root, `Final-Report/`, `Github-Page/`, and active workspace indexes.
- Update `Github-Page/index.md` and its generator template so the architecture introduction and supplied diagram remain visible after the normal portal build.
- Correct the requested Review 1 Draw.io diagram where its route flow is visually ambiguous.
- Keep prior report folders and their README files frozen, except for the explicitly named Draw.io source. Keep upstream, paper, dataset, run-artifact, and withdrawn-evidence README files unchanged.
- Do not edit `CAPSTONE PROJECT REGISTER.md`, `docs/fpt_capstone_guide/`, model artifacts, experiment outputs, or product implementation.

## Evidence and claims

- The active umbrella milestone is Review 2. Its overall checklist remains open.
- The separate seed-42 PIDS-Bench TF-IDF-to-DeBERTa experiment completed and has a report with held-out results and provenance. State its dataset, seed, denominators, and limits when citing it.
- `v2.2-baseline-freezing-meeting6` is the last recorded workspace snapshot dated 2026-09-24; `pyproject.toml` says package version `0.1.0`. Keep milestone snapshot and package version distinct. Do not invent a newer release number.
- In the proposed ingress flow, L2 emits per-chunk ALLOW, REVIEW, or BLOCK candidates. REVIEW chunks alone are sent to L3. L2 ALLOW/BLOCK candidates and L3 predictions go to API coverage/request aggregation; only that aggregation emits final request ALLOW/BLOCK.
- `p_attack` is a model score. `τ_allow` and `τ_block` in the Review 1 architecture are symbolic design parameters, not accepted service cutoffs. The separate seed-42 experiment used validation-selected gates for its specific run; those do not establish project-wide or service thresholds.

## Verification

- Parse the edited Draw.io XML and verify the candidate route branches, REVIEW-only L3 dispatch, API aggregation inputs, final decision ownership, and threshold disclaimer.
- Verify the architecture image used by both README and portal matches the checked-in diagram output where an exporter is available; otherwise record that export could not be refreshed and do not present a stale image as newly rendered.
- Check links and images in edited README files and run a strict MkDocs build without invoking the destructive portal aggregator unless its cleanup behavior has been made safe.
- Review `git diff` and status to confirm frozen reports and pre-existing upstream changes were preserved.
