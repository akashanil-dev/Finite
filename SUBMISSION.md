# Finite — Devin Hacks Kochi submission packet

**Event:** Devin Hacks Kochi, 24–25 October 2026. **Code freeze:** 25 October, 8:00 AM IST. Organizer-form submission is a separate human action; this document does not claim it has occurred.

## Project and access

| Field | Value |
| --- | --- |
| Project | **Finite — News that ends. Understanding that doesn't.** |
| Author | Akash A, [@akashanil-dev](https://github.com/akashanil-dev), solo participant |
| Public source repository | https://github.com/akashanil-dev/Finite |
| Working HTTPS demo | https://finite.akashanil.dev |
| Account creation | https://finite.akashanil.dev/signup |
| Returning user | https://finite.akashanil.dev/login |
| Reviewer guide | [docs/EVALUATION.md](docs/EVALUATION.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| CI/CD | [GitHub Actions](https://github.com/akashanil-dev/Finite/actions/workflows/ci-cd.yml) |
| Latest verified implementation checkpoint | `f8a537905b08e053bc3461be77c7a18b8b55bd72` — compact mobile reader and saved edition library |
| Checkpoint CI/deploy evidence | [Run 40149975675](https://github.com/akashanil-dev/Finite/actions/runs/40149975675): checks, both ARM64 images and production deployment succeeded |
| Final submitted implementation SHA | **Not yet designated.** Record the chosen freeze commit before submitting the organizer form; the checkpoint above is not a claim of final submission. |

The hosted demo needs only a browser and a self-created account. Reviewers do not need Python, Node or their own API key. Local reproducibility instructions are in [README.md](README.md#run-locally).

## One-line description

Finite turns English and Malayalam news into saved, personalised briefings and source-backed explorations of context, perspectives, history and connections—with a clear stopping point instead of endless scrolling.

## Short description

Finite helps readers understand the news without doomscrolling. Users choose interests, languages and reading depth, then read a bounded set of attributed stories. Within each story card they can compare publisher perspectives, inspect dated source passages, explore related-story evidence or follow a cited rabbit hole that ends after two levels. Optional Curiosity Challenges invite reflection without scores, while the Knowledge Passport saves useful journeys. Accounts keep preferences, editions and progress separate. Earlier briefings remain available; a single extra-edition attempt prevents unlimited on-demand refresh. The application runs on Oracle ARM64 containers with GitHub CI/CD, guarded optional AI and explicit extractive fallbacks.

## Problem, approach and distinguishing choices

- **Problem:** headline feeds encourage repeated consumption while leaving context fragmented and offering few stopping cues.
- **Approach:** freeze a finite edition, make context available inside the story, and end both reading and exploration deliberately.
- **Evidence-centered design:** citations, source methodology, claim-support checks, original excerpts and honest insufficient-evidence states.
- **Learning continuity:** saved journeys and concepts without streaks or artificial quiz scoring.
- **Regional access:** India-first source selection, English/Malayalam feeds and optional cached Malayalam translation.
- **Practical engineering:** account isolation, persistent cost reservations, saved edition history, responsive interactions and a working container deployment.

These are product and implementation claims. No measured retention improvement, learning outcome, user count or factual-accuracy benchmark is claimed.

## Suggested demonstration

1. Open the public homepage and create an account.
2. Set languages, interest priorities and exclusions; prepare/open a briefing card.
3. Show Quick/Standard/Deep, a source citation and saved read progress.
4. Navigate vertically between cards and horizontally through Brief / Different views / Explore. Show the compact fixed mobile dock.
5. Compare publishers where available; inspect a Time Machine excerpt and a knowledge-map branch with evidence from both stories.
6. Ask a relevant question, choose a level-two connection, predict or skip, then reach the ending and save the journey to Passport.
7. Return to the edition library. Show that old cards remain and New edition is a single attempt, not a repeatable refresh chain.

Do not force every story to have multiple publishers, a dated event or a meaningful connection. Empty/single-source states are valid evidence-sensitive behavior. The hosted AI allowance is shared, so avoid repeated expensive regeneration.

## Implementation and validation

- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS 4; responsive swipe reader, saved library and standalone-display manifest.
- **Backend:** Python 3.13+, FastAPI, SQLite WAL; feed ingestion, ranking/grouping, retrieval, analysis, account isolation and edition lifecycle.
- **AI:** optional OpenAI generation/embeddings with source support checks, cache/version handling and a persistent reservation ledger. Separate development $5 and approved production $15 guards; 100-request ceiling per installation.
- **Deployment:** GitHub checks/builds/smoke-tests native ARM64 images, publishes SHA tags and deploys to Oracle via restricted SSH. Server pulls containers without cloning/building the source.
- **Automated checkpoint:** 51 backend tests, backend import, TypeScript, ESLint, production build and container health jobs passed.
- **Browser evidence:** local 320px/390px and desktop checks; earlier live signup/login/isolation, feature flows and bounded production AI sample. See [evaluation matrix](docs/EVALUATION.md#evidence-matrix) for exact scopes.

### Evidence files

| Record | Coverage |
| --- | --- |
| [MOBILE_BRIEFING_QA.md](MOBILE_BRIEFING_QA.md) | Compact reading area, sticky dock, resizing, saved editions, one-use refresh and reload persistence |
| [AI_UX_QA.md](AI_UX_QA.md) | Real-key Kerala/Jamia examples, support checks, exploration/challenge/Passport, Malayalam sample and activation |
| [LIVE_QA.md](LIVE_QA.md) | Production account flows, isolation, feature checks and deployment backup repair |
| [DESIGN_QA.md](DESIGN_QA.md) | Visual references, landing page, responsive checks and connection regression |
| [CHANGELOG.md](CHANGELOG.md) | Timestamped implementation and validation chronology |
| [AI_USAGE.md](AI_USAGE.md) | Actual Devin/Codex contribution, checks and human review boundaries |

## Limitations to disclose

AI checks are not a guarantee of correctness. Human Malayalam review, wider editorial sampling, physical-device/Safari and full accessibility/load/security audits remain open. Publisher availability varies. Deterministic connections can miss synonyms and Time Machine is not a complete archive. Password reset, email verification, offline article reading and push notifications are not implemented. Scheduler activation and actual observed delivery are recorded separately in [the scheduler record](deploy/SCHEDULER_APPROVAL.md). Image rollback does not automatically restore database schema/data.

## Attribution and event compliance

Built solo from scratch during the event, using public libraries, publisher RSS, Wikipedia background and optional OpenAI APIs. [README attribution](README.md#data-dependencies-and-attribution) links the data/dependency sources. Devin assisted planning and initial implementation; Codex assisted subsequent features, fixes, design, tests, deployment and documentation. Human direction is Akash’s; detailed code/editorial review is not represented as universally complete.

## Final submission checklist

- [x] Project, author and event identified.
- [x] Public repository and working production links provided.
- [x] Feature inventory, architecture, setup and evidence guide supplied.
- [x] AI assistance and external dependencies/data attributed.
- [x] Current implementation checkpoint has successful CI/CD evidence.
- [x] Basic tracked-file/history credential-pattern review found no matching secrets or private database/key artifacts (not a comprehensive security audit).
- [ ] Choose and record the final implementation SHA at code freeze.
- [ ] Verify the final documentation push and production state.
- [ ] Submit the repository, description and demo through the organizers’ announced method.

Publication of this repository and packet does not imply completion of those unchecked organizer-submission steps.
