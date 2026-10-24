# Change log

Meaningful project changes during Devin Hacks Kochi, newest first. Timestamps are IST (UTC+05:30).

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
