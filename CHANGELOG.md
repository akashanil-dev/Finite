# Change log

Meaningful project changes during Devin Hacks Kochi, newest first. Timestamps are IST (UTC+05:30).

## 2026-10-24T23:32:53+05:30 — Curiosity Challenges browser QA

- Changed: Focus the challenge heading when it opens; show saving/error/retry states for Passport saves while retaining the prediction; prevent repeat clicks while saving. Clarify the no-connections state and remove an inaccurate fact-checking claim from the no-key loading message.
- Why: Browser QA found focus lost when the selected connection button disappeared and an unhandled save failure with no user feedback.
- Validation: Production frontend against an isolated SQLite database and deterministic retrieved passages; OPENAI_API_KEY forced empty. Verified desktop and 390px mobile prediction selection, disabled reveal until selection, back/cancel, skip with no prediction, Level 2 endpoint, exploration error/retry retaining prediction, failed save/retry, saved prediction in Passport, insufficient sources and early ending. No horizontal overflow; no new unhandled console errors after fixes. Earlier injected save failure reproduced the corrected issue.
- Checks: Nine backend/API tests and import passed in implementation checkpoint; final frontend TypeScript, ESLint and production build pass. QA servers stopped and standard API configuration restored in the final build.
- Limitations: No live OpenAI calls or AI quality claims. Hypotheses are generic, ungraded and currently English. Live AI validation is the explicit stopping point until the owner supplies a key.

## 2026-10-24T23:28:09+05:30 — Curiosity Challenges implementation

- Changed: Optional three-choice prediction before Level 2, reveal/skip/back controls, reflection alongside the cited answer and optional prediction in saved Passport journeys. Added curiosity-challenge.tsx; updated rabbit-hole.tsx, passport page and API types.
- Why: Active reflection without trivia scores or fabricated correct answers. The challenge uses no additional AI calls and never adds a journey level.
- Backend: Versioned exploration cache includes depth, angle, search and custom-question flag; cached responses receive the current request path. This prevents a cached Level 1 response from breaking the Level 2 endpoint. Old cache rows remain harmlessly unused.
- Validation: Nine backend/API tests and backend import pass with OPENAI_API_KEY explicitly empty. TypeScript, ESLint and production build pass for the core flow; final Passport display and browser checks follow in the QA checkpoint.
- Limitations: Browser QA pending in this implementation checkpoint. Generic connection hypotheses are intentionally ungraded; live AI quality is a separate key-required stage and is not run.

## 2026-10-24T23:18:29+05:30 — Perspective Lens browser QA and fixes

- Changed: Preserve short opening sentences in perspectives.py; regression test added. Citation chips show full publisher names and expose expanded state/accessibility labels. Keep the Lens toggle on one line on mobile. README documents recovery from a cached Turbopack port-permission failure.
- Why: Browser QA exposed skipped short lead sentences, ambiguous “The” citation labels and a wrapping Hide control.
- Validation: Seven backend/API tests and backend import passed; TypeScript, ESLint and standard production build passed. Fresh generated .next cache plus a port-capable execution environment resolved the earlier build failure; subsequent incremental builds passed too. No dependency or framework config changes.
- Browser checks: Production frontend with isolated temporary SQLite copy and labelled QA fixtures. Verified loading, expand/collapse, single-publisher explanation, injected HTTP 503 and successful retry, AI claim rendering with controlled responses, citation popovers/links, existing multi-publisher Jamia coverage, desktop and 390px mobile layout, and no horizontal overflow. Final AI and real-news pages had no console warnings/errors.
- Limitations: AI responses were fixtures, not real-key calls; live generation quality remains unverified. User database was not used for QA writes. Temporary QA API/frontend used ports 8100/3101; final build restored the default API configuration.

## 2026-10-24T23:12:02+05:30 — Perspective Lens

