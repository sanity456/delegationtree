# Architecture

1. A creator opens a mandate with one root scope and a finite integer quota.
2. A node's assigned delegate may allocate part of its remaining quota to one child. Validators check that the child scope is inside the parent and disjoint from every active sibling scope. Any missing, uncertain, or overlapping judgment rejects the delegation.
3. The child may repeat the same operation within its own quota, producing a bounded delegation tree.
4. A delegate submits a uniquely identified action request against its node. Validators independently classify whether it fits the frozen scope. Code consumes quota only on `WITHIN_SCOPE`; unclear or outside requests do not consume it.
5. A parent may revoke an unused subtree only if no node in it spent quota and it has no pending or unresolved action. The reservation is then released to that parent.

The invariant at every node is `spent + reserved + pending <= capacity`. The root cap never changes, delegation reserves quota before a child acts, and each action reserves quota when filed so assessment order cannot give one pending request another's allocation. Semantic judgment gates scope changes and action authorizations, while the contract calculates all limits and state transitions.

Bounds: 20 mandates per deployment, 15 nodes per mandate, 20 action requests, 512 UTF-8 bytes per scope, 256 bytes per action description, and 1,000,000 units per root. IDs are permanent within a mandate. One deployment serves independent work programs.
