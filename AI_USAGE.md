# AI usage record

Finite was built at Devin Hacks Kochi with **Devin** (Cognition's AI software engineer) as the main coding assistant. This file briefly records what AI tools actually contributed. It omits secrets, private data and full chat transcripts.

## Event build log

| Date and time (IST) | Tool / model | Task | Assistance and affected files | Human review / corrections | Validation and result |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24, about 20:20–21:00 | Devin | Product analysis and planning | Analysed Akash's concept doc, suggested solutions for content sourcing, hallucination, cost and neutrality, proposed the scope, stack and naming options, checked OpenAI pricing for the $50 budget, and tested which publisher RSS feeds are reachable | Akash chose the name ("Finite"), the stack, mobile-first, India-first with Malayalam, the source credibility index, and that the feed must be finite | Planning only |
| 2026-10-24, about 21:03–22:32 | Devin | MVP implementation | Wrote `backend/app/*`, `frontend/src/*`, project config and `README.md` | Akash directed features and repository changes. Line-by-line code review is pending | tsc, eslint and `next build` passed; API smoke test passed without a key (see CHANGELOG) |
| 2026-10-24, about 22:43 | Devin | Event documentation | Adapted the template docs for Devin Hacks Kochi using the official website and Luma page | Akash asked for the update and supplied the code freeze time | Event details checked against the official pages |

## Use inside the product

When `OPENAI_API_KEY` is set, Finite itself uses OpenAI models at runtime: `gpt-6-luna` for classification, summaries, claim verification and Malayalam translation, `gpt-6.1-sol` for rabbit-hole writing, and `text-embedding-3-small` for grouping duplicate stories. The model may only use passages the app retrieved, every claim must cite a source, and unsupported claims are dropped. Without a key, the app runs in extractive mode and no AI is used at runtime.

## 2026-10-24T23:08:19+05:30 — Codex context review and checkpoint

Reviewed the existing handoff document, available project chat messages and implementation; prepared the shared-context documentation checkpoint at the owner’s request. Preserved prior authorship claims without attributing the original context draft to Codex. Human review of this checkpoint is pending. Documentation diff checked; no runtime tests performed.

## 2026-10-24T23:12:02+05:30 — Codex Perspective Lens

Implemented the comparison endpoint and expandable UI, publisher deduplication, strict citation validation and fail-closed AI verification. Added six fixture/API tests and updated project records. Owner authorized implementation and separate commit/push checkpoints; human code and UI review remain pending. Tests, backend import, TypeScript and ESLint passed. Production build blocked by local port-binding permissions; real-key generation and browser review not performed. Corrected invalid inline markup during source review.

## 2026-10-24T23:18:29+05:30 — Codex browser validation and corrections

Used the in-app browser against the production frontend and isolated QA backend to test Perspective Lens states, citations, retry and responsive layout. Found and fixed short-lead omission, ambiguous citation labels and wrapping toggle. Added a regression test. Diagnosed build recovery through a fresh generated cache and local port permission; no configuration workaround required. Seven tests, import, tsc, ESLint and production build pass. Human review and live-key AI evaluation remain pending; fixture AI checks are not live model validation.

## 2026-10-24T23:28:09+05:30 — Codex Curiosity Challenges

Implemented optional prediction/reveal/skip flow, saved prediction display and depth-safe exploration caching. Added depth-cache and journey-persistence regression tests. Nine tests and import pass without a key; frontend core checks pass. Human review and browser QA pending. Owner instructed work without a key and to stop before live AI validation.

## 2026-10-24T23:32:53+05:30 — Codex Curiosity Challenges browser QA

Tested the production UI with an isolated no-key backend, deterministic source passages and injected exploration/save failures. Fixed focus, save error/retry, empty connections and misleading loading text. Verified prediction persistence, skips, two-level ending and mobile layout in the browser. Nine tests/import previously passed; final tsc/ESLint/build pass. No key was used. Human review and live AI quality evaluation remain pending; stopped before that stage per owner instruction.

## 2026-10-25T00:08:44+05:30 — $1 AI budget guard

Added persistent, atomic conservative reservations before every uncached OpenAI chat/embedding call (`budget.py`, `llm.py`), a read-only `/api/ai-budget` endpoint, no automatic SDK retries, and request size/output/count limits. Failed requests keep reservations. Unknown models fail closed. Four focused tests cover concurrency, exhaustion, failures/cache and invalid requests; backend import passed. Live AI/browser checks follow in a separate checkpoint. This is an installation allowance, not an account-wide cap or actual billing meter.
Codex implemented and tested this change; human review pending.

## 2026-10-25T00:15:26+05:30 — Repair live AI JSON requests

Live calls returned HTTP 400 because JSON mode requires JSON in the input message, not only instructions. `llm.py` now adds that instruction to the input and rejects non-object JSON. `analysis.py` regenerates extractive cached analysis when AI mode becomes available, and handles empty source lists. The wrapper regression test checks JSON input and standard service tier. Live classification identified both stored Jamia articles as protests/education/elections; embeddings grouped them together. Browser verified generated summaries, tailored questions, Missing Piece and Perspective Lens. Fifteen backend tests and import pass. Remaining grounding/UI refinements are a separate checkpoint.
Codex diagnosed the real API rejection and implemented the fix; human review pending.

## 2026-10-25T00:17:27+05:30 — Fail-closed AI verification and live browser QA

Rabbit-hole nodes now require exactly one explicit positive verdict; failed/malformed/missing/duplicate verdicts drop the claim. Timeline events and their dates are verified too; invalid refs are removed and empty results are marked insufficient. Exploration cache moved to v3. Translation rejects malformed/empty entries. Corrected off-topic UI wording (retrieval can already have run). Files: `rabbithole.py`, `translate.py`, `rabbit-hole.tsx`, `tests/test_ai_validation.py`.

Validation: 16 backend tests and import pass; TypeScript, ESLint and QA production build pass. Real API classification and embeddings passed on two stored Jamia articles. Production browser tested AI summaries, Missing Piece, tailored questions, Perspective Lens, two levels of cited exploration, timeline, unsupported-claim removal, challenge prediction/reveal, ending, Passport persistence, Malayalam rendering, unrelated custom-question rejection and corrected wording. No console errors on the three tested pages. QA used a database copy with scheduling disabled; real API calls used the shared persistent allowance. 15 requests reserved $0.776700; $0.223300 remains. These are conservative reservations, not actual billed spend. Existing publisher material and live Wikipedia retrieval were used, not synthetic AI responses.

Limitations: sample coverage only; Malayalam editorial accuracy requires human review. Browser viewport override did not take effect in this run, so live-AI mobile layout is not newly verified (earlier extractive mobile QA remains valid). Scheduler/full-ingestion live operation and account-wide billing are outside this test.
Codex performed implementation and live QA; owner review pending. No credentials recorded.

## 2026-10-25T00:32:15+05:30 — Time Machine implementation

Added a lazy story-page Time Machine with source-extractive dated passages, earlier/current grouping, a separate unresolved-date section, and publication/update coverage history. New `backend/app/time_machine.py` and GET `/api/stories/{id}/timeline`; new `frontend/src/components/time-machine.tsx`, story-page integration and five focused tests. Complete quotations retain citations; missing years are not inferred; multiple dates remain unresolved; up to 12 event passages. No OpenAI calls or extra retrieval.

Validation: 21 backend tests and import pass. Frontend tsc/ESLint/production build pass. Browser QA follows separately. Limitations: English date patterns only, stored source passages rather than a complete historical archive, no independent fact verification or automatic translation.
Codex implemented and checked the feature; human review pending.

## 2026-10-25T00:35:42+05:30 — Time Machine browser QA and date correction

Browser fixtures exposed a false year: “2000 residents”. Standalone years now require temporal context, while connected alternatives/ranges stay unresolved. Undated-year passages retain source order rather than arbitrary alphabetical order. Added count/currency regression assertions in `test_time_machine.py`.

Verified in the production browser: real stored Jamia passages, 2005/2006 source disagreement, missing-year sections, citation popover/link, event/coverage switching, publication/update timestamps, collapse/reopen, no-dates empty state, injected 503 and successful retry, and the corrected numeric-count fixture. Real/empty pages had no console warnings/errors; the fixture's injected 503 was expected. Desktop layout has no horizontal overflow. Mobile-specific QA was not performed in this checkpoint. Backend 21 tests/import and frontend tsc/ESLint/build pass. No AI calls; ledger remains $0.776700 reserved and $0.223300 available. QA database isolated; main API restarted with scheduler disabled.
Codex performed browser QA, fixed the date bug and reconciled documentation; human review pending.

## 2026-10-25T00:44:56+05:30 — Connection Explorer implementation

Added source-backed cross-story comparisons in `connections.py`, GET `/api/stories/{id}/connections`, and the lazy story-page `connection-explorer.tsx`. Up to three inline comparisons among the latest 200 stored stories; saved concepts require literal evidence on both sides. Excludes overlapping article clusters/URLs, blocked sources, dominant excluded topics and unselected languages. No new AI calls, network retrieval or schema changes. Each comparison ends with original-source citations; no recursive recommendation loop.

Validation: 25 backend tests and import pass; frontend TypeScript, ESLint and production build pass. Browser QA follows separately. Limitations: shared mentions do not establish causality; exact matching misses synonyms/translations; saved concept quality and stored coverage bound discovery.
Codex implemented and checked the feature; human review pending.

## 2026-10-25T00:46:14+05:30 — Connection Explorer browser verification

Production desktop browser QA passed on an isolated database with the API key disabled: real stored AI-election story linked to two other stories via cited ChatGPT mentions; both source excerpts and original publisher citation links rendered correctly. Injected 503 displayed a useful error and retry recovered; empty fixture, collapse/reopen and finite ending passed. No horizontal overflow at 1280px; empty page console clean (the injected 503 on the real-story page was expected). No feature defects found in this sample. Mobile-specific QA not performed.

25 backend tests/import and TypeScript/ESLint/production build passed at implementation checkpoint. No AI calls; ledger unchanged at $0.776700 reserved, $0.223300 remaining, 15 requests. Shared mentions are not causal relationships; richer semantic links remain future work.
Codex performed browser verification and documentation reconciliation; human review pending.

## 2026-10-25T01:14:28+05:30 — Interactive knowledge graph

Added a finite selectable knowledge map to Connection Explorer with a starting story, labelled shared-mention branches, keyboard-operable story nodes, selection state and cited evidence on both sides. List view retained; no recursive expansion, new dependencies, backend changes or AI calls. Files: `connection-explorer.tsx`, `story-view.tsx`. TypeScript, ESLint and production build passed. Browser QA pending. Literal-mention discovery limitations remain.
Codex implemented and validated the map; human review pending.

## 2026-10-25T01:16:43+05:30 — Knowledge graph browser QA and connector fix

Fixed a disconnected visual branch line discovered in browser inspection. Production desktop QA verified node selection by click and Enter, selection/evidence updates, citation popovers and original links, map/list switching, injected error/retry, empty state and finite ending. Corrected connector visually rechecked. No console warnings/errors after reload; no horizontal overflow at 1280px. Mobile-specific testing remains pending. 25 backend tests, TypeScript, ESLint and production build pass. QA used an isolated database with API key disabled; no provider calls.
Codex implemented the visual fix and performed QA; human review pending.

## 2026-10-25T01:37:34+05:30 — Accounts, sessions and per-user data

Implemented username/password registration, sign-in, 30-day opaque cookie sessions, sign-out, salted scrypt password hashing and persistent login throttling. No reset/email verification or complex password rules. Added API authentication, exact credentialed CORS, browser-write origin/header protection, local-only admin grants and additive ownership migration. Profiles, briefing dedup/history/read state and Passport journeys are isolated per account; scheduler iterates onboarded accounts. Old local history remains unassigned until explicit local claim; no automatic first-user ownership. Frontend login/registration, account gate and Settings sign-out added.

Validation: auth/ownership, session expiry/revocation, cookie flags, CSRF, login throttling, legacy claim and per-user briefing tests pass; frontend types/lint/build pass. Production desktop browser verified protected-page redirect, registration, reload persistence, saved preferences, wrong-password rejection, sign-out, a second account with empty preferences, and successful case-insensitive sign-in restoring the first account's preferences. Tests used a copied DB and no AI key. Mobile/assistive-technology audit and production HTTPS verification remain pending; no API allowance used.
Codex implemented auth, tests and browser QA; human review pending.

## 2026-10-25T01:39:40+05:30 — Oracle ARM64 container and CI/CD preparation

Prepared separate unprivileged backend/frontend images, Next standalone output, Compose with persistent data/budget volume and resource ceilings, existing-Caddy site/network integration, and GitHub Actions checks plus native ARM64 build/smoke/publish jobs. SSH deployment is gated by FINITE_DEPLOY_ENABLED and the production environment; health checks, SQLite backups and previous-image rollback are included. Target is finite.akashanil.dev on the same Oracle Ampere host as Tuxos. Tuxos deployment was inspected read-only; Finite code was not imported from it. Added server setup and Codex CLI handoff documentation.

Validation: 34 backend tests; import, route type generation, tsc, zero-warning ESLint, standalone production build; Compose configuration and shell syntax pass. Browser auth flow passed on an isolated no-key DB. Local Docker daemon access is unavailable (sudo needs a password), so image builds and container smoke tests must run in CI; no Oracle deployment or public HTTPS verification claimed. No AI calls; ledger unchanged at $0.997112 reserved / $0.002888 remaining, 32 requests.
Codex prepared deployment files and docs from the existing Tuxos operational pattern; human/server review pending.

## 2026-10-25T01:45:05+05:30 — Hosted ARM64 validation and local auth handoff

GitHub run https://github.com/akashanil-dev/Finite/actions/runs/40128562535 succeeded for code commit `9d246ab5172e9eab681eb213a276aba2b0b8e2f0`: code checks, both native ARM64 image builds, no-key container health smoke tests and GHCR pushes. Deploy job skipped; FINITE_DEPLOY_ENABLED is unset. Local standalone frontend and authenticated API restored on 3000/8000 with scheduler disabled. Pre-auth SQLite and budget backups saved under gitignored backend/data/backups; no existing history was automatically assigned to an account.

Deployment script simulation (mocked Docker, temporary filesystem) passed successful release, valid SQLite backup, pull-failure preservation and health-failure rollback checks. This is not Oracle deployment verification. Server setup, Caddy integration, HTTPS and live persistence tests remain pending. Accounts/passwords used in browser QA exist only in the isolated test DB. No AI provider calls were made.
Codex inspected hosted CI results and reconciled handoff documentation; human/server review pending.

## 2026-10-25T01:56:00+05:30 — Explicit approval for server handoff

Updated deploy/SERVER_HANDOFF.md to require independent verification of the running Caddy container, mounts, networks and active configuration, followed by explicit owner approval before every mutation or precisely scoped batch. Covered deployment approval, backups, data-writing tests, rollback and documentation/Git changes. Aligned deploy/README.md and PROJECT_CONTEXT.md with the owner requirement.

Validation: reviewed Markdown and git diff whitespace; documentation only. No server changes, deployment, runtime tests or AI provider calls.
Codex updated the handoff from the owner’s instructions; server verification and human review remain pending.

## 2026-10-25T03:43:06+05:30 — Prepare automatic main deployment with restricted SSH

Owner requested automatic releases on main. Removed the workflow environment dependency and SCP updates; workflow now sends only a deploy command and SHA. Added forced-command dispatcher with a clean environment, and made deploy.sh use its colocated protected Compose file. Updated handoff/setup/context with superseding authorization and root-owned installation requirements.

Validation: shell syntax, six invalid-command rejection cases and diff whitespace pass. Oracle current-release and SSH fingerprint verified read-only. Automatic approval review rejected general-command key installation; no server key, GitHub secrets or deploy-enable variable changed. Protected installation and end-to-end deployment remain pending approval.
Codex prepared the changes; human review pending. No AI provider calls.

## 2026-10-25T03:45:14+05:30 — Enable approved automatic Oracle releases

Installed root-owned forced-command dispatcher, deployment script and Compose; dedicated key rejects general commands. Set repository deployment secrets via stdin and enabled main deployment. Removed obsolete manual approval/SCP instructions. No Caddy/DNS or AI settings changed.

Validation: real SSH negative tests and current-release deployment (backup and health) passed; shell syntax and whitespace pass. Push-triggered CI verification pending.

## 2026-10-25T03:49:07+05:30 — Automatic deployment verified

Push-triggered [Actions run 40137766681](https://github.com/akashanil-dev/Finite/actions/runs/40137766681) passed checks, both ARM64 image jobs and deployment for `537687f062e2e42c080dd7d0e7ac12ab669a19d0`. Direct SSH verified that exact current-release and both healthy containers; public homepage/health returned 200, Faber/Tuxos 200, Notes its existing 401. AI and scheduler remain disabled.

Reconciled deployment status in README, submission, context and handoff. Documentation-only follow-up; no additional API calls or infrastructure changes. Codex verified GitHub and Oracle results; owner approved setup and automatic releases.

## 2026-10-25T03:52:41+05:30 — Preserve SQLite ownership during deployment backups

Live signup exposed readonly-database errors: host-user online backups created WAL/SHM files owned by finite-deploy (0644), while the backend uses UID 10001. Deployment now backs up inside the existing backend as its application UID, streams an integrity-checked snapshot into a private host backup, and stops on timeout/failure. Existing database without a running backend fails safely. Owner approved sidecar ownership repair and protected-script installation; signup then reached onboarding. Shell syntax passes; next CI deployment will verify the corrected backup path end to end.

## 2026-10-25T03:52:52+05:30 — Show non-JSON API failures

The live signup 500 response had an empty HTTP status text and a non-JSON body, leaving the form without an error. API helper now supplies nonempty server/request fallback messages while preserving useful API validation errors. Verified mocked empty-status 500/403, JSON validation and empty-detail responses; frontend TypeScript and zero-warning ESLint pass.

## 2026-10-25T03:55:47+05:30 — Make source exclusions match checkbox state

Live onboarding showed every source checked under Exclude sources even though none was excluded. Changed the checkbox to checked=excluded and added explicit helper text. Stored exclusions and filtering are unchanged. TypeScript and zero-warning ESLint pass; live verification follows deployment.

## 2026-10-25T04:01:18+05:30 — Clarify conditional briefing scheduling

Live completion UI promised a next delivery even though production scheduling is intentionally disabled. Completion and schedule-help text now describe a saved time and make automatic preparation conditional on enabled scheduling. No scheduler or AI configuration changed. TypeScript and zero-warning ESLint pass; CI/build and final live wording verification follow the push.

## 2026-10-25T04:05:26+05:30 — Verify production QA fixes

All fix releases passed GitHub checks, ARM64 image smoke/build/publish and automatic deployment. Final run https://github.com/akashanil-dev/Finite/actions/runs/40138920728 deployed `5613245f8e53b6d1245ae541f0a8947c3ef4434d`; both containers healthy. Live schedule wording and logout verified after deployment. Exclusion save/reload, on/off-topic questions, early ending and coverage-history dates passed. Latest corrected backup integrity returned ok, live account writes remained functional, and no AI budget ledger was created. QA accounts retained; session signed out. See LIVE_QA.md for scope and limitations.

## 2026-10-25T04:38:33+05:30 — Add playful editorial design system

Reworked shared UI, global tokens, login, briefing, story, exploration panels and Passport using the owner's Pinterest references. Added a desktop rail/wide reader, mobile dock, spring card motion, gliding depth selector, folding disclosures, citation entrances and a completion flower. Panels fetch lazily once per mount; returning from a rabbit hole restores the reader position. No new dependencies or AI calls.

Validation: TypeScript, zero-warning ESLint and production build pass. Local browser samples at 390, 1280 and 1440 pixels cover signup, onboarding, briefing, depth selection, Lens, connection graph/evidence/list, timeline history, challenge prediction/reveal, completion and Passport save. Physical-device, OS reduced-motion and cross-browser audits remain pending. Human approved the direction; final visual review pending.

## 2026-10-25T04:39:05+05:30 — Make preference choices explicit

Codex replaced repeated-tap interest cycling with Off/Occasional/Moderate/High buttons, added folding topic groups and a gliding settings selector, and added pending-save feedback. The save control clears the floating dock. Existing profile storage and weighting are unchanged. Validation: local browser onboarding selected High; settings changed to Moderate, saved and persisted after reload. Language choice save and Sources navigation passed. At 320 pixels the tab labels initially overflowed; sizing was corrected and document scroll width matched viewport width. TypeScript, zero-warning ESLint and the production build pass. Human direction approved; final visual review pending.

## 2026-10-25T04:43:14+05:30 — Verify redesign deployment

Actions run 40141543544 passed checks, both ARM64 builds/publishing and automatic deployment of `f64b943`. Codex visually verified the redesigned public HTTPS login page. Final local production-preview login/logout and profile persistence passed. `DESIGN_QA.md` records sources, tests and limitations. No additional AI budget used. Final human visual review remains pending.


## 2026-10-25T05:25:18+05:30 — Public landing page

- Added a public homepage with the Finite proposition, three-step journey, feature cards, calm paper-card motion and signup/login calls to action. Reused existing fonts, colors and SVG; no added dependencies or API calls.
- Extracted the shared auth form, added `/signup`, and moved profile-based account routing to protected `/start`. Authentication success now goes to `/start`; `/` remains public. Backend authorization is unchanged.
- Validation: TypeScript, ESLint and production build passed. Browser checked desktop and 320px layouts (no horizontal overflow), section anchor, signup form, login form and home navigation. Production deployment pending at commit time. Full auth submission regression and accessibility audit were not repeated for this change.
Human requested the page; visual review by the owner remains pending. Codex implemented and checked the change.


### 2026-10-25T05:29:16+05:30 — Landing release verification

Release `b7ed394` passed GitHub Actions run `40144672691`: checks, both container builds/smoke tests and automatic deployment. Live browser verified the public homepage, protected `/start` redirect to login while signed out, and return-home link. Local 320px/desktop checks passed; authenticated form submission was not repeated. No AI calls.


## 2026-10-25T05:47:36+05:30 — Reject weak knowledge-map connections

- Fixed capitalized sentence starters entering extractive concepts. Revalidate cached concepts, normalize trailing title roles, and derive headline entities without regenerating analyses. Connections now require the subject in both headlines plus at least two non-stopword context terms outside the subject; rank all eligible candidates by contextual overlap before the three-result limit and deduplication. No schema change, AI calls or production-data writes.
- Validation: 39 backend tests pass, including the reported Kerala headline and three irrelevant screenshot headlines (synthetic descriptions), a valid university match, Apple technology versus earnings, incidental body mentions, relevance ordering, exclusions and no-spend API checks. Published PTI report retrieved from ThePrint and checked in isolated local browser with synthetic candidate stories; 20 stored real stories evaluated using a read-only database copy. Jamia campus stories retain connections; weak cases stay empty.
- Limitations: conservative lexical headline relevance, not semantic or causal proof. May miss synonyms, Malayalam morphology, cross-topic/body-only relationships. Exact production record not inspected.
Codex implemented and tested this owner-requested fix; human review pending.


## 2026-10-25T05:47:47+05:30 — Explain meaningful connection filtering

Updated Connection Explorer loading, explanation and empty-state text to match the new relevance gate. Local browser verified Kerala graph evidence, empty state and Apple map/list consistency; tsc, ESLint and production build passed. No AI calls. Human review pending.