- Changed: Added backend/app/perspectives.py, GET /api/stories/{story_id}/perspectives, and the on-demand story-page Perspective Lens component. Added backend/tests/test_perspectives.py; updated README, submission demo and project context.
- Why: Compare coverage without inventing disagreement or treating multiple sections of one publisher as independent perspectives.
- Behaviour: One article per publisher homepage hostname, no aggregators, at most eight publishers. Original headlines and excerpts in extractive mode. AI groups cited claims and a separate explicit verification pass gates every displayed claim; malformed, unsupported or unverified claims are omitted. Existing prompt/model disk cache reused; no schema or dependency changes.
- Validation: Six unittest cases passed, including HTTP 200/404 routes, deduplication, fallback and citation/verification rejection; backend import, TypeScript and ESLint passed. git diff --check passed. Production build attempted twice but blocked by Turbopack CSS worker port binding (Operation not permitted), including elevated retry.
- Limitations: No real-key AI validation or browser walkthrough. AI comparison is English; source excerpts remain original-language. Hostname deduplication does not detect syndicated reporting or shared ownership. Coverage limited to stored headlines/excerpts, without additional network retrieval.

## 2026-10-24T23:08:19+05:30 — Shared project context

- Changed: Added PROJECT_CONTEXT.md and maintenance rules in AGENTS.md and RULES.md; linked the context from README.md.
- Why: Preserve requirements, architecture, verification limits and handoff instructions across agents.
- Validation: Reviewed documentation against source files and Git state; git diff --check passed. No runtime checks in this documentation checkpoint.
- Limitations: Prior test results remain historical; original assistant chat replies were unavailable through chat retrieval.

## 2026-10-24T22:43:23+05:30 — Event documentation for Devin Hacks Kochi

- Changed: Added `RULES.md`, `AGENTS.md`, `CHANGELOG.md`, `AI_USAGE.md`, `SUBMISSION.md` and `.github/pull_request_template.md`, adapted from the community-hackathon template the organizers first shared. Updated for Devin Hacks Kochi: event name, 24–25 October 2026 dates, 5:00 PM start, 8:00 AM code freeze, 11:00 AM wrap-up, solo format, hosts, prizes and links. Replaced the Codex requirements with Devin. Merged the template's extra ignore rules into `.gitignore` and added an event section to `README.md`.
- Why: The template described an older event (DevDay Exchange, 10–11 October, Codex). The organizers said the template is optional, so it was first removed and then brought back with accurate details.
- Validation: Checked event details against https://www.devinhacks.in/ and https://luma.com/3v8n74l1. The code freeze time comes from the organizers' announcement at the venue. Checked that local Markdown links resolve.
- Limitations: The public pages list the venue as "Venue TBC", so RULES.md points to the organizers' announcement instead of naming it.

## 2026-10-24T22:32:43+05:30 — Finite MVP: backend pipeline and mobile-first frontend

- Changed: `backend/` (FastAPI + SQLite: taxonomy, source credibility index, RSS ingestion, classification, briefing builder, story analysis, rabbit holes, translation, passport, scheduler) and `frontend/` (Next.js 16 PWA: onboarding, briefing, story and rabbit hole, passport, sources, settings). Committed as eight commits, from `chore: scaffold FastAPI backend and Next.js frontend` to `feat(frontend): briefing feed, story view, rabbit holes, passport and sources`.
- Timeline (all during the event, 24 October 2026, IST):
  - Around 20:00: started working on the project during the event (ideation and planning, as reported by Akash).
  - 20:21: local working folder created (filesystem timestamp).
  - From about 21:03: backend and frontend code written from scratch.
  - 21:31: moved into this repository.
  - 22:32: the history was re-recorded as eight logical commits, after the organizers said the template is optional. All commit times are real; nothing is backdated.
- Why: Core product. A finite daily briefing where any story can be opened into a cited exploration, with a depth limit, of causes, history and connections.
- Validation: `npx tsc --noEmit` and `npx eslint src` passed, and `npx next build` succeeded. API smoke test without a key: feed ingestion of about 1,000 articles, profile save, a 12-story briefing, story analysis, rabbit-hole exploration (4 nodes, 4 timeline events, 2 follow-up questions), mark-read and journey save all returned the expected data. All frontend routes returned HTTP 200.
- Limitations: AI-mode paths (OpenAI summaries, synthesis, claim verification, embeddings, Malayalam translation) have not been run with a real key. Single local user. Classification and clustering are approximate without a key.

## 2026-10-25T00:08:44+05:30 — $1 AI budget guard

