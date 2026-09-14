# Commit messages

Commits in a branch or Draft PR are checkpoints; merge acceptance applies to
the final tree. Squash exploratory checkpoints when policy permits.

Name the responsibility or contract transition, not the edited files:

```text
<type>(<responsibility>): <imperative transition>
```

Examples:

- `refactor(verification-identity): unify selector and observation contracts`
- `fix(topology-proof): require ordered edge witnesses`
- `refactor(review-projection): consume canonical membership directly`

When useful, mention migrated endpoints, changed boundaries, removed bypasses,
and preserved contracts. Never call unconsumed or exploratory code canonical.
When hardening an invariant, name the invalid semantic transition being
prevented rather than only the type, factory, test, or gate used to prevent it.

For substantive Task-Issue work, an optional checkpoint footer may record the
same owner as the PR:

```text
Task: #<task-issue>
```

It is a traceability aid, not a second requirement contract; the owning
relation is declared only by the PR's `Closes #<task-issue>`. Do not use a
Parent Issue as `Task`, and do not use a replacement PR's old PR number as its
Task Issue.
