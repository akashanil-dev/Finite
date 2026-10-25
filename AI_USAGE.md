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


### 2026-10-25T05:51:38+05:30 — Connection fix deployment

Commits `050cf46` (backend/tests) and `584716f` (UI explanation) deployed successfully through Actions run `40146140933`; checks, images, no-AI smoke tests and public-site verification passed. Article-specific browser QA was local with published PTI report text and synthetic comparison candidates, not the friend’s production account. No additional AI budget used.

## 2026-10-25T06:14:39+05:30 — AI reliability

Codex implemented and tested the AI reliability and configurable-budget fixes. Used live OpenAI calls against isolated QA data with the existing development budget ledger; no production key/configuration changed. Human review pending. Corrected overly strict whole-analysis rejection to preserve independently accepted questions and verified missing-piece premises. 43 backend regressions pass.

## 2026-10-25T06:17:33+05:30 — Swipe briefing

Codex implemented the requested swipe reader and calm interaction changes, then exercised a production frontend build against an isolated local backend. Browser-native vertical/horizontal scrolling, reverse dock gesture, saved journey/prediction and feature panels were verified. Found and fixed dock overlap, snap flicker and lost Explore selection. Human design review remains pending; no production AI activation performed.

## 2026-10-25T06:24:38+05:30 — Deployment and approved production AI

Codex performed the owner-approved production AI activation after CI passed. Key transferred privately over SSH, never printed or committed. Isolated live QA account used; signup API and browser login/article generation verified. Development reservation ledger remained $2.281297/$5. Production sample validation recorded in AI_UX_QA.md.

## 2026-10-25T06:43:15+05:30 — Saved briefing editions

Codex implemented and tested saved-edition APIs, retention, one-attempt refresh and scheduled-date uniqueness. Owner requested these behaviors; human code review pending. 51 backend tests passed with no OpenAI calls; browser flow verification is ongoing.

## 2026-10-25T06:46:00+05:30 — Mobile reading space and edition library

Codex implemented the saved briefing library, compact mobile reader, fixed dock and responsive depth controls. Browser testing found and fixed horizontal panel misalignment on resize. Local production build, TypeScript and ESLint pass. Browser checks used isolated data/test-only auth and no OpenAI calls. Owner review pending; physical-device checks remain open.

## 2026-10-25T06:54:04+05:30 — Public documentation and scheduler checkpoint

Codex expanded documentation from actual source/config/test evidence, created architecture/evaluation guides and updated submission/runtime records. Captured real local-browser screenshots, not generated artwork. Owner explicitly approved public repository visibility and scheduler activation. Basic history scan found no matching credentials/private artifacts; no comprehensive security guarantee. Mobile CI/deploy passed, scheduler first ingestion passed with $15 guard preserved. Local document/image link checks and whitespace check passed; public GitHub/demo/signup/health links returned 200. Human review of final narrative/submission remains pending; ranking and organizer submission are not claimed.

## 2026-10-25T07:53:00+05:30 — Local briefing-count correction (uncommitted)

Changed backend/app/briefing.py to use a soft diversity cap with ranked backfill, preserving all eligibility and prior-delivery filters. Added four deterministic selection regressions and original requested-count metadata to history. Clarified edition cards and unsaved Settings changes. Read-only production inspection matched the two reported editions: 6 and 10 stories, both requested 12 at creation; the account still had 12 saved. This does not prove why a 20-story UI selection was not saved. Validation: 55 backend tests passed with AI/scheduling disabled; frontend TypeScript, ESLint and production build passed for the count/library change. No new browser QA or production mutation; existing editions unchanged. No commits or pushes, per owner instruction.
Codex investigated and implemented this local fix; human review pending. No provider calls were made.

## 2026-10-25T08:11:07+05:30 — Stacked briefing cards (local only)

Codex added two decorative sage paper layers and a 420ms eased lift/fan animation on hover and keyboard focus. Touch keeps the static stack; reduced-motion disables movement. Changed briefing/page.tsx and globals.css. An isolated browser preview caught and corrected layer ordering that obscured text; corrected focus state visually checked. TypeScript and ESLint pass. Authenticated full-page/mobile motion QA and human design review remain pending. No AI calls, commits, pushes or deployment.

