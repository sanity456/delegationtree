# Review and release check

Scope: `contracts/delegation_tree.py` and its tests. This is an engineering review, not a formal security audit or a guarantee of Portal acceptance.

## Findings and controls

- The contract reserves integer authority recursively. Child creation requires the parent's assigned delegate, unique delegate identity, semantic containment, disjoint active sibling scopes, and enough unspent/unreserved/unpending capacity.
- Pending actions reserve quota before assessment. `spent + reserved + pending` is checked at delegation and action submission to prevent assessment-order races.
- Leader and validators independently repeat scope/action classification and compare structured results. Action IDs are single-use; uncertain results do not spend units.
- Node, action, mandate, scope, and description sizes are bounded. Branch revocation rejects spent, pending, or unresolved work.
- The mechanism is distinct from the workspace's flat permission/capability checks: it records a recursive tree with quota reservations and sibling-scope exclusion.

## Verification performed (2026-10-23)

- `genvm-lint check` passes with the pinned `py-genlayer` runner `1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`, using the compatible GenVM `v0.2.16` bundle.
- `genvm-lint typecheck --strict`: zero errors and zero warnings. Pyright emits informational unknown-type notices for GenLayer's dynamic nondeterministic APIs.
- Direct tests: 6 passed.
- StudioNet deployment finalized successfully. The Explorer/CLI source read-back matches the local contract source (normalized for line endings and trailing newline).
- Live StudioNet flow: mandate creation; 40 units delegated to a fresh test delegate under a child signage-only scope; a 15-unit action was judged `WITHIN_SCOPE` and `APPROVED`. Read-back showed the child spent 15 units, had zero pending units, and retained 25 units. Transaction receipts were checked for successful execution.

## Remaining submission gates

- Public source repository: https://github.com/sanity456/delegationtree. The release manifest records the repository and source-release commit.
- Evidence URLs must be entered and checked in the Portal while logged out. This local evidence file is not a substitute for Portal evidence.
- The initial CLI delegation attempt failed because the CLI coerced the numeric-looking string node ID `"1"` into an integer, while the contract correctly expects a string. It made no state change. The valid typed-string call through GenLayer JS succeeded. Use the recorded successful transaction, not the failed CLI attempt, as evidence.
- Live semantic coverage is one successful contained scope and one in-scope action. Sibling-overlap, uncertainty, quota contention, revocation, and abuse cases are covered by direct tests but not all repeated on StudioNet.

## Known limits

Quota units do not represent money, and wallet control does not establish legal authority or identity. The contract cannot prove that an approved action was performed. Disagreements may leave an action unresolved; there is no automatic appeal or expiry.