Added persistent, atomic conservative reservations before every uncached OpenAI chat/embedding call (`budget.py`, `llm.py`), a read-only `/api/ai-budget` endpoint, no automatic SDK retries, and request size/output/count limits. Failed requests keep reservations. Unknown models fail closed. Four focused tests cover concurrency, exhaustion, failures/cache and invalid requests; backend import passed. Live AI/browser checks follow in a separate checkpoint. This is an installation allowance, not an account-wide cap or actual billing meter.

## 2026-10-25T00:15:26+05:30 — Repair live AI JSON requests

Live calls returned HTTP 400 because JSON mode requires JSON in the input message, not only instructions. `llm.py` now adds that instruction to the input and rejects non-object JSON. `analysis.py` regenerates extractive cached analysis when AI mode becomes available, and handles empty source lists. The wrapper regression test checks JSON input and standard service tier. Live classification identified both stored Jamia articles as protests/education/elections; embeddings grouped them together. Browser verified generated summaries, tailored questions, Missing Piece and Perspective Lens. Fifteen backend tests and import pass. Remaining grounding/UI refinements are a separate checkpoint.

## 2026-10-25T00:17:27+05:30 — Fail-closed AI verification and live browser QA

Rabbit-hole nodes now require exactly one explicit positive verdict; failed/malformed/missing/duplicate verdicts drop the claim. Timeline events and their dates are verified too; invalid refs are removed and empty results are marked insufficient. Exploration cache moved to v3. Translation rejects malformed/empty entries. Corrected off-topic UI wording (retrieval can already have run). Files: `rabbithole.py`, `translate.py`, `rabbit-hole.tsx`, `tests/test_ai_validation.py`.

Validation: 16 backend tests and import pass; TypeScript, ESLint and QA production build pass. Real API classification and embeddings passed on two stored Jamia articles. Production browser tested AI summaries, Missing Piece, tailored questions, Perspective Lens, two levels of cited exploration, timeline, unsupported-claim removal, challenge prediction/reveal, ending, Passport persistence, Malayalam rendering, unrelated custom-question rejection and corrected wording. No console errors on the three tested pages. QA used a database copy with scheduling disabled; real API calls used the shared persistent allowance. 15 requests reserved $0.776700; $0.223300 remains. These are conservative reservations, not actual billed spend. Existing publisher material and live Wikipedia retrieval were used, not synthetic AI responses.

Limitations: sample coverage only; Malayalam editorial accuracy requires human review. Browser viewport override did not take effect in this run, so live-AI mobile layout is not newly verified (earlier extractive mobile QA remains valid). Scheduler/full-ingestion live operation and account-wide billing are outside this test.

## 2026-10-25T00:32:15+05:30 — Time Machine implementation

Added a lazy story-page Time Machine with source-extractive dated passages, earlier/current grouping, a separate unresolved-date section, and publication/update coverage history. New `backend/app/time_machine.py` and GET `/api/stories/{id}/timeline`; new `frontend/src/components/time-machine.tsx`, story-page integration and five focused tests. Complete quotations retain citations; missing years are not inferred; multiple dates remain unresolved; up to 12 event passages. No OpenAI calls or extra retrieval.

Validation: 21 backend tests and import pass. Frontend tsc/ESLint/production build pass. Browser QA follows separately. Limitations: English date patterns only, stored source passages rather than a complete historical archive, no independent fact verification or automatic translation.

## 2026-10-25T00:35:42+05:30 — Time Machine browser QA and date correction

Browser fixtures exposed a false year: “2000 residents”. Standalone years now require temporal context, while connected alternatives/ranges stay unresolved. Undated-year passages retain source order rather than arbitrary alphabetical order. Added count/currency regression assertions in `test_time_machine.py`.

Verified in the production browser: real stored Jamia passages, 2005/2006 source disagreement, missing-year sections, citation popover/link, event/coverage switching, publication/update timestamps, collapse/reopen, no-dates empty state, injected 503 and successful retry, and the corrected numeric-count fixture. Real/empty pages had no console warnings/errors; the fixture's injected 503 was expected. Desktop layout has no horizontal overflow. Mobile-specific QA was not performed in this checkpoint. Backend 21 tests/import and frontend tsc/ESLint/build pass. No AI calls; ledger remains $0.776700 reserved and $0.223300 available. QA database isolated; main API restarted with scheduler disabled.

## 2026-10-25T00:44:56+05:30 — Connection Explorer implementation

