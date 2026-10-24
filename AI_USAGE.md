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
