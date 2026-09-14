"""Materialize the bounded PR #208 R/G semantic-layer calibration."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from repodelta.evaluation.rg_calibration import analyze_rg_semantic_layer_calibration
from repodelta.evaluation.rg_candidate_universe import (
    load_rg_candidate_universe,
    load_rg_retrieval_observation,
    load_rg_semantic_reference,
    write_rg_candidate_artifact,
)


PR208_UNIVERSE_DIGEST = "6ee61bf0f516385acfce02172b1b2466a0ffb3a7cec58165e4fcc4b1c5a86502"
PR208_CANDIDATE_COUNT = 54


def build_pr208_rg_calibration(campaign: Path) -> dict[str, object]:
    """Bind the fixed #309 declaration to frozen PR #208 observed facts."""

    universe_path = campaign / "rg-candidate-universes/pr-208.json"
    retrieval_path = campaign / "rg-retrieval-observations/pr-208.json"
    declaration_path = (
        campaign
        / "rg-semantic-proposals/pr-208.batch-001.ai-adjudicated.proposed.json"
    )
    review_design_path = (
        campaign / "rg-semantic-labeling-runs/pr-208.batch-001.manifest.json"
    )
    proposer_run_path = (
        campaign / "rg-semantic-labeling-runs/pr-208.batch-001.proposer-run.json"
    )
    adjudicator_run_path = (
        campaign / "rg-semantic-labeling-runs/pr-208.batch-001.ai-adjudicator-run.json"
    )
    universe = load_rg_candidate_universe(universe_path)
    if (
        universe.digest != PR208_UNIVERSE_DIGEST
        or len(universe.candidates) != PR208_CANDIDATE_COUNT
    ):
        raise ValueError("PR #208 calibration requires the frozen 54-candidate universe")
    result = analyze_rg_semantic_layer_calibration(
        universe,
        load_rg_retrieval_observation(retrieval_path),
        load_rg_semantic_reference(declaration_path),
    )
    result["input_provenance"] = {
        "candidate_universe": _file_identity(campaign, universe_path),
        "observed_retrieval": _file_identity(campaign, retrieval_path),
        "historical_declared_calibration": _file_identity(campaign, declaration_path),
        "frozen_review_design": _file_identity(campaign, review_design_path),
        "historical_review_method": {
            "kind": "source-evidence proposal followed by campaign-local AI adjudication",
            "records": [
                _review_record(campaign, proposer_run_path),
                _review_record(campaign, adjudicator_run_path),
            ],
            "limitation": (
                "The identities and execution contracts are preserved as provenance; "
                "they do not turn the proposal into a verified reference or prove "
                "independent error modes."
            ),
        },
        "review_design_boundary": (
            "The #309 manifest selected all 54 candidate IDs before labeling. Its "
            "proposal/adjudication output remains historical proposed calibration "
            "evidence and is not upgraded to a verified semantic reference here."
        ),
    }
    return result


def _file_identity(campaign: Path, path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(campaign)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def _review_record(campaign: Path, path: Path) -> dict[str, object]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {
        **_file_identity(campaign, path),
        "identity": raw["identity"],
        "role": raw["role"],
        "provider": raw["provider"],
        "model": raw.get("model") or raw.get("model_identifier"),
        "endpoint_class": raw["endpoint_class"],
        "execution_contract": raw["execution_contract"],
        "authority_boundary": raw["authority_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Materialize the bounded PR #208 R/G semantic-layer calibration"
    )
    parser.add_argument(
        "--campaign",
        type=Path,
        default=Path(__file__).parent,
        help="Frozen v1.1 campaign directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output calibration JSON (defaults under the campaign results directory)",
    )
    args = parser.parse_args()
    output = args.output or args.campaign / "results/rg-calibration/pr-208.json"
    write_rg_candidate_artifact(build_pr208_rg_calibration(args.campaign), output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
