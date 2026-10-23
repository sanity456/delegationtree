# StudioNet release evidence

Corrected deployment verified on 2026-10-23 against public source release commit `d2d66ac2fcb13e824971e68eb4063d16448e8501`.

- Contract: `0x40BA2E7200753aa11284C92Ec544c2D4795BA538`
- Deployment transaction: `0x46a1d37af681edd97b424617fb2130120b672823b3ce4da708bfe820b13defa5`
- Explorer: https://explorer-studio.genlayer.com/address/0x40BA2E7200753aa11284C92Ec544c2D4795BA538
- Deploy transaction: https://explorer-studio.genlayer.com/tx/0x46a1d37af681edd97b424617fb2130120b672823b3ce4da708bfe820b13defa5
- Finality/result: `FINALIZED`, `MAJORITY_AGREE`, execution `SUCCESS`; validator votes agreed.
- Deployed source was byte-for-byte equal to local corrected source; SHA-256 `a78b92b95c657e85197609ca8bc3143f73eafe48f7ae7999cf8df0083854fc4e`.
- Test wallets were newly generated and isolated for this Batch D run; they were not reused from another batch/user or workspace wallet.

## Focused live checks

All listed transactions finalized. Expected rejection tests produced execution `ERROR`; they were not treated as success-path passes.

| Check | Transaction | Result |
| --- | --- | --- |
| Creator A creates `capacity_00` | `0xdaad09a48d7dc259e9e8e5d6e00a9ca55bb54fcbe31dbdbb612b2dd264883bea` | SUCCESS |
| Creator B independently reuses `capacity_00` | `0x7eb2a548e3e194226f294615baa66f43aab6958599cb1915037ecdd0de4f8b9a` | SUCCESS; readback confirmed separate creator-qualified records |
| Create node-capacity test mandate | `0xba5fdfa6b036bca0ad3ae26e980c28ca0c06808d404982cb3881b7ca01b44bc4` | SUCCESS |
| Delegate within parent scope and reserved node slots | `0x594610848f3b22278186e94d29b195d277964d68cc71e1a78217fc61f3dbfc73` | SUCCESS; state showed one reserved child slot |
| Child exceeds reserved descendant-node slots | `0xefc765ab11c612d341f3f5407d1ec12f829c77fe1525fc4db87b63c9657bb7f5` | Expected ERROR; state readback confirmed no extra node/allocation |
| Close mandate | `0xfec26eb5d80e53563f945f039fd1723557b2a09d9efc5efe2975128e7ea97707` | SUCCESS |
| Mutate closed mandate | `0x42081c3cff7d499fa437b18c16a82ed25825d671c674add05bf61bf3c9d185cb` | FINALIZED, expected ERROR; fresh readback remained `CLOSED` with same two nodes, reserved/spent amounts and empty actions |

Local verification: GenVM AST lint passed (3 checks); SDK validation passed; standard typecheck passed with zero diagnostics; direct tests passed (11 tests). Strict Pyright mode reports 24 diagnostics, primarily redundant runtime type guards and unknown types from dynamic/SDK APIs; it is stricter than the standard check and does not indicate an SDK validation failure. No contract source was changed for these optional strict-mode diagnostics. `git diff --check` passed. No reviewer outcome is guaranteed.

## Obsolete deployment — do not submit

- Address: `0x0a3Ed4cDc845B42f4c982610681bcFeDDFFf1A5C`
- Deployment transaction: `0xc4320389644748734976b51368e0ef47339274f8325c2144bb9559b031be99fa`
- It runs the earlier shared-capacity version without reserved child node slots and does not match the corrected source.
