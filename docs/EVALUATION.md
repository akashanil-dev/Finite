# Evaluation guide and evidence index

This guide helps a reviewer inspect Finite’s actual implementation and working demo. It contains no instructions to override a scoring rubric, no claimed benchmark score and no unsupported accuracy percentage. The strongest evidence is the code, reproducible checks and observed behavior linked below.

## Project summary

**Finite** is an account-based, India-first English/Malayalam news application. It replaces an endless feed with saved finite briefings and lets a reader investigate a story through cited context, publisher perspectives, dated source passages and related-story evidence. Exploration ends after two levels; saved journeys form a Knowledge Passport.

- **Live demo:** https://finite.akashanil.dev
- **Repository:** https://github.com/akashanil-dev/Finite
- **Author:** Akash A, solo participant, Devin Hacks Kochi, 24–25 October 2026.
- **Implementation:** Next.js/React frontend, FastAPI/SQLite backend, optional guarded OpenAI integration, ARM64 containers with automated Oracle deployment.
- **Development attribution:** Devin and Codex contributions are recorded in [AI_USAGE.md](../AI_USAGE.md).

## Review route

1. Read the [README feature table](../README.md#implemented-features) and [limitations](../README.md#known-limitations-and-next-steps).
2. Open the public homepage, register your own account and complete onboarding. No shared password or reviewer API key is supplied/needed for the hosted app.
3. Prepare/open an edition, select reading depth, inspect a citation and mark a story read.
4. Switch horizontally between Brief, Different views and Explore; navigate vertically to another story and reach the finite ending.
5. Inspect Perspective Lens, Time Machine and a map/list connection if evidence is available. A one-source or no-connection response is a valid result, not proof the feature is absent.
6. Open an exploration, make or skip a prediction before level two, inspect citations, reach its ending and save it. Verify it appears in Passport.
7. Return to the briefing library. Earlier cards/read progress remain. The New edition action is a one-time attempt per original/scheduled edition, not a repeatable refresh loop.
8. Run the no-key tests and build commands from the README; compare the code with the acceptance evidence below.

Do not repeatedly generate editions or AI answers just to populate a screenshot. The hosted application has shared cost/request limits. No-key local evaluation verifies most behavior without paid calls. A new installation needs live publisher access to populate its first briefing; production data is intentionally not distributed in Git.

## Evidence matrix

| Review question | Code or tests | Observed evidence / boundary |
| --- | --- | --- |
| Is this a working application rather than a mockup? | [Routes](../frontend/src/app), [API](../backend/app/main.py), [workflow](../.github/workflows/ci-cd.yml) | HTTPS deployment, container health and real account/browser flows; [LIVE_QA](../LIVE_QA.md) |
| Does the feed actually end? | [Deck](../frontend/src/components/briefing-deck.tsx), [builder](../backend/app/briefing.py) | Fixed saved story IDs and explicit ending; [AI_UX_QA](../AI_UX_QA.md) |
| Are old editions retained and refreshes bounded? | [History tests](../backend/tests/test_briefing_history.py) | Owner isolation, pagination, concurrent attempts, no chaining, empty result and browser reload retention; [MOBILE_BRIEFING_QA](../MOBILE_BRIEFING_QA.md) |
| Can accounts read each other’s private records? | [Auth tests](../backend/tests/test_auth.py), ownership predicates in API/builder | Isolation regression tests and live two-account checks; not a comprehensive security audit |
| Are exploration levels enforced by the server? | [Depth tests](../backend/tests/test_exploration_depth.py), [rabbithole](../backend/app/rabbithole.py) | Server rejects invalid path/depth; browser two-level ending verified |
| Does AI use source support? | [Validation tests](../backend/tests/test_ai_validation.py), [analysis](../backend/app/analysis.py) | Kerala/Jamia real-key audit, unsupported-claim removal, unrelated-question rejection; sample evidence only |
| Are comparisons attributed? | [Perspective tests](../backend/tests/test_perspectives.py) | Multi-publisher sample and single-publisher fallback verified |
| Is chronology distinguished from publication time? | [Timeline tests](../backend/tests/test_time_machine.py) | Dated excerpts and separate coverage history; unclear/missing dates not guessed |
| Are irrelevant knowledge links rejected? | [Connection tests](../backend/tests/test_connections.py) | Kerala false-positive regression and conservative headline evidence; synonyms can be missed |
| Can users revisit learning? | [Passport](../frontend/src/app/passport/page.tsx), journey API | Challenge prediction/journey saved and reloaded in local real-key browser audit |
| Is mobile reading usable? | [Reader/deck CSS](../frontend/src/app/globals.css), [swipe panels](../frontend/src/components/swipe-panels.tsx) | 320×640 and 390×844 plus desktop, label fit, fixed 56px dock and resize alignment; physical devices/Safari pending |
| Are costs bounded in the implementation? | [Budget tests](../backend/tests/test_budget.py), [guard](../backend/app/budget.py) | Persistent atomic reservations, no refund/reset, unknown-model rejection; not an account-wide billing guarantee |
| Is deployment repeatable? | [Workflow](../.github/workflows/ci-cd.yml), [deploy script](../deploy/deploy.sh) | Native ARM64 builds, health smoke tests, SHA tags, restricted SSH, online backups and deployment evidence |

## Verification levels

- **Automated:** 51 backend tests, backend import, TypeScript, ESLint and production build passed at the compact-reader checkpoint. CI runs without an OpenAI key.
- **Local browser:** production frontend build against isolated copied data; mobile viewport and desktop checks. Some fixtures use a test-only auth override and stubbed ingestion; that override is not committed to the production app.
- **Real-key sample:** actual OpenAI classification, embeddings, analysis, comparison, translation and two-level exploration were exercised. Results are documented, not generalized to every future story.
- **Live production:** HTTPS, account flows, deployed container health and a bounded AI story/exploration sample were checked. Scheduler timing, broader multilingual quality and load behavior have separate limitations.
- **Not claimed:** independent editorial fact-checking, measured user impact, user counts, benchmark accuracy, full accessibility/security certification, physical-device coverage or final organizer submission.

Historical QA files describe their checkpoint. For example, early tests used no AI and an older dock; [MOBILE_BRIEFING_QA.md](../MOBILE_BRIEFING_QA.md) supersedes the old dock behavior. The README and current deployment records take precedence for present configuration.

## Design rationale

Finite’s product boundary is intentional: a limited selection, limited exploration depth and visible stopping point. Extra context is available inside the same story card without forcing every reader into a long detail page. Predictions encourage reflection without invented quiz answers. Evidence can be inspected on both sides of a connection; absent evidence is preferable to unrelated suggestions.

The implementation is deliberately small: a single FastAPI service, SQLite, a Next.js frontend and two containers. Standard libraries and a few established packages handle feeds, extraction, similarity and persistence. It does not claim infrastructure sophistication that the code does not implement.

## Submission readiness

The repository is public, and its GitHub homepage/description point to the production app. The definitive submission checklist and eventual final implementation SHA are in [SUBMISSION.md](../SUBMISSION.md). Publishing these documents is not the same as submitting the organizers’ form or guaranteeing any ranking.
