# Submission checklist

- [x] Standalone bounded contract; mechanism and boundaries documented
- [x] Per-creator namespaces/allowances, conserved quota, reserved descendant-node capacity, and per-node action limits/IDs
- [x] Concrete GenVM runner pin and source provenance
- [x] GenVM AST lint passed (3 checks); direct tests passed (11)
- [ ] SDK validate/typecheck completion — blocked by missing cached runner archive artifact; rerun in a clean SDK cache before claiming full validation
- [x] Corrected StudioNet deployment finalized successfully; deployed bytes matched corrected source
- [x] Live creator namespace, valid delegation, descendant-slot rejection, close, and closed-mutation rejection checks recorded with reads
- [x] Public repository and commit-pinned source link recorded in `release_manifest.json`
- [ ] Before submission, independently open every repository/source/Explorer URL while logged out and ensure Portal evidence uses corrected deployment details, not obsolete ones
- [ ] Do not submit until the SDK validation tooling limitation is resolved and the Portal preview is checked; reviewer acceptance cannot be guaranteed

Obsolete deployment `0x0a3Ed4cDc845B42f4c982610681bcFeDDFFf1A5C` is not submission-ready. Use only corrected deployment `0x40BA2E7200753aa11284C92Ec544c2D4795BA538` if/when all gates above are cleared.
