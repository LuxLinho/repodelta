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

The decisive counterexample is `distinctive_phrase`: it retrieves **5 declared direct** and **9 declared non-direct** candidates. The same lexical association therefore cannot decide semantic relation. Its job may remain broad candidate retrieval; current production already treats it as `suggested`, not direct authority.

## Completion: precise insufficiency

The bounded PR #208 evidence is **insufficient to choose exactly one next production layer**. It identifies two separate defects, but does not establish whether retrieval recall or semantic resolution should be changed first.

1. **Candidate-retrieval recall is insufficient in this set.** Seven of the 12 declared semantic-direct candidates were not retrieved.
2. **Retrieval reason does not determine semantic relation.** `distinctive_phrase` retrieves **5 declared direct** and **9 declared non-direct** candidates.

The architectural implication is narrower and stable: candidate-retrieval reason and semantic relation must remain separate layers. In current production, `distinctive_phrase` is already `suggested`, not direct. Its mixture is therefore not, by itself, a direct-admission defect.

PR #208 cannot decide whether the next production change should prioritize recall or semantic resolution. Proofability and final admission also remain unmeasured because this sample contains neither a typed production proof trace nor an observed current direct attempt. No production behavior changes in this calibration.

The generated calibration also binds the #309 AI-adjudication amendment by SHA-256. The amendment was frozen after the 22 verifier disagreements were known but before the adjudicator received their ledger. It is recorded as a post-disagreement plan delta, not as prospective registration of the full #309 review path.
