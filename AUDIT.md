# Review and release check

Scope: `contracts/delegation_tree.py` and its tests. This is an engineering review, not a formal security audit or a guarantee of Portal acceptance.

## Findings and controls

- **Fixed before corrected deployment:** the initial shared deployment let any caller consume the single global 20-mandate allowance. It also gave every child access to the shared 15-node mandate cap and used mandate-global action IDs/caps, so a delegate could crowd out other branches. The corrected source gives each creator an isolated mandate namespace/allowance, reserves descendant-node slots from parent to child, applies action limits and IDs per node, and rejects post-close mutations. The old deployment does not contain these fixes and must not be submitted.

- The contract reserves integer authority recursively. Child creation requires the parent's assigned delegate, unique delegate identity, semantic containment, disjoint active sibling scopes, and enough unspent/unreserved/unpending capacity.
- Pending actions reserve quota before assessment. `spent + reserved + pending` is checked at delegation and action submission to prevent assessment-order races.
- Leader and validators independently repeat scope/action classification and compare structured results. Action IDs are single-use; uncertain results do not spend units.
- Node slots, per-node actions, per-creator mandates, scope, and description sizes are bounded. Branch revocation rejects spent, pending, or unresolved work.
- The mechanism is distinct from the workspace's flat permission/capability checks: it records a recursive tree with quota reservations and sibling-scope exclusion.

## Verification performed locally (2026-10-23)

- `genvm-lint check` passes with the pinned `py-genlayer` runner `1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`, using the compatible GenVM `v0.2.16` bundle.
- `genvm-lint typecheck --strict`: zero errors and zero warnings. Pyright emits informational unknown-type notices for GenLayer's dynamic nondeterministic APIs.
- GenVM lint/SDK validation passes for the corrected source with the pinned runner.
- Direct tests: 11 passed, including per-creator limit/namespace isolation, node-scoped action caps and IDs, parent-reserved child-node slots, close-state immutability, and forged validator output.
- **Not yet verified:** no corrected StudioNet deployment or live abuse demonstration has been run. Prior deployment and receipts cover only the vulnerable source.

## Remaining submission gates

- Public source repository: https://github.com/sanity456/delegationtree. The release manifest records the repository and source-release commit.
- Evidence URLs must be entered and checked in the Portal while logged out. This local evidence file is not a substitute for Portal evidence.
- Push corrected source, deploy that exact pushed revision, and verify raw deployed bytes against the public Git blob.
- Demonstrate live that one creator cannot consume another's mandate allowance and an authorized child cannot use node slots reserved by the parent for other branches; read back all state and receipt results.
- Replace the stale deployment/receipt links and manifest with fresh corrected deployment evidence, then verify all public links anonymously.

## Known limits

Quota units do not represent money, and wallet control does not establish legal authority or identity. The contract cannot prove that an approved action was performed. Disagreements may leave an action unresolved; there is no automatic appeal or expiry. Creator and per-node allowances are permanent lifetime caps; closed or revoked records do not restore slots.
