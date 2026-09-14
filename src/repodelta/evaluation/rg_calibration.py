"""Evaluation-only R/G semantic-layer calibration.

This consumer analyzes a *proposed* source-evidence review against an observed
R/G retrieval sidecar.  It is deliberately not a semantic-reference comparator:
it produces no semantic FI/FE metrics and cannot make a production authority
claim.  Its only output is a bounded architecture hypothesis (or an explicit
insufficiency result) for a separately scoped production experiment.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict
from typing import Any

from repodelta.evaluation.rg_candidate_universe import (
    RGRetrievalObservation,
    RGSemanticCandidateUniverse,
    RGSemanticReference,
)


RG_CALIBRATION_SCHEMA = "rg_semantic_layer_calibration.v1"

_DIRECT_RELATIONS = frozenset(
    {"implements", "constrains", "removes", "directly_verifies"}
)
_DIRECT_ASSOCIATIONS = frozenset({"provided_association", "exact_identifier"})


def analyze_rg_semantic_layer_calibration(
    universe: RGSemanticCandidateUniverse,
    retrieval: RGRetrievalObservation,
    declared_calibration: RGSemanticReference,
) -> dict[str, Any]:
    """Compare one bounded, non-authoritative review with observed retrieval.

    ``declared_calibration`` must remain proposed.  A verified semantic
    reference belongs to ``compare_rg_retrieval`` instead; accepting it here
    would make this calibration consumer a second semantic-metric sink.
    """

    _validate_inputs(universe, retrieval, declared_calibration)
    labels = {item.candidate_id: item for item in declared_calibration.labels}
    rows = {item.candidate_id: item for item in retrieval.rows}
    anchors = {item.evidence_id: item for item in universe.anchors}
    source_anchor_witnesses = [
        {
            "evidence_id": anchor.evidence_id,
            "summary": anchor.summary,
            "path": anchor.path,
            "sources": [asdict(source) for source in anchor.sources],
        }
        for anchor in universe.anchors
    ]

    candidate_records: list[dict[str, Any]] = []
    declared_direct: set[str] = set()
    retrieved: set[str] = set()
    direct_attempts: set[str] = set()
    unresolved: set[str] = set()
    by_association: dict[str, list[str]] = defaultdict(list)

    for candidate in universe.candidates:
        label = labels[candidate.candidate_id]
        row = rows[candidate.candidate_id]
        semantic_direct = label.semantic_relation in _DIRECT_RELATIONS
        observed = row.retrieval_state != "not_retrieved"
        direct_attempt = row.association in _DIRECT_ASSOCIATIONS
        if semantic_direct:
            declared_direct.add(candidate.candidate_id)
        if observed:
            retrieved.add(candidate.candidate_id)
            assert row.association is not None
            by_association[row.association].append(candidate.candidate_id)
        if direct_attempt:
            direct_attempts.add(candidate.candidate_id)
        if label.semantic_relation == "insufficient":
            unresolved.add(candidate.candidate_id)

        mechanisms = _candidate_mechanisms(
            semantic_direct=semantic_direct,
            unresolved=label.semantic_relation == "insufficient",
            observed=observed,
            direct_attempt=direct_attempt,
        )
        candidate_records.append(
            {
                "candidate_id": candidate.candidate_id,
                "subject_id": candidate.subject_id,
                "evidence_id": candidate.evidence_id,
                "evidence_role": candidate.evidence_role,
                "declared_calibration": {
                    "semantic_relation": label.semantic_relation,
                    "proofability": label.proofability,
                    "proof_basis": label.proof_basis,
                    "semantic_evidence_witnesses": list(label.evidence_witnesses),
                    "note": label.note,
                },
                "source_anchor_witness_id": candidate.evidence_id,
                "observed_retrieval": {
                    "state": row.retrieval_state,
                    "association": row.association,
                    "relation_id": row.relation_id,
                    "reasons": [asdict(reason) for reason in row.reasons],
                },
                "mechanism_observations": mechanisms,
            }
        )

    resolved_non_direct = {
        candidate_id
        for candidate_id, label in labels.items()
        if label.semantic_relation not in _DIRECT_RELATIONS
        and label.semantic_relation != "insufficient"
    }
    selected_direct = declared_direct & retrieved
    selected_non_direct = resolved_non_direct & retrieved
    direct_capable = {
        item.candidate_id
        for item in declared_calibration.labels
        if item.proofability == "direct_capable"
    }
    association_mixtures = _association_mixtures(
        by_association, declared_direct, resolved_non_direct
    )
    completion = _completion(
        association_mixtures=association_mixtures,
        declared_direct=declared_direct,
        selected_direct=selected_direct,
        selected_non_direct=selected_non_direct,
        unresolved=unresolved,
    )

    return {
        "schema_version": RG_CALIBRATION_SCHEMA,
        "classification": {
            "kind": "declared_historical_calibration",
            "semantic_reference": "not_verified",
            "semantic_metrics": "not_emitted",
            "production_changed": False,
            "causal_replay": False,
        },
        "candidate_universe_digest": universe.digest,
        "structural_packet_digest": universe.structural_packet_digest,
        "declared_calibration_authority": asdict(declared_calibration.authority),
        "source_anchor_witnesses": source_anchor_witnesses,
        "counts": {
            "candidate_count": len(universe.candidates),
            "declared_semantic_direct": len(declared_direct),
            "declared_resolved_non_direct": len(resolved_non_direct),
            "declared_insufficient": len(unresolved),
            "observed_retrieved": len(retrieved),
            "observed_direct_attempts": len(direct_attempts),
        },
        "mechanism_breakdown": {
            "candidate_retrieval": {
                "declared_direct_retrieved": _ids(selected_direct),
                "declared_direct_not_retrieved": _ids(declared_direct - retrieved),
                "interpretation": (
                    "A missing candidate is a retrieval gap, not evidence that the "
                    "candidate is semantically unrelated."
                ),
            },
            "semantic_relation": {
                "observed_retrieved_declared_direct": _ids(selected_direct),
                "observed_retrieved_declared_non_direct": _ids(selected_non_direct),
                "association_role_mixtures": association_mixtures,
                "interpretation": (
                    "A lexical association that contains both declared direct and "
                    "declared non-direct candidates is candidate evidence, not a "
                    "semantic-direct determination."
                ),
            },
            "proofability": {
                "declared_direct_capable": _ids(direct_capable),
                "direct_capable_retrieved_without_direct_attempt": _ids(
                    (direct_capable & retrieved) - direct_attempts
                ),
                "disposition": "not_discriminated",
                "limitation": (
                    "The declared proofability judgment is not a typed production "
                    "proof trace; this calibration cannot measure a missing "
                    "deterministic-proof mechanism."
                ),
            },
            "final_admission": {
                "observed_direct_attempts": _ids(direct_attempts),
                "direct_capable_without_direct_attempt": _ids(
                    direct_capable - direct_attempts
                ),
                "disposition": "not_discriminated",
                "limitation": (
                    "No current provided/exact association attempts direct admission "
                    "inside this bounded PR #208 sample."
                ),
            },
        },
        "candidate_records": candidate_records,
        "completion": completion,
        "limits": {
            "authority": (
                "The declared judgments are historical proposed calibration evidence "
                "from #309, not a protocol-verified semantic reference."
            ),
            "scope": (
                "PR #208's 54 profile-eligible changed-anchor memberships are not a "
                "repository-wide or v1.1-population result."
            ),
            "inference": (
                "The nominated layer is an architecture hypothesis for a future "
                "production experiment, not a claim that the hypothesis has been "
                "validated in production."
            ),
        },
    }


def _validate_inputs(
    universe: RGSemanticCandidateUniverse,
    retrieval: RGRetrievalObservation,
    declared_calibration: RGSemanticReference,
) -> None:
    candidate_ids = {item.candidate_id for item in universe.candidates}
    if retrieval.structural_packet_digest != universe.structural_packet_digest:
        raise ValueError("R/G calibration retrieval does not match structural packet")
    if retrieval.candidate_universe_digest != universe.digest:
        raise ValueError("R/G calibration retrieval does not match candidate universe")
    if {item.candidate_id for item in retrieval.rows} != candidate_ids:
        raise ValueError("R/G calibration retrieval must dispose every candidate")
    if declared_calibration.candidate_universe_digest != universe.digest:
        raise ValueError("R/G calibration declaration does not match candidate universe")
    if {item.candidate_id for item in declared_calibration.labels} != candidate_ids:
        raise ValueError("R/G calibration declaration must label every candidate")
    anchors = {item.evidence_id: item for item in universe.anchors}
    if any(not anchors[item.evidence_id].sources for item in universe.candidates):
        raise ValueError("R/G calibration requires a source-anchor witness per candidate")
    if declared_calibration.authority.status != "proposed":
        raise ValueError("R/G calibration only accepts a proposed historical declaration")
    if any(item.review_status != "reviewed" for item in declared_calibration.labels):
        raise ValueError("R/G calibration requires reviewed declared labels")
    if declared_calibration.out_of_universe:
        raise ValueError("R/G calibration keeps its declared boundary to the universe")


def _candidate_mechanisms(
    *, semantic_direct: bool, unresolved: bool, observed: bool, direct_attempt: bool
) -> list[str]:
    if unresolved:
        return ["semantic_insufficient"]
    if semantic_direct and not observed:
        return ["retrieval_miss"]
    if semantic_direct and direct_attempt:
        return ["retrieved_semantic_direct", "observed_direct_attempt"]
    if semantic_direct:
        return ["retrieved_semantic_direct", "no_observed_direct_attempt"]
    if observed:
        return ["retrieved_semantic_noise"]
    return ["not_retrieved_non_direct"]


def _association_mixtures(
    by_association: dict[str, list[str]],
    declared_direct: set[str],
    resolved_non_direct: set[str],
) -> list[dict[str, Any]]:
    mixtures: list[dict[str, Any]] = []
    for association, candidate_ids in sorted(by_association.items()):
        direct_ids = sorted(set(candidate_ids) & declared_direct)
        non_direct_ids = sorted(set(candidate_ids) & resolved_non_direct)
        if direct_ids and non_direct_ids:
            mixtures.append(
                {
                    "association": association,
                    "declared_direct_candidate_ids": direct_ids,
                    "declared_non_direct_candidate_ids": non_direct_ids,
                }
            )
    return mixtures


def _completion(
    *,
    association_mixtures: list[dict[str, Any]],
    declared_direct: set[str],
    selected_direct: set[str],
    selected_non_direct: set[str],
    unresolved: set[str],
) -> dict[str, Any]:
    if association_mixtures and selected_direct and selected_non_direct:
        return {
            "state": "sufficient_evidence",
            "next_production_layer": "semantic_relation",
            "hypothesis": (
                "Insert an R/G semantic-relation stage after broad candidate "
                "retrieval and before direct admission. A distinctive phrase, claim "
                "bridge, or other lexical association remains candidate evidence; it "
                "cannot itself establish semantic-direct membership."
            ),
            "falsifier": (
                "The hypothesis fails if a future isolated cross-PR evaluation shows "
                "that each pre-semantic association class maps to one semantic role, "
                "or if the new stage permits lexical association alone to create a "
                "direct admission."
            ),
            "why_not_other_layers": {
                "candidate_retrieval": (
                    "Retrieval has declared-direct misses, but broad recall need not "
                    "decide semantic role; those misses remain a separate follow-up."
                ),
                "proofability": (
                    "This input has declared direct-capable judgments but no typed "
                    "production proof trace, so it cannot isolate proofability."
                ),
                "final_admission": (
                    "The bounded observation contains no current direct attempts, so "
                    "it cannot measure final-admission overreach or underreach."
                ),
            },
        }
    return {
        "state": "insufficient_evidence",
        "reason": (
            "The bounded declaration does not contain an observed association class "
            "with both direct and non-direct resolved candidates."
        ),
        "observed_counts": {
            "declared_direct": len(declared_direct),
            "retrieved_declared_direct": len(selected_direct),
            "retrieved_declared_non_direct": len(selected_non_direct),
            "declared_insufficient": len(unresolved),
        },
    }


def _ids(candidate_ids: set[str]) -> dict[str, Any]:
    return {"count": len(candidate_ids), "candidate_ids": sorted(candidate_ids)}
