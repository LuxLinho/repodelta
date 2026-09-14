# PR #208 R/G semantic-layer calibration

This is the bounded decision calibration for [Issue #316](https://github.com/repodelta/repodelta/issues/316). It consumes the frozen 54-candidate PR #208 universe, the observed current retrieval sidecar, and the historical #309 proposed source-evidence labels. It is **not** a verified semantic reference, semantic FI/FE result, benchmark, production decision, or model comparison.

## Inputs kept separate

| Surface | Role | Authority here |
| --- | --- | --- |
| Candidate universe | Frozen changed-anchor identities and source witnesses | Observed boundary |
| #309 adjudicated proposal | 54 declared semantic/proofability judgments | Historical calibration evidence only |
| Retrieval observation | Current association/convergence result | Observed system fact only |

The generated [`pr-208.json`](pr-208.json) binds all input artifacts, including the all-54 frozen review design, proposer, opaque verifier, verifier-decision output, adjudication ledger, and adjudicator by SHA-256. Every candidate record exposes its actual `proposer → verifier → optional adjudicator` lineage and the opaque verifier limitation. It rejects a `verified` reference so it cannot become a second semantic-comparison consumer.

## Mechanism breakdown

| Observation | Count | Meaning |
| --- | ---: | --- |
| Candidates | 54 | Complete bounded PR #208 set |
| Declared semantic-direct | 12 | Historical proposed calibration judgment, not formal truth |
| Declared direct retrieved | 5 | Direct candidates surfaced by current association |
| Declared direct not retrieved | 7 | Retrieval gap; not semantic-negative evidence |
| Retrieved declared non-direct | 10 | Semantic noise in the current retrieved set |
| Current direct attempts | 0 | Final direct admission is not measured by this sample |

The decisive counterexample is `distinctive_phrase`: it retrieves **5 declared direct** and **9 declared non-direct** candidates. The same lexical association therefore cannot decide semantic relation or direct authority. Its job may remain broad candidate retrieval.

## Completion: sufficient evidence

The bounded evidence nominates exactly one next production layer: **semantic relation**.

> Introduce an R/G semantic-relation stage after broad candidate retrieval and before direct admission. A distinctive phrase, claim bridge, or other lexical association remains candidate evidence; it cannot itself establish semantic-direct membership.

Both recall and semantic discrimination are deficient here. The sequencing is nevertheless semantic separation first: expanding recall before separating semantic role would send more candidates into the same currently mixed lexical surface and can expand noise together with recall. The next production step must preserve lexical associations as candidates, separate their semantic roles, and only then improve retrieval coverage.

This hypothesis is falsified if an explicit semantic-relation stage cannot distinguish the currently mixed `distinctive_phrase` candidates from source evidence without changing retrieval, or if it must reuse the lexical association itself as semantic authority.

Candidate retrieval remains a follow-up: the seven declared-direct misses need greater recall, but broad recall does not need to decide semantic role. Proofability and final admission are not nominated because this sample has no typed production proof trace and no observed current direct attempt. No production behavior changes in this calibration.
