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

## Completed delegated action

A fresh mandate `review_action_20261023` was created under participant 2, who delegated the accessible-signage sub-scope and 40 units to participant 3 with one child slot. Participant 3 submitted a 15-unit signage action. Validators agreed it fit the delegated scope; the final action readback was `APPROVED` / `WITHIN_SCOPE`, with 15 spent, zero pending, and 40 still reserved by the root.

| Step | Explorer transaction | Status / execution / votes |
| --- | --- | --- |
| Create review action mandate | https://explorer-studio.genlayer.com/tx/0x205453ffcb8bd179121a2db46beea447e7bc713f8e1f081447005e16812f4b04 | FINALIZED / SUCCESS / `[1,5,1,5,1]` |
| Delegate 40 units and one child slot | https://explorer-studio.genlayer.com/tx/0xaecc46d98af78396a4222a5e600ccea82c2b8a66114c661db74668da01ad65b9 | FINALIZED / SUCCESS / `[5,5,1,1,1]` |
| Submit 15-unit child action | https://explorer-studio.genlayer.com/tx/0x96229b2d6d63dbf827fbc7a4cdea800d7965766a0641b7601da3f96176261b87 | FINALIZED / SUCCESS / `[1,5,1,5,1]` |
| Assess and approve within-scope action | https://explorer-studio.genlayer.com/tx/0xb22889f3d3579cdfa37de229e446a8d47bd1ee08db62d905dc05bc6fb737d791 | FINALIZED / SUCCESS / `[1,5,5,1,1]` |

Final mandate readback key: `0x380516bf492a6fb052e04a4ceeeb2f8d8e3b1dde|review_action_20261023`; action key `2:accessible_signage`; child capacity 40, spent 15, pending 0; root reserved 40. These abstract units record authorization accounting; no funds or real-world work were transferred or verified.

## Obsolete deployment — do not submit

- Address: `0x0a3Ed4cDc845B42f4c982610681bcFeDDFFf1A5C`
- Deployment transaction: `0xc4320389644748734976b51368e0ef47339274f8325c2144bb9559b031be99fa`
- It runs the earlier shared-capacity version without reserved child node slots and does not match the corrected source.
