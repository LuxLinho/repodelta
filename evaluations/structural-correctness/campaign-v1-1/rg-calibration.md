# PR #208 R/G semantic-layer calibration

This is the bounded decision-calibration work for [Issue #316](https://github.com/repodelta/repodelta/issues/316). It does not change production R/G association, structural focus, assessment, HTML, LLM authority, or the frozen v1.1 candidate universe/retrieval observation.

## Inputs and authority

The analysis has three separate inputs:

| Input | Provenance | Authority in this analysis |
| --- | --- | --- |
| `rg-candidate-universes/pr-208.json` | Frozen profile-eligible changed-anchor boundary | Observed candidate identity and source-anchor witness only |
| `rg-semantic-proposals/pr-208.batch-001.ai-adjudicated.proposed.json` | Historical #309 all-54 source-evidence proposal/adjudication record | Declared calibration judgment only; never a verified semantic reference |
| `rg-retrieval-observations/pr-208.json` | Frozen observation of the current RepoDelta retrieval output | Observed system fact only |

The historical review design selected every one of the 54 candidate IDs before labeling in `rg-semantic-labeling-runs/pr-208.batch-001.manifest.json`. Every final label now retains its actual review lineage: the `deepseek-v4-flash` proposer, the opaque Codex verifier's `accept` or `challenge` decision, and—only for the 22 challenges—the `deepseek-v4-pro` adjudication. The verifier's `not_emitted_by_local_cli` model identifier is explicit for all 54 records; it remains an unverified review attempt, not a reproducible verification authority. Immutable run records, decision ledger, execution contracts, and authority boundaries are copied into generated provenance. This task makes no new model call and does not relabel, repair, or extend #309.

## Contract

The consumer accepts only a complete, `proposed` historical declaration. It fails closed when the declaration/retrieval does not bind to the frozen candidate universe, a candidate is absent, a label remains pending, or the declaration has been upgraded to `verified`. Verified references have a separate canonical consumer (`compare-rg-semantic-candidates`) and must not be silently converted into calibration output.

The calibration does not emit semantic FI/FE, benchmark metrics, or a model ranking. It may only:

1. identify a retrieval gap, semantic-role mixture, unmeasured proofability boundary, or unmeasured direct-admission boundary;
2. nominate one falsifiable next production layer, if the bounded counterexample supports one; or
3. end with an explicit insufficiency conclusion.

Run the materialization from the repository root:

```bash
PYTHONPATH=src python evaluations/structural-correctness/campaign-v1-1/run_pr208_rg_calibration.py
```

The committed output is `results/rg-calibration/pr-208.json`; its input digests make the analysis reproducible without granting its declared labels any formal authority.
