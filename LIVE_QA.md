# Live browser QA — 25 October 2026

Target: https://finite.akashanil.dev. Tests used two explicitly named QA accounts (`qa_live_1025_0400`, `qa_isolation_1025_0400`) rather than owner accounts. These accounts and their QA data remain; no existing user records were deleted. No OpenAI key was present; scheduler remained disabled; no AI budget ledger was created.

## Verified in the production browser

- Signup, onboarding and first real-source briefing generation after database repair.
- Wrong-password and duplicate-username errors, case-insensitive login, logout and protected-page redirect.
- Login/reload/deployment persistence; independent preferences and empty Passport in the second account.
- Interests and English/Malayalam preference changes persisted. Malayalam correctly explained that translation needs an AI key.
- All 12 initial stories opened; reading depth, source citation popover and source-index methodology displayed.
- Reading progress reached 12/12 and the finite ending; Passport counted one completed briefing. Manual regeneration produced a new 12-story list with different story IDs.
- Perspective Lens showed the honest single-publisher limitation and source excerpt.
- Connection Explorer's graph branch displayed both source excerpts; list alternative worked.
- Time Machine showed dated passages with missing-year context; coverage history displayed the source publication timestamp and citation.
- Missing Piece opened a sourced level-one exploration; Curiosity Challenge selected a prediction, revealed level two, and reached the depth limit. Saved journey and prediction persisted in Passport after reload and deployments.
- On-topic custom question returned cited passages; off-topic custom question was rejected with a clear explanation. Voluntary early expedition ending also worked.
- Corrected source-exclusion checkbox persisted as checked after save/reload.
- A transient deployment connection failure recovered via Try again without losing the session.

## Fixes

1. Host-user SQLite backups created WAL/SHM files the container UID could not write. Owner approved repairing ownership and installing protected deployment-script correction. Backups now execute as the application UID, check integrity, have a timeout, and stream to private host files. Successful subsequent automatic deployments and account writes verified the repair.
2. Empty HTTP status text plus non-JSON errors left signup silently failing. API helper now supplies a nonempty fallback; four mocked response cases pass.
3. Source-exclusion checkbox state was inverted relative to its heading. Checked now means excluded, with helper text.
4. Scheduled delivery wording now makes automatic preparation conditional; scheduler remains off.

## Boundaries

This is desktop production browser QA, not an exhaustive device/accessibility/security audit. No additional paid AI generation or translation was tested. Multi-publisher Perspective Lens comparison, every empty/error branch, PWA installation, and actual scheduled delivery were not exercised in this run. Existing automated tests cover additional API and feature cases. Container updates can briefly interrupt requests; zero-downtime rollout is not implemented.

## Deployment verification

Final [push-triggered run 40138920728](https://github.com/akashanil-dev/Finite/actions/runs/40138920728) passed all checks, both ARM64 image jobs and deployment. Oracle current-release is `5613245f8e53b6d1245ae541f0a8947c3ef4434d`, with healthy containers. Corrected schedule help was verified live; QA session signed out. The latest backup passed integrity_check and account writes survived deployment; no budget ledger was created.