## 2026-10-25T08:16:30+05:30 — Actual-page stacked-card QA

Tested authenticated /briefing on localhost using a dedicated local QA account with two copied saved editions (existing accounts unchanged), at 1280x900, 390x844 and 320x640. Found stale generated Next CSS still covering text despite corrected source; preserved/moved generated cache and restarted frontend, then verified z-index 2 and readable real-page cards. No application-code change required. Checked 34px inter-card layout gaps, no horizontal overflow, narrow-screen wrapped footer with 44px button and dock clearance, keyboard-focus fan-out, pointer hover state, opening an edition and returning. Sampled 18 computed transform states over 374ms: progressive easing toward -3px lift without overshoot. This is not a frame-rate benchmark; physical touch and OS reduced-motion emulation remain untested. Screenshot evidence: /tmp/finite-stack-mobile.png and /tmp/finite-stack-desktop.png (temporary local files, not repository assets). AI and scheduler disabled for the restarted local backend. No commits, pushes or production changes.

## 2026-10-25T08:20:19+05:30 — Brief identity and opened state (local)

Codex replaced first-story library headlines with concise top-three dominant-topic labels derived from stored story classifications (no AI calls). Added per-account chronological insertion numbering, Unopened/Opened/Finished badges, softer opened-card surfaces, and Continue reading/Read again actions. Additive nullable opened_at migration and authenticated idempotent POST /api/briefings/{bid}/opened persist opening only after reader data loads; reading counts stay independent. Existing saved stories and accounts are preserved. Tests: 58 backend tests pass including cross-account denial, idempotence, numbering/pagination and topic mix; frontend tsc and ESLint pass. Actual authenticated local browser verified open/return/reload persistence, zero stories marked read, and 390px/1280px styling. Production build blocked by font networking in sandbox, then Turbopack subprocess port permission in retry; not claimed passed. Human design review pending. No commits, pushes or production changes.

## 2026-10-25T08:43:33+05:30 — Requested local account demo data

Verified localhost Settings signed in as stack_layout_qa_0813. With owner authorization, seeded only that account with 10 demo editions and 8 explicitly labeled sample expeditions using existing stored stories; prior records preserved. Mixed unopened, partial and finished states; demo editions disable extra refresh. Passport browser readback: 8 expeditions, 16 sample questions, 3 finished briefs; library: 12 total cards including two prior editions. Added Demo prefix for history items whose config.demo_data is true. Database online backup: /tmp/finite-before-demo-1792897977.sqlite3. Seed marker demo_passport_cards_v1:<account id> records inserted IDs and prevents duplicate seed runs. Demo questions are illustrative, not claims of genuine user exploration; dates/read counts are simulated. No AI, production writes, commits or pushes.

## 2026-10-25T08:46:06+05:30 — Requested akash_a demo account

Owner corrected the demo destination to local username akash_a. Confirmed it did not exist, created it with the owner-supplied credential (not recorded here), and seeded 10 labeled demo editions and 8 sample Passport expeditions. Login API verification passed; 10 editions, 8 expeditions, 16 questions and 3 completed examples. Existing QA account/data retained. Backup /tmp/finite-before-demo-1792898149.sqlite3; inserted edition IDs 18–27 and journey IDs 10–17. No AI, production changes, commits or pushes.

## 2026-10-25T09:22:49+05:30 — Local akash_a presentation adjustment

At owner request, removed visible Demo prefixes from the seeded akash_a edition and expedition titles/questions. Internal seed provenance remains in kv; historical reading/question activity is seeded, not verified personal activity. Updated only the ten seeded editions: newest three contain 10 actual stored stories each, remaining seven contain 15 each. Counts/read lists adjusted consistently; completed examples stay complete. All referenced story payloads verified present and unique within each edition. The 42-story corpus is reused across editions; no invented news or AI calls. Backup: /tmp/finite-akash-before-card-update-1792900355.sqlite3. No commits, pushes or production changes.

## 2026-10-25T09:25:29+05:30 — News-specific edition cover lines