Added source-backed cross-story comparisons in `connections.py`, GET `/api/stories/{id}/connections`, and the lazy story-page `connection-explorer.tsx`. Up to three inline comparisons among the latest 200 stored stories; saved concepts require literal evidence on both sides. Excludes overlapping article clusters/URLs, blocked sources, dominant excluded topics and unselected languages. No new AI calls, network retrieval or schema changes. Each comparison ends with original-source citations; no recursive recommendation loop.

Validation: 25 backend tests and import pass; frontend TypeScript, ESLint and production build pass. Browser QA follows separately. Limitations: shared mentions do not establish causality; exact matching misses synonyms/translations; saved concept quality and stored coverage bound discovery.

## 2026-10-25T00:46:14+05:30 — Connection Explorer browser verification

Production desktop browser QA passed on an isolated database with the API key disabled: real stored AI-election story linked to two other stories via cited ChatGPT mentions; both source excerpts and original publisher citation links rendered correctly. Injected 503 displayed a useful error and retry recovered; empty fixture, collapse/reopen and finite ending passed. No horizontal overflow at 1280px; empty page console clean (the injected 503 on the real-story page was expected). No feature defects found in this sample. Mobile-specific QA not performed.

25 backend tests/import and TypeScript/ESLint/production build passed at implementation checkpoint. No AI calls; ledger unchanged at $0.776700 reserved, $0.223300 remaining, 15 requests. Shared mentions are not causal relationships; richer semantic links remain future work.

## 2026-10-25T01:14:28+05:30 — Interactive knowledge graph

Added a finite selectable knowledge map to Connection Explorer with a starting story, labelled shared-mention branches, keyboard-operable story nodes, selection state and cited evidence on both sides. List view retained; no recursive expansion, new dependencies, backend changes or AI calls. Files: `connection-explorer.tsx`, `story-view.tsx`. TypeScript, ESLint and production build passed. Browser QA pending. Literal-mention discovery limitations remain.

## 2026-10-25T01:16:43+05:30 — Knowledge graph browser QA and connector fix

Fixed a disconnected visual branch line discovered in browser inspection. Production desktop QA verified node selection by click and Enter, selection/evidence updates, citation popovers and original links, map/list switching, injected error/retry, empty state and finite ending. Corrected connector visually rechecked. No console warnings/errors after reload; no horizontal overflow at 1280px. Mobile-specific testing remains pending. 25 backend tests, TypeScript, ESLint and production build pass. QA used an isolated database with API key disabled; no provider calls.

## 2026-10-25T01:37:34+05:30 — Accounts, sessions and per-user data

Implemented username/password registration, sign-in, 30-day opaque cookie sessions, sign-out, salted scrypt password hashing and persistent login throttling. No reset/email verification or complex password rules. Added API authentication, exact credentialed CORS, browser-write origin/header protection, local-only admin grants and additive ownership migration. Profiles, briefing dedup/history/read state and Passport journeys are isolated per account; scheduler iterates onboarded accounts. Old local history remains unassigned until explicit local claim; no automatic first-user ownership. Frontend login/registration, account gate and Settings sign-out added.

Validation: auth/ownership, session expiry/revocation, cookie flags, CSRF, login throttling, legacy claim and per-user briefing tests pass; frontend types/lint/build pass. Production desktop browser verified protected-page redirect, registration, reload persistence, saved preferences, wrong-password rejection, sign-out, a second account with empty preferences, and successful case-insensitive sign-in restoring the first account's preferences. Tests used a copied DB and no AI key. Mobile/assistive-technology audit and production HTTPS verification remain pending; no API allowance used.

## 2026-10-25T01:39:40+05:30 — Oracle ARM64 container and CI/CD preparation

Prepared separate unprivileged backend/frontend images, Next standalone output, Compose with persistent data/budget volume and resource ceilings, existing-Caddy site/network integration, and GitHub Actions checks plus native ARM64 build/smoke/publish jobs. SSH deployment is gated by FINITE_DEPLOY_ENABLED and the production environment; health checks, SQLite backups and previous-image rollback are included. Target is finite.akashanil.dev on the same Oracle Ampere host as Tuxos. Tuxos deployment was inspected read-only; Finite code was not imported from it. Added server setup and Codex CLI handoff documentation.

