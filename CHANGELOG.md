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
