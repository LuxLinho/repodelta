# Responsibility-closed delivery

Treat the repository as responsibility pipelines. A semantic change must:

1. replace the authority for the affected output;
2. migrate every observed affected upstream and downstream contract;
3. remove or classify stale producers, mappings, consumers, and bypasses;
4. verify that observed intended production sinks consume the new result.

Each changed boundary has one canonical contract: preserved properties,
permitted loss, and failure behavior. Representations may differ when mappings
preserve it; consumers may project but must not re-decide upstream semantics.

Before changing or adding a derived result, record provenance (observed,
declared, inferred, or derived), authority scope (domain-wide, cross-consumer,
consumer-local, or presentation-only), owner, and authorized semantic
dependencies. Explicitly local projection is allowed; undeclared production is
not.

Mutation executes the recorded plan. If evidence materially changes target,
authority, contract, region, or derived-result owner, re-plan before further
production-boundary mutation. Helpers and layout do not trigger re-planning
when the plan remains valid.

Expand the selected region only when an external contract is invalidated.
Every mergeable state must be responsibility-closed, abandonment-safe, and fail
closed for unsupported semantics. Main is not an exploration surface.

Tests alone do not prove closure; keep declarations, repository/runtime facts,
inference, and unresolved surfaces distinct.

For a stable invariant, use counterexample and sink evidence, then the smallest
machine-enforceable boundary that excludes a concrete invalid transition. Do
not harden uncertain semantics or increase abstraction without one.

## Task-contract ownership

For new RepoDelta work, every substantive, non-automated implementation PR
has exactly one owning Task Issue. A Task Issue is the human-owned source of
intent, requirements, guardrails, and verification expectations for that PR;
the PR records the transformation, evidence, and acceptance state. An optional
Parent Issue may group Task Issues and carry program-level goals or shared
constraints, but never directly owns an implementation PR.

A Task Issue has at most one active implementation PR. A closed or abandoned
attempt remains historical evidence. Before a replacement PR starts, record an
explicit ownership transfer on the Task Issue and identify the replaced PR in
the replacement PR. Do not allow two PRs to claim the same Task Issue at once.

Use `Closes #<task-issue>` for the owning relation. A PR may additionally use
`Tracks #<parent-issue>` for program context, but that link is not requirement
authority. The exact authoring grammar, exemptions, replacement record, and
grandfathering policy are defined in the Issue and PR guides.

Only a mechanically generated, non-semantic change may be exempt, and its PR
must declare the applicable exemption. A human- or agent-designed change to
behavior, a public or workflow contract, evaluation authority, or repository
method is substantive even when a bot submits it. Do not retroactively invent
Task Issues for work authored before this policy; preserve those links as
grandfathered historical facts.

For non-trivial behavioral, responsibility, contract, data-flow, or
cross-component changes, follow `docs/agent-change-protocol.md`. Before an
Issue, commit, or PR, follow its corresponding guideline in `docs/`.