Validation: 34 backend tests; import, route type generation, tsc, zero-warning ESLint, standalone production build; Compose configuration and shell syntax pass. Browser auth flow passed on an isolated no-key DB. Local Docker daemon access is unavailable (sudo needs a password), so image builds and container smoke tests must run in CI; no Oracle deployment or public HTTPS verification claimed. No AI calls; ledger unchanged at $0.997112 reserved / $0.002888 remaining, 32 requests.

## 2026-10-25T01:45:05+05:30 — Hosted ARM64 validation and local auth handoff

GitHub run https://github.com/akashanil-dev/Finite/actions/runs/40128562535 succeeded for code commit `9d246ab5172e9eab681eb213a276aba2b0b8e2f0`: code checks, both native ARM64 image builds, no-key container health smoke tests and GHCR pushes. Deploy job skipped; FINITE_DEPLOY_ENABLED is unset. Local standalone frontend and authenticated API restored on 3000/8000 with scheduler disabled. Pre-auth SQLite and budget backups saved under gitignored backend/data/backups; no existing history was automatically assigned to an account.

Deployment script simulation (mocked Docker, temporary filesystem) passed successful release, valid SQLite backup, pull-failure preservation and health-failure rollback checks. This is not Oracle deployment verification. Server setup, Caddy integration, HTTPS and live persistence tests remain pending. Accounts/passwords used in browser QA exist only in the isolated test DB. No AI provider calls were made.

## 2026-10-25T01:56:00+05:30 — Explicit approval for server handoff

Updated deploy/SERVER_HANDOFF.md to require independent verification of the running Caddy container, mounts, networks and active configuration, followed by explicit owner approval before every mutation or precisely scoped batch. Covered deployment approval, backups, data-writing tests, rollback and documentation/Git changes. Aligned deploy/README.md and PROJECT_CONTEXT.md with the owner requirement.

Validation: reviewed Markdown and git diff whitespace; documentation only. No server changes, deployment, runtime tests or AI provider calls.

## 2026-10-25T03:43:06+05:30 — Prepare automatic main deployment with restricted SSH

Owner requested automatic releases on main. Removed the workflow environment dependency and SCP updates; workflow now sends only a deploy command and SHA. Added forced-command dispatcher with a clean environment, and made deploy.sh use its colocated protected Compose file. Updated handoff/setup/context with superseding authorization and root-owned installation requirements.

Validation: shell syntax, six invalid-command rejection cases and diff whitespace pass. Oracle current-release and SSH fingerprint verified read-only. Automatic approval review rejected general-command key installation; no server key, GitHub secrets or deploy-enable variable changed. Protected installation and end-to-end deployment remain pending approval.

## 2026-10-25T03:45:14+05:30 — Enable approved automatic Oracle releases

Installed root-owned forced-command dispatcher, deployment script and Compose; dedicated key rejects general commands. Set repository deployment secrets via stdin and enabled main deployment. Removed obsolete manual approval/SCP instructions. No Caddy/DNS or AI settings changed.

Validation: real SSH negative tests and current-release deployment (backup and health) passed; shell syntax and whitespace pass. Push-triggered CI verification pending.

## 2026-10-25T03:49:07+05:30 — Automatic deployment verified

