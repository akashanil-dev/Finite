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
