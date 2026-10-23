# Security and trust limits

- Wallet authorization proves control of the submitting address, not an organization's real-world delegation.
- Scope text and action descriptions are public caller declarations. Validators adjudicate meaning but cannot verify the resulting real-world performance.
- Each accepted judgment is independently recomputed and all stored decision fields are compared exactly. Malformed and uncertain results fail closed.
- Quota is reserved before delegation. Every action ID is single-use. Only the assigned delegate can submit against its node.
- Each creator has an isolated 20-mandate lifetime allowance. The parent explicitly reserves child descendant-node slots, so an authorized child cannot consume node capacity the parent kept for another branch.
- Action capacity is capped per node, and action IDs are node-scoped.
- A branch can be revoked only before use or unresolved work; otherwise existing reservations remain frozen.
- Mutating calls, including revocation and action assessment, reject a closed mandate.
- Abstract units have no monetary value. No funds or external rights are transferred.
- This is an unaudited prototype. Manual review is not a formal security audit.