Push-triggered [Actions run 40137766681](https://github.com/akashanil-dev/Finite/actions/runs/40137766681) passed checks, both ARM64 image jobs and deployment for `537687f062e2e42c080dd7d0e7ac12ab669a19d0`. Direct SSH verified that exact current-release and both healthy containers; public homepage/health returned 200, Faber/Tuxos 200, Notes its existing 401. AI and scheduler remain disabled.

Reconciled deployment status in README, submission, context and handoff. Documentation-only follow-up; no additional API calls or infrastructure changes.

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


### 2026-10-25T05:29:16+05:30 — Landing release verification

Release `b7ed394` passed GitHub Actions run `40144672691`: checks, both container builds/smoke tests and automatic deployment. Live browser verified the public homepage, protected `/start` redirect to login while signed out, and return-home link. Local 320px/desktop checks passed; authenticated form submission was not repeated. No AI calls.


## 2026-10-25T05:47:36+05:30 — Reject weak knowledge-map connections

- Fixed capitalized sentence starters entering extractive concepts. Revalidate cached concepts, normalize trailing title roles, and derive headline entities without regenerating analyses. Connections now require the subject in both headlines plus at least two non-stopword context terms outside the subject; rank all eligible candidates by contextual overlap before the three-result limit and deduplication. No schema change, AI calls or production-data writes.
- Validation: 39 backend tests pass, including the reported Kerala headline and three irrelevant screenshot headlines (synthetic descriptions), a valid university match, Apple technology versus earnings, incidental body mentions, relevance ordering, exclusions and no-spend API checks. Published PTI report retrieved from ThePrint and checked in isolated local browser with synthetic candidate stories; 20 stored real stories evaluated using a read-only database copy. Jamia campus stories retain connections; weak cases stay empty.
- Limitations: conservative lexical headline relevance, not semantic or causal proof. May miss synonyms, Malayalam morphology, cross-topic/body-only relationships. Exact production record not inspected.


## 2026-10-25T05:47:47+05:30 — Explain meaningful connection filtering

Updated Connection Explorer loading, explanation and empty-state text to match the new relevance gate. Local browser verified Kerala graph evidence, empty state and Apple map/list consistency; tsc, ESLint and production build passed. No AI calls. Human review pending.


### 2026-10-25T05:51:38+05:30 — Connection fix deployment

Commits `050cf46` (backend/tests) and `584716f` (UI explanation) deployed successfully through Actions run `40146140933`; checks, images, no-AI smoke tests and public-site verification passed. Article-specific browser QA was local with published PTI report text and synthetic comparison candidates, not the friend’s production account. No additional AI budget used.

## 2026-10-25T06:14:39+05:30 — AI reliability

Verify story summaries, cited facts and question premises; replace rejected summaries with excerpts. Remove spurious fallback follow-ups, improve verification evidence window, refresh stale AI/translation caches and configure preserved dev/production allowances. Backend regression suite: 43 passed. Real API sample checks succeeded; comprehensive factual accuracy is not guaranteed. Affected backend analysis, rabbithole, translate, budget, tests and environment templates.

## 2026-10-25T06:17:33+05:30 — Swipe briefing

Add a finite vertical briefing deck and horizontal in-card feature panels, retain visited card/panel state, embed journeys, preserve explicit read/save confirmation, and hide/show the dock by gesture direction. Fixed mobile dock overlap, returning-to-Explore state, embedded scrolling and scroll-snap dock flicker. Frontend tsc, ESLint and production build pass. Browser QA covers 390px mobile and 1280px desktop, native wheel scrolling, challenges/Passport, connections and timelines; physical touch remains untested.

## 2026-10-25T06:24:38+05:30 — Deployment and approved production AI

Verified release b33eb6e through successful Actions 40148109626. Executed explicitly approved server-only AI activation at $15, scheduling disabled, separate ledger preserved, environment backed up and backend health verified. Browser login and actual production Kerala article AI analysis passed. No Caddy/DNS/other-service configuration changes.

## 2026-10-25T06:43:15+05:30 — Saved briefing editions

Preserve saved briefing history with owner-scoped pagination; add atomic one-use extra editions, prohibit chaining/unlimited POST refresh, avoid empty editions, and key scheduled editions by local delivery date including midnight preparation. Additive SQLite migration preserves existing data. Affected: backend/app/{db,briefing,main}.py and tests/test_briefing_history.py. Validation: all 51 backend tests passed; no AI calls. Production scheduler activation remains separate; initial-creation crash claim recovery is an operator limitation.

## 2026-10-25T06:46:00+05:30 — Mobile reading space and edition library

Replace the latest-only briefing page with saved-edition cards and a dedicated reader route. Move edition metadata into cards and headlines into scrollable content. Restore a compact fixed 56px mobile dock; give depth labels 72px minimum buttons; fix horizontal-panel alignment on resize. Validation: 320×640/390×844 and desktop browser checks, history persistence, successful/empty one-time refresh, depth selection and scrolling; TypeScript, ESLint, production build passed. Isolated copied data and test auth; ingestion stubbed and OpenAI disabled. Physical phones and production rollout pending.

## 2026-10-25T06:54:04+05:30 — Public documentation and scheduler checkpoint

Rebuilt README around current features, production links, mobile screenshots, reproducible setup, evidence, AI guard and honest limitations. Added docs/ARCHITECTURE.md and docs/EVALUATION.md; rewrote SUBMISSION.md, reconciled deployment/handoff/context and labeled historical QA. Updated GitHub description/homepage/topics and made repository public with explicit approval after a 360-blob credential-pattern/private-path check (no matches; not a full audit). Verified mobile release f8a5379 via successful Actions 40149975675. Executed separately approved scheduler activation with environment backup and backend-only restart; health and first ingestion pass, timed delivery unobserved. Local document/image link checks and git diff --check passed. Unauthenticated GitHub repository, production homepage, signup and health returned HTTP 200.

## 2026-10-25T07:53:00+05:30 — Local briefing-count correction (uncommitted)

Changed backend/app/briefing.py to use a soft diversity cap with ranked backfill, preserving all eligibility and prior-delivery filters. Added four deterministic selection regressions and original requested-count metadata to history. Clarified edition cards and unsaved Settings changes. Read-only production inspection matched the two reported editions: 6 and 10 stories, both requested 12 at creation; the account still had 12 saved. This does not prove why a 20-story UI selection was not saved. Validation: 55 backend tests passed with AI/scheduling disabled; frontend TypeScript, ESLint and production build passed for the count/library change. No new browser QA or production mutation; existing editions unchanged. No commits or pushes, per owner instruction.

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


### 2026-10-25 17:04 IST — feat: improve briefing editions and reading controls
- Backfill narrow-interest editions, generate content-based cover lines, number/open editions, stack library cards and persist read/unread controls.
- Validation: 71 backend tests and frontend TypeScript/ESLint passed for the assembled changes; browser checks recorded in the detailed task entries. No push.


### 2026-10-25 17:04 IST — fix: retrieve original content behind Hacker News links
- Retrieve bounded public content and GitLab README prose, reject feed metadata, preserve source attribution, repair caches with backup and show unavailable previews without unsupported reader tools.
- Validation: 71 backend tests and frontend TypeScript/ESLint passed for the assembled changes; browser checks recorded in the detailed task entries. No push.


### 2026-10-25 17:04 IST — feat: clarify passport exploration history
- Replace mastery wording and variable-size chips with counted idea tiles and explicitly explained topic-frequency bars; preserve concept-free journeys.
- Validation: 71 backend tests and frontend TypeScript/ESLint passed for the assembled changes; browser checks recorded in the detailed task entries. No push.


### 2026-10-25 17:04 IST — fix: scope instant validation to protected route behavior
- Keep protected page validation configuration in server wrappers; preserve client auth gating and the settings unsaved-change notice.
- Validation: 71 backend tests and frontend TypeScript/ESLint passed for the assembled changes; browser checks recorded in the detailed task entries. No push.


### 2026-10-25 17:04 IST — feat: improve source methodology readability
- Add readable editorial principles, full-methodology disclosure and source-settings link with responsive layout and protected-route wrapper.
- Validation: 71 backend tests and frontend TypeScript/ESLint passed for the assembled changes; browser checks recorded in the detailed task entries. No push.


### 2026-10-25 17:04 IST — fix: show remaining stories as an aligned card stack
- Use explicit stack styles with two/one/no layers, last-story navigation wording and desktop sidebar alignment. Mobile 390x844 and 320x640 verified: stack visible, 8px dock clearance, no horizontal overflow, final layers absent.
- Validation: 71 backend tests and frontend TypeScript/ESLint passed for the assembled changes; browser checks recorded in the detailed task entries. No push.


### 2026-10-25 17:05 IST — Mobile verification and authorized local checkpoints
- Owner authorized logical commits after mobile verification; no push authorized. Six implementation commits created: d7f9b64 briefing editions/reading controls, 94e7cf1 linked-source retrieval, 9836f93 Passport, 1a32785 protected-route validation, 6b86ef8 source methodology, f63f06f story stacks. Earlier “uncommitted” notes describe their historical task state and are superseded by this checkpoint.
- Mobile browser checks at 390×844 and 320×640 confirmed visible layers, 8px stack-to-dock clearance, no horizontal overflow, successful next navigation and no layers on the final story. No further mobile code fix needed. Not a physical-device or safe-area hardware test.
- Final assembled checks: 71 backend tests passed with AI/scheduler disabled, TypeScript and ESLint passed, diff whitespace checks passed. Production build was not rerun; production is unchanged. No push performed.
