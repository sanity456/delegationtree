# Batch D2 — DelegationTree

DelegationTree is a reusable GenLayer contract for distributing bounded authority through a hierarchy. Every child receives a reserved portion of its parent's integer quota and a semantic sub-scope that validators must find contained by the parent and disjoint from active sibling scopes. A parent also reserves a finite number of descendant-node slots for each child. Later actions consume quota only after independent validators agree that the action fits the assigned scope.

## Mechanism and distinction

The mechanism is recursive authority reservation: children cannot spend or delegate their parent's reserved capacity, sibling scopes cannot overlap, and unused branches can be revoked only before any action is pending or any units have been spent. This is different from `agent-permission-check` and `credentialscope`, which check a designated action against a capability or credential registry rather than create a nested tree with nonoverlapping semantic scopes and conserved quota.

## Boundary

GenLayer judges semantic containment and action fit. Deterministic code enforces tree ownership, quota and node-slot conservation, per-node action limits, replay protection, bounded lifecycle, and revocation. Each creator receives an independent lifetime allowance of 20 mandates; mandate IDs are scoped by creator. Action IDs are scoped by node, so separate delegates cannot collide or overwrite one another's requests. Units are abstract authorization units, not money or tokens. This contract does not authenticate identities beyond wallet control, establish legal authority, or execute the described real-world action.

## Verify and release

    genvm-lint check contracts/delegation_tree.py
    genvm-lint typecheck contracts/delegation_tree.py --strict
    python -m pytest tests/direct -q -p no:cacheprovider

The earlier deployment used a shared global registry and did not reserve descendant-node slots. It must not be submitted. The corrected source is under local verification; deployment, source-byte comparison, and refreshed live abuse evidence are still required. See `STUDIONET_EVIDENCE.md`, `release_manifest.json`, and `SUBMISSION_CHECKLIST.md` for release gate status.
