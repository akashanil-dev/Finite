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