Replaced generic category-list titles with content-keyed editorial cover lines (app/edition_title.py). At creation, AI-enabled builds request an 8–16-word line from actual headlines through the existing guarded LLM wrapper; output length and supporting-story IDs are validated, but these checks do not guarantee factual entailment. Library reads never generate. Unavailable/rejected generation falls back to two headline excerpts. Keys include ordered story IDs and headlines, so changed contents cannot reuse stale titles. Codex reviewed all ten akash_a edition headline sets and saved specific cover lines locally without provider calls. This one-time reviewed backfill is distinct from automated generation. Added cache/fallback/invalid-support tests; all 61 backend tests passed with AI disabled, and authenticated running API returned new titles. Existing numbering, counts and opened/read states preserved. No commits, pushes or deployment.

## 2026-10-25T09:29:05+05:30 — Reversible briefing reading status

Added whole-briefing Mark read/unread control inside the reader card header and reversible individual-story footer toggle. Authenticated POST /api/briefings/{bid}/read-state updates all stories; existing /read accepts read:false (default true preserved). Atomic owner-scoped updates recompute completed_at, clearing it when unread so Passport completed counts remain correct. UI uses confirmed server payload; failures show errors. Mobile QA caught a positional flex-layout conflict; moved controls into the existing header to preserve reader scrolling and footer clearance. 62 backend tests pass; actual local QA browser verified whole-brief read/unread persistence and individual toggle at desktop/390px. No AI, commits, pushes or production changes.

## 2026-10-25T09:31:48+05:30 — Shared card feature coverage

Verified card design and controls are shared application behavior, not seeded-account conditions. Added regression coverage creating normal initial, extra and scheduled editions for two independent accounts without demo metadata: cover caching, per-account numbering, owner-scoped opening and whole-edition read/unread completion all pass. Shared frontend maps every library item and routes every edition through the same reader controls. All 63 backend tests pass; title generation mocked, zero provider calls. Existing uncached editions use headline excerpts; new AI-enabled editions can generate editorial lines at creation. No additional runtime change needed, no commits or pushes.


### 2026-10-25 10:13 IST — Passport exploration wording and layout (local, uncommitted)
- Replaced mastery/unlock language with saved exploration history. Counts explicitly describe saved expeditions, question steps (including repeats), and briefings marked read.
- Replaced variable-size lime chips with consistent muted idea tiles and expedition counts; mobile uses one column. Topic bars now explain relative frequency and multi-topic counting, not proficiency.
- Saved journeys without concept labels remain visible. Backend data and API unchanged.
- Validation: TypeScript and ESLint passed; authenticated localhost Passport inspected at desktop 1280×900 and mobile 390×844, including topic bars; mobile document width matched content width. No production build rerun, API spending, commit or push.


### 2026-10-25 10:24 IST — Resolve Hacker News links before summarizing (local, uncommitted)
- Added bounded public-URL retrieval with per-redirect validation, pinned resolved destination, TLS hostname, content-type/size limits and GitLab README prose extraction. HN description/link/points metadata is never used as evidence. Original and discussion links remain distinct; citations name the destination with HN discovery attribution.
- Unreadable sources return an explicit unavailable preview with links; reader suppresses depth choices and unsupported exploration tools. Failed retrievals retry after an hour; existing unavailable summaries do not bypass retrieval. Analysis/exploration cache versions advanced without deleting saved exploration records.
- Added scripts/repair_linked_articles.py: SQLite online backup, refresh HN content and invalidate only affected story analysis/translations. Local repair covered 45 articles (32 readable, 13 unavailable) and seven story caches; accounts, briefings, progress and saved journeys/explorations preserved. Backup files remain in gitignored backend/data/.
- Validation: 70-test full backend suite passed, followed by eight targeted tests after adding mixed-empty-source coverage; TypeScript/ESLint passed. Browser verified reported TCL/GitLab story, Small Programs and Languages HTML extraction, and Steal My Bitcoin unavailable state including Different views/Explore on a mobile viewport. README markdown/table noise found in browser and removed. No AI credits used. No commit, push, production change or final production build.
- Limits: special README support currently covers two-segment gitlab.com project URLs with README.md; other repositories use generic HTML extraction or honest fallback. Self-post discussions are deliberately not treated as article evidence. Extraction is heuristic, not verification of authors' claims.


