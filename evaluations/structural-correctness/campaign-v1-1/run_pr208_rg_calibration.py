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
    proposer_declaration_path = (
        campaign / "rg-semantic-proposals/pr-208.batch-001.proposed.json"
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
    verifier_run_path = (
        campaign / "rg-semantic-labeling-runs/pr-208.batch-001.verifier-run.json"
    )
    verifier_output_path = (
        campaign / "rg-semantic-verifications/pr-208.batch-001.verifier-output.json"
    )
    adjudication_ledger_path = (
        campaign / "rg-semantic-adjudications/pr-208.batch-001.ai-adjudicated.json"
    )
    adjudication_amendment_path = (
        campaign
        / "rg-semantic-labeling-runs/pr-208.batch-001.ai-adjudication-amendment.json"
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
    adjudication_amendment = _adjudication_amendment_record(
        campaign, adjudication_amendment_path
    )
    review_summary = _attach_review_provenance(
        result,
        proposer_run_path=proposer_run_path,
        proposer_declaration_path=proposer_declaration_path,
        verifier_run_path=verifier_run_path,
        verifier_output_path=verifier_output_path,
        adjudicator_run_path=adjudicator_run_path,
        adjudication_ledger_path=adjudication_ledger_path,
        adjudication_amendment=adjudication_amendment,
    )
    result["input_provenance"] = {
        "candidate_universe": _file_identity(campaign, universe_path),
        "observed_retrieval": _file_identity(campaign, retrieval_path),
        "historical_declared_calibration": _file_identity(campaign, declaration_path),
        "historical_proposer_declaration": _file_identity(
            campaign, proposer_declaration_path
        ),
        "frozen_review_design": _file_identity(campaign, review_design_path),
        "historical_review_method": {
            "kind": "source-evidence proposal followed by campaign-local AI adjudication",
            "records": [
                _review_record(campaign, proposer_run_path),
                _review_record(campaign, verifier_run_path),
                _review_record(campaign, adjudicator_run_path),
            ],
            "verifier_decisions": _file_identity(campaign, verifier_output_path),
            "adjudication_ledger": _file_identity(campaign, adjudication_ledger_path),
            "adjudication_amendment": adjudication_amendment,
            "verifier_decision_summary": review_summary,
            "limitation": (
                "The identities and execution contracts are preserved as provenance; "
                "they do not turn the proposal into a verified reference or prove "
                "independent error modes."
            ),
        },
        "review_design_boundary": (
            "The #309 manifest selected all 54 candidate IDs before labeling. Its "
            "proposal/adjudication output remains historical proposed calibration "
            "evidence and is not upgraded to a verified semantic reference here. "
            "The AI-adjudicator amendment was frozen after the 22 verifier "
            "disagreements were known, but before the adjudicator received the "
            "unresolved ledger; it is not a pre-registration of the full #309 "
            "review path."
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
    model_identifier = raw.get("model_identifier") or raw.get("model")
    return {
        **_file_identity(campaign, path),
        "identity": raw["identity"],
        "role": raw["role"],
        "provider": raw["provider"],
        "model": model_identifier,
        "reproducible_model_identifier": model_identifier
        not in {None, "", "not_emitted_by_local_cli"},
        "endpoint_class": raw.get("endpoint_class"),
        "execution_contract": raw.get("execution_contract"),
        "execution": raw.get("execution"),
        "authority_boundary": raw["authority_boundary"],
    }


def _adjudication_amendment_record(
    campaign: Path, path: Path
) -> dict[str, object]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("batch_id") != "pr-208-batch-001":
        raise ValueError("PR #208 adjudication amendment must bind its batch")
    if raw.get("status") != "effective_before_ai_adjudication":
        raise ValueError("PR #208 adjudication amendment must predate adjudication")
    sequencing = raw.get("sequencing")
    if not isinstance(sequencing, list) or not sequencing or (
        "before the third AI receives ledger contents" not in sequencing[0]
    ):
        raise ValueError("PR #208 adjudication amendment must freeze before ledger access")
    return {
        **_file_identity(campaign, path),
        "amendment_id": raw["amendment_id"],
        "status": raw["status"],
        "authority_scope": raw["plan_delta"]["authority_scope"],
        "authorization_timing": (
            "Frozen after the 22 verifier disagreements were known and before the "
            "third AI received the unresolved ledger."
        ),
        "limitation": (
            "This is a post-disagreement plan delta, not a pre-registration of the "
            "entire proposer/verifier/adjudicator path."
        ),
    }


def _attach_review_provenance(
    result: dict[str, object],
    *,
    proposer_run_path: Path,
    proposer_declaration_path: Path,
    verifier_run_path: Path,
    verifier_output_path: Path,
    adjudicator_run_path: Path,
    adjudication_ledger_path: Path,
    adjudication_amendment: dict[str, object],
) -> dict[str, int]:
    proposer_run = json.loads(proposer_run_path.read_text(encoding="utf-8"))
    proposer_declaration = json.loads(
        proposer_declaration_path.read_text(encoding="utf-8")
    )
    verifier_run = json.loads(verifier_run_path.read_text(encoding="utf-8"))
    decisions_raw = json.loads(verifier_output_path.read_text(encoding="utf-8"))
    adjudicator_run = json.loads(adjudicator_run_path.read_text(encoding="utf-8"))
    adjudications_raw = json.loads(adjudication_ledger_path.read_text(encoding="utf-8"))
    decisions = {
        item["candidate_id"]: item
        for item in decisions_raw["decisions"]
    }
    proposer_labels = {
        item["candidate_id"]: item
        for item in proposer_declaration["labels"]
    }
    adjudications = adjudications_raw["entries"]
    candidate_records = result["candidate_records"]
    assert isinstance(candidate_records, list)
    candidate_ids = {item["candidate_id"] for item in candidate_records}
    if set(decisions) != candidate_ids:
        raise ValueError("PR #208 verifier decisions must cover every calibration candidate")
    if set(proposer_labels) != candidate_ids:
        raise ValueError("PR #208 proposer declaration must cover every calibration candidate")
    if decisions_raw["final_status"] != "unverified":
        raise ValueError("PR #208 historical verifier result must remain unverified")
    challenged_ids = {
        candidate_id
        for candidate_id, decision in decisions.items()
        if decision["decision"] == "challenge"
    }
    if set(adjudications) != challenged_ids:
        raise ValueError("PR #208 adjudication ledger must cover only verifier challenges")
    if any(item["decision"] not in {"accept", "challenge"} for item in decisions.values()):
        raise ValueError("PR #208 verifier decision must be accept or challenge")

    proposer_identity = proposer_run["identity"]
    verifier_identity = verifier_run["identity"]
    verifier_model_identifier = verifier_run.get("model_identifier")
    adjudicator_identity = adjudicator_run["identity"]
    for candidate in candidate_records:
        candidate_id = candidate["candidate_id"]
        assert isinstance(candidate_id, str)
        decision = decisions[candidate_id]
        verifier = {
            "identity": verifier_identity,
            "decision": decision["decision"],
            "model_identifier": verifier_model_identifier,
            "reproducible_model_identifier": False,
            "authority": "unverified_verification_attempt",
        }
        if decision["decision"] == "accept":
            _require_final_label_matches(
                candidate,
                proposer_labels[candidate_id],
                "accepted proposer label",
            )
            adjudicator: dict[str, object] = {
                "status": "not_invoked",
                "reason": "verifier accepted the proposer label",
            }
            final_label_lineage = "proposer_retained_after_verifier_accept"
        else:
            entry = adjudications[candidate_id]
            adjudication = entry["adjudication"]
            _require_final_label_matches(
                candidate,
                adjudication["final_label"],
                "adjudicated final label",
            )
            adjudicator = {
                "identity": adjudicator_identity,
                "status": adjudication["status"],
                "disposition": adjudication["disposition"],
                "decision_witnesses": adjudication["decision_witnesses"],
                "role_authorization": adjudication_amendment,
            }
            final_label_lineage = "verifier_challenge_resolved_by_adjudicator"
        candidate["review_provenance"] = {
            "proposer": {
                "identity": proposer_identity,
                "decision": "proposed_label",
            },
            "verifier": verifier,
            "adjudicator": adjudicator,
            "final_label_lineage": final_label_lineage,
            "uncertainty": [
                "The opaque Codex verifier did not emit a reproducible model "
                "identifier and cannot establish verified-reference authority.",
                "This lineage is historical proposed calibration evidence, not an "
                "independent semantic reference or formal metric.",
            ],
        }
    return {
        "accept": len(candidate_ids - challenged_ids),
        "challenge": len(challenged_ids),
        "adjudicated": len(adjudications),
    }


def _require_final_label_matches(
    candidate: dict[str, object], source_label: dict[str, object], source: str
) -> None:
    declared = candidate["declared_calibration"]
    assert isinstance(declared, dict)
    for field in (
        "semantic_relation",
        "proofability",
        "proof_basis",
        "evidence_witnesses",
        "note",
    ):
        declared_field = (
            "semantic_evidence_witnesses" if field == "evidence_witnesses" else field
        )
        if declared[declared_field] != source_label[field]:
            raise ValueError(f"PR #208 {source} does not match declared calibration")


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
