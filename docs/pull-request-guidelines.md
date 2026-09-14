# Pull requests

Title the PR around its responsibility or contract transition. For new
non-trivial RepoDelta work, begin with the focused Issue it implements:

```text
Closes #<focused-issue>
Tracks #<parent-issue>     # optional context for a child Issue
```

If a parent Issue is broader than this PR, create a focused child Issue first;
do not close the parent from the PR. Do not retrospectively add a focused Issue
to work authored before this rule.

Record applicable items only; do not fill absent concepts with template noise:

- parent transformation, responsibility, output, sinks, authority, and region;
- each changed derived result's provenance, scope, owner, and dependencies;
- each changed decision's orthogonal dependency and counterfactual;
- affected contracts, before/after flow, migrations, removals, and retained
  classifications;
- any material re-plan: invalidating evidence and changed target, authority,
  owner, contract, region, or merge evidence;
- contract, counterfactual, sink-level, and final-tree evidence;
- invariant enforcement and why it does not freeze uncertain semantics;
- unresolved surfaces;
- responsibility closure, contract closure, abandonment safety, and parent
  completion as separate states.

A derived result is not automatically cross-consumer truth. If consumer-local,
state why the projection is allowed and does not alter canonical facts.
Consumers must not silently produce or re-decide upstream semantics.

Use `Before`/`After` for state transitions and `Before topology`/`After
topology` only for topology claims. Put concrete file/symbol identities in
Markdown code spans so RepoDelta can focus structure without treating state
prose as proof.

Explain why the tree remains valid if the parent stops. Unsupported or
incomplete semantics must fail closed.

Keep the PR Draft while responsibility, contracts, or a merge gate is unsettled.
Mark ready only after auditing the final tree. If a parent remains open, link
the focused child Issue that owns this PR's obligations and stop conditions.