### 2026-10-25 10:27 IST — Remaining-story stack cue (local, uncommitted)
- Briefing reader shows two decorative sheets when at least two stories remain, one when one remains, and none on the final story. Fixed-height snap slots reserve 16px for layers; reading/footer controls stay above them. Final navigation says “Last story · swipe to finish”. Styles scoped to the component.
- Verified authenticated three-story edition at desktop: stack states 2/1/0, next-button scrolling at exact slot height, and final card without layers. Mobile 390×844 final card and dock remained separated with no horizontal overflow. TypeScript/ESLint and diff checks passed. No commits, pushes or API calls introduced.


### 2026-10-25 10:52 IST — Briefing instant-navigation validation (local)
- Split /briefing into a server page wrapper and unchanged client briefing-library component. Set instant=false only on the server page: AuthGate deliberately withholds this route until the client session check resolves, so its initial render cannot be validated as instant. Auth behavior and data access remain unchanged.
- Consulted installed Next.js 16 documentation; instant exports are invalid in client components. Other routes retain validation. This is a scoped validation opt-out, not a performance improvement.
- Validation: TypeScript, ESLint and diff checks passed. Authenticated browser loaded saved briefings with no insight badge and no captured error/warning logs. No production build rerun, commit or push.


### 2026-10-25 10:56 IST — Protected-route instant validation (local, uncommitted)
- Applied the briefing server-wrapper pattern to Settings, Passport, Sources, onboarding and start; existing story/edition server pages also declare instant=false. All sit behind the same client AuthGate and cannot promise a validation-time render. Public landing/login/signup remain unchanged. No auth checks removed and client view behavior preserved.
- Validation: TypeScript, ESLint and diff checks passed; authenticated Settings loaded with no insight badge or captured warning/error logs. Other routes inspected structurally but not individually browser-tested this turn. No commits or pushes.


### 2026-10-25 10:59 IST — Source methodology readability (local, uncommitted)
- Replaced dense dark methodology block with a light bordered card, clear headline, three concise principles, version badge and link to source settings. All five API-provided methodology rules remain available in a native keyboard-accessible disclosure. Desktop columns become mobile rows; namespaced stylesheet avoids dev CSS-module export issues.
- Validation: TypeScript/ESLint passed; desktop/mobile browser inspection, disclosure opens with all five rules, mobile width equals scroll width (no horizontal overflow). No API behavior changes, commits or pushes.


### 2026-10-25 16:59 IST — Make story-stack styles reliable (local)
- Replaced the reader stack CSS-module binding with an explicit namespaced stylesheet import, matching the working Sources styling approach. This avoids missing module class mappings in the current development pipeline. Layer logic remains two/one/none.
- TypeScript, ESLint and diff checks passed. Authenticated browser verified computed layer displays for all three positions, visual first-card stack and persistence after a full reload. No commit/push.


### 2026-10-25 17:01 IST — Align desktop reader with sidebar (local)
- Desktop immersive reader now uses the sidebar's 28px top/bottom inset. Deck including decorative sheets has height 100dvh minus 56px; mobile rules unchanged.
- Browser geometry confirmed sidebar and deck both top 28px/bottom 692px at 720px viewport height; front card reserves 16px for sheets. TypeScript/ESLint passed. No commit/push.


### 2026-10-25 17:05 IST — Mobile verification and authorized local checkpoints
- Owner authorized logical commits after mobile verification; no push authorized. Six implementation commits created: d7f9b64 briefing editions/reading controls, 94e7cf1 linked-source retrieval, 9836f93 Passport, 1a32785 protected-route validation, 6b86ef8 source methodology, f63f06f story stacks. Earlier “uncommitted” notes describe their historical task state and are superseded by this checkpoint.
- Mobile browser checks at 390×844 and 320×640 confirmed visible layers, 8px stack-to-dock clearance, no horizontal overflow, successful next navigation and no layers on the final story. No further mobile code fix needed. Not a physical-device or safe-area hardware test.
- Final assembled checks: 71 backend tests passed with AI/scheduler disabled, TypeScript and ESLint passed, diff whitespace checks passed. Production build was not rerun; production is unchanged. No push performed.
