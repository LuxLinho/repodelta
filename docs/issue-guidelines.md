# Issues

Use an Issue as the requirement-source contract, not as a copy of the future
PR transition record. Describe the result and review boundary without assuming
the implementation.

## Focused Issue before PR

For new non-trivial RepoDelta work, create one focused Issue before opening its
implementation PR. That Issue is the requirement-source contract, and the PR
that implements it begins with `Closes #<focused-issue>`.

If an existing Issue is broader than the proposed change, do not make the PR
pretend to complete that broader Issue. Create a focused Issue for the task and
link the broader Issue with `Parent: #<broader-issue>` for context, then have
the PR close the focused Issue. The PR may also say `Tracks #<broader-issue>`.
If no broader Issue exists, create the focused Issue directly.

Prefer these headings when applicable:

```text
Goal
Requirements
Guardrails
Verification expectations
Scope
Out of scope
Uncertainties
```

`Requirements`, `Acceptance criteria`, `Definition of done`, and `Success
criteria` are requirement aliases; prefer `Requirements` for consistent
authoring. Write one independently reviewable semantic obligation per list
item. Goals explain intent and guardrails constrain the solution; neither is a
requirement.

Keep optional sections optional. Use Scope for included responsibility and Out
of scope for explicit exclusions. Verification expectations name the kind of
evidence required without claiming that evidence already exists. Uncertainties
record dynamic or external surfaces that cannot yet be covered.

Do not put PR-level `Before`, `After`, authority transitions, migrations,
completion evidence, closure state, or `Completion conditions` in the Issue.
Those describe the implemented transition and belong in the PR. A PR may map
its transformation and completion claims to Issue requirements, but must not
copy the requirements as a second source of truth.

Mention a repository path or symbol only when it is part of the required
contract, not merely the expected implementation. Do not retrospectively create
a focused Issue for a PR that predates this rule or rewrite an older parent
reference as ownership.
