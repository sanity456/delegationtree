# Submission checklist

- [x] Standalone bounded contract; mechanism and boundaries documented
- [x] Per-creator namespaces/allowances, conserved quota, reserved descendant-node capacity, and per-node action limits/IDs
- [x] Concrete GenVM runner pin and source provenance
- [x] GenVM AST lint passed (3 checks); direct tests passed (11)
- [x] SDK validation passed using the pinned GenVM `v0.2.16` bundle; standard typecheck passed with zero diagnostics
- [ ] Optional strict Pyright mode reports 24 diagnostics, primarily redundant type guards and unknown SDK/API types; disclosed in `STUDIONET_EVIDENCE.md` (no source/deployment change made solely to silence these)
- [x] Corrected StudioNet deployment finalized successfully; deployed bytes matched corrected source
- [x] Live creator namespace, valid delegation, descendant-slot rejection, close, and closed-mutation rejection checks recorded with reads
- [x] Successful delegated action assessed on StudioNet; `APPROVED` readback records 15 units spent from the child's 40-unit allocation
- [x] Public repository and commit-pinned source link recorded in `release_manifest.json`
- [ ] Before submission, independently open every repository/source/Explorer URL while logged out and ensure Portal evidence uses corrected deployment details, not obsolete ones
- [ ] Before submission, check the Portal preview; reviewer acceptance cannot be guaranteed

Obsolete deployment `0x0a3Ed4cDc845B42f4c982610681bcFeDDFFf1A5C` is not submission-ready. Use only corrected deployment `0x40BA2E7200753aa11284C92Ec544c2D4795BA538` if/when all gates above are cleared.
