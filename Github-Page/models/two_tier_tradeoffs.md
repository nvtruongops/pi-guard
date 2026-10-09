# Model trade-offs

## Design question

The project proposes combining a fast lexical scorer with a contextual transformer so that uncertain chunks can receive deeper review. This is a research question to evaluate, not proof that a cascade is always better or that the proposed service meets its targets.

See [the current ingress proposal](ingress_architecture.md) for the L1/L2/L3/API flow. L2 ALLOW and BLOCK are chunk-level candidates. REVIEW is routed to L3. Only API aggregation makes the final request-level ALLOW or BLOCK decision.

## Current evidence boundary

Review 2 experiments and run-level metrics remain in the maintainer's ignored local workspace. They are not published or cited as shared evidence here. A reviewed report with its protocol, raw results, and provenance must be placed in a tracked deliverable before this page presents performance numbers.

The symbolic tau_allow and tau_block in the architecture proposal remain assumptions, not established service cutoffs.