from __future__ import annotations

import importlib.util
import json
from dataclasses import replace
from pathlib import Path

import pytest

from repodelta.evaluation.rg_calibration import analyze_rg_semantic_layer_calibration
from repodelta.evaluation.rg_candidate_universe import (
    load_rg_candidate_universe,
    load_rg_retrieval_observation,
    load_rg_semantic_reference,
    verify_rg_semantic_reference,
)


ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "evaluations/structural-correctness/campaign-v1-1"
RUNNER = CAMPAIGN / "run_pr208_rg_calibration.py"


def _runner_module():
    spec = importlib.util.spec_from_file_location("pr208_rg_calibration", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _inputs():
    return (
        load_rg_candidate_universe(CAMPAIGN / "rg-candidate-universes/pr-208.json"),
        load_rg_retrieval_observation(
            CAMPAIGN / "rg-retrieval-observations/pr-208.json"
        ),
        load_rg_semantic_reference(
            CAMPAIGN
            / "rg-semantic-proposals/pr-208.batch-001.ai-adjudicated.proposed.json"
        ),
    )


def test_pr208_calibration_preserves_boundaries_and_nominates_semantic_relation() -> None:
    universe, retrieval, declaration = _inputs()

    result = analyze_rg_semantic_layer_calibration(universe, retrieval, declaration)

    assert result["classification"] == {
        "kind": "declared_historical_calibration",
        "semantic_reference": "not_verified",
        "semantic_metrics": "not_emitted",
        "production_changed": False,
        "causal_replay": False,
    }
    assert result["counts"] == {
        "candidate_count": 54,
        "declared_semantic_direct": 12,
        "declared_resolved_non_direct": 42,
        "declared_insufficient": 0,
        "observed_retrieved": 15,
        "observed_direct_attempts": 0,
    }
    assert result["mechanism_breakdown"]["candidate_retrieval"][
        "declared_direct_not_retrieved"
    ]["count"] == 7
    assert result["mechanism_breakdown"]["semantic_relation"][
        "observed_retrieved_declared_non_direct"
    ]["count"] == 10
    assert result["mechanism_breakdown"]["semantic_relation"][
        "association_role_mixtures"
    ] == [
        {
            "association": "distinctive_phrase",
            "declared_direct_candidate_ids": [
                "C:R1:E:structural_change:7c4162e02e623fea377f",
                "C:R1:E:structural_change:d0cf036a1010c1207bc5",
                "C:R2:E:structural_change:d0cf036a1010c1207bc5",
                "C:R4:E:structural_change:d0cf036a1010c1207bc5",
                "C:R5:E:structural_change:d0cf036a1010c1207bc5",
            ],
            "declared_non_direct_candidate_ids": [
                "C:R1:E:structural_change:44a2370ce77a6e66f8e7",
                "C:R1:E:structural_change:4fbcf96b02d19017c2c9",
                "C:R1:E:structural_change:5d2be31cc60dea3d2f3b",
                "C:R2:E:structural_change:4fbcf96b02d19017c2c9",
                "C:R2:E:structural_change:5d2be31cc60dea3d2f3b",
                "C:R4:E:structural_change:4fbcf96b02d19017c2c9",
                "C:R4:E:structural_change:5d2be31cc60dea3d2f3b",
                "C:R5:E:structural_change:4fbcf96b02d19017c2c9",
                "C:R5:E:structural_change:5d2be31cc60dea3d2f3b",
            ],
        }
    ]
    assert result["completion"]["state"] == "sufficient_evidence"
    assert result["completion"]["next_production_layer"] == "semantic_relation"
    assert "Expanding recall before semantic separation" in result["completion"][
        "sequencing_rationale"
    ]


def test_calibration_rejects_a_verified_reference_and_unbound_retrieval() -> None:
    universe, retrieval, declaration = _inputs()
    verified = verify_rg_semantic_reference(
        declaration,
        universe,
        verified_by="test-only",
        verification_method="test-only",
        verification_evidence=("test-only",),
        system_under_test_isolated=True,
    )

    with pytest.raises(ValueError, match="only accepts a proposed"):
        analyze_rg_semantic_layer_calibration(universe, retrieval, verified)
    with pytest.raises(ValueError, match="does not match candidate universe"):
        analyze_rg_semantic_layer_calibration(
            universe,
            replace(retrieval, candidate_universe_digest="wrong"),
            declaration,
        )
    source_less_universe = replace(
        universe,
        anchors=(replace(universe.anchors[0], sources=()), *universe.anchors[1:]),
    )
    with pytest.raises(ValueError, match="source-anchor witness"):
        analyze_rg_semantic_layer_calibration(
            source_less_universe,
            replace(retrieval, candidate_universe_digest=source_less_universe.digest),
            replace(
                declaration,
                candidate_universe_digest=source_less_universe.digest,
            ),
        )


def test_committed_pr208_calibration_is_reproducible() -> None:
    result = _runner_module().build_pr208_rg_calibration(CAMPAIGN)
    committed = json.loads(
        (
            CAMPAIGN / "results/rg-calibration/pr-208.json"
        ).read_text(encoding="utf-8")
    )

    assert json.loads(json.dumps(result)) == committed
    assert result["input_provenance"]["historical_review_method"][
        "verifier_decision_summary"
    ] == {"accept": 32, "challenge": 22, "adjudicated": 22}
    records = {item["candidate_id"]: item for item in result["candidate_records"]}
    accepted = records["C:G1:E:structural_change:44a2370ce77a6e66f8e7"][
        "review_provenance"
    ]
    assert accepted["verifier"]["decision"] == "accept"
    assert accepted["verifier"]["reproducible_model_identifier"] is False
    assert accepted["adjudicator"]["status"] == "not_invoked"
    challenged = records["C:G1:E:structural_change:9ff44326982c1acafe85"][
        "review_provenance"
    ]
    assert challenged["verifier"]["decision"] == "challenge"
    assert challenged["adjudicator"]["identity"] == (
        "deepseek:deepseek-v4-pro:pr-208-batch-001-ai-adjudicator"
    )
    assert challenged["final_label_lineage"] == (
        "verifier_challenge_resolved_by_adjudicator"
    )
