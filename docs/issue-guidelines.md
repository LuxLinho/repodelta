# Issues

Use an Issue as the requirement-source contract, not as a copy of the future
PR transition record. Describe the result and review boundary without assuming
the implementation.

## Task Issues and Parent Issues

For new RepoDelta work, choose one Issue role before implementation begins:

- A **Task Issue** is the one human-owned requirement-source contract for one
  substantive implementation PR. Start it with `Type: Task` and, when
  applicable, `Parent: #<parent-issue>`.
- A **Parent Issue** groups Task Issues for a campaign, epic, or program. Start
  it with `Type: Parent`. It may state program-level goals and cross-task
  constraints, but it does not directly own an implementation PR.

A Task Issue must be created before the PR that implements it. It has at most
one active implementation PR; active means any open PR, including a Draft. A
PR closes its owning Task Issue with `Closes #<task-issue>`; a parent reference
is context only and must not be written as a closing reference. Once the Task
Issue is closed by its accepted PR, later substantive work starts a new Task
Issue rather than reopening the completed contract.

When an implementation attempt is abandoned, keep that PR in the Task Issue's
history. Before a replacement begins, add `Execution replacement: #<old-pr>`
to the Task Issue and have the replacement PR declare both `Closes
#<task-issue>` and `Replaces #<old-pr>`. The new PR takes over execution; it
does not create a second requirements contract.

Only these mechanically generated, non-semantic changes may be exempt:

- `format-only`: a deterministic formatter changes layout or whitespace only;
- `generated-artifact-sync`: committed derived artifacts are regenerated from
  unchanged canonical inputs; or
- `release-metadata`: approved release automation updates metadata from an
  already accepted release decision without changing source, dependencies, or
  runtime configuration.

Its PR must state `Exemption: <category>` and its boundary. Dependency, runtime,
configuration, schema, evaluation-authority, workflow-method, or agent-designed
changes are never exempt. Bot submission does not itself make a change exempt.

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
contract, not merely the expected implementation.

Do not retrospectively create a Task Issue for a PR that predates this policy
or rewrite an older parent reference as ownership. Mark that relation
grandfathered in the PR record if clarification is needed. For new substantive
work, an Issue-free implementation PR is not permitted.

### Relationship examples

```text
# Valid Task Issue
Type: Task
Parent: #<parent-issue>

# Valid PR for that Task Issue
Closes #<task-issue>
Tracks #<parent-issue>

# Valid replacement PR after #401 was abandoned
Closes #<task-issue>
Replaces #401

# Valid exempt mechanical PR
Exemption: generated snapshot synchronization; no behavior, contract,
evaluation-authority, or repository-method change

# Invalid: a Parent Issue cannot be the owning Issue
Closes #<parent-issue>

# Invalid: two open PRs both declare Closes #<task-issue>
```
