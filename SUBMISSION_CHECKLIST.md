# Submission checklist

- [x] Standalone bounded contract with a mechanism distinct from workspace projects
- [x] Fixed global-cap exhaustion: per-creator mandates, parent-reserved child node slots, and per-node action limits/IDs
- [x] Pinned GenVM runner and source provenance
- [x] Static GenVM lint and semantic validation pass
- [x] Strict typecheck reports zero errors/warnings with informational SDK typing notices; direct tests: 11 passed
- [ ] Deploy corrected source and compare raw deployed bytes to the pushed Git blob
- [ ] Demonstrate isolated creator capacity and parent-reserved descendant-node capacity on StudioNet
- [ ] Record fresh successful and expected-failure receipts with execution results and read-backs
- [x] Publish repository publicly and record repository URL and source-release commit in `release_manifest.json`
- [ ] Add/verify GitHub Repository, GitHub source file, release manifest, and Explorer contract/transaction links in the Portal while logged out
- [ ] Recheck every link anonymously and pin the source evidence to the corrected deployment commit

The old deployment is not submission-ready. Do not resubmit it. Submission readiness depends on every corrected deployment/evidence gate above; no reviewer outcome is guaranteed.
