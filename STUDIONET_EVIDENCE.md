# StudioNet evidence

Test date: 2026-10-23. Network: GenLayer StudioNet (`chainId 61999`, `https://studio.genlayer.com/api`). The deployment and test accounts were created in an isolated CLI profile; no pre-existing workspace account was used. Private keys and keystore passwords are intentionally not recorded here.

## Deployment

- Contract: `DelegationTree`
- Contract address: `0x0a3Ed4cDc845B42f4c982610681bcFeDDFFf1A5C`
- Deployment transaction: `0xc4320389644748734976b51368e0ef47339274f8325c2144bb9559b031be99fa`
- Deployment receipt: `FINALIZED`; consensus `MAJORITY_AGREE`.
- Local source: `contracts/delegation_tree.py`
- Local SHA-256: `81F39046A2189C2B7058E82515B9BB96ADFA66C8C4625DDB86A21B490FC45D7C`
- `genlayer code <address>` read-back matched the local source after normalizing line endings and trailing newline. The on-chain schema exposed the expected 8 methods, including two read-only views.

## Live flow and read-back

- Mandate: `batchd_mandate_20261023`; root capacity: 100 abstract units.
- Creator/test wallet: `0x94ce68c866439c9cf88bd3cbcdaa4c1aeb533873`; delegate: `0xbc8e12997be8f1269a10b9636a6c84708efd9347`.
- Mandate creation transaction: `0xa4822f353cb78824ab9cae4458ba0afd5bcc97d9e61c6149a83207968ab04ddd` — finalized, leader execution `SUCCESS`.
- Delegation transaction: `0x6a4d22d27d8c1503d2c1f0716ca2ad35478dcafa9874ec10cae762ce823a8429` — finalized, leader execution `SUCCESS`; validators accepted the signage-only child scope and 40-unit reservation.
- Action submission transaction: `0xe0af3b1234c7e2ab35cd9f5c3d4d9511e7f4377c9473187c9b2fa0bfd9d5a4b0` — finalized, leader execution `SUCCESS`.
- Assessment transaction: `0x2653ea9852db5d8c35c4187f380ba84224fb9a09535fe7f755c8a59c07ac8eb9` — finalized, leader execution `SUCCESS`.
- `get_action` read-back reported `WITHIN_SCOPE` / `APPROVED`, node `2`, units `15`. `get_mandate` read-back showed node 2 with capacity 40, spent 15, pending 0; root reserved 40 of 100.

## CLI serialization note

The first delegation attempt (`0x0045ccfa66421b94ab3866948caaf92954a35c39de6e95ee0036f3c4a70d59a9`) did not change state: the CLI converted node ID `"1"` to integer `1`, causing `AttributeError: 'int' object has no attribute 'strip'`. The successful retry used the GenLayer JS client with the node ID passed as a true string. This is a CLI argument-coercion issue, not a source change; cite only the successful transaction above.

This file records local CLI evidence. Add direct StudioNet and Explorer URLs to the Portal submission after the public repository and commit are ready.
