# AI and swipe-reader audit — 25 October 2026

## Scope and evidence

Real OpenAI calls ran against an isolated copy of local story data in `/tmp/finite-ai-audit`, with the **original development reservation ledger** preserved. No production data, credentials or AI configuration were changed. UI QA used a test-only local auth override; this is not a new production authentication test. The normal authentication/isolation regression tests passed.

Cases exercised:

- Kerala University VC report (PTI via ThePrint, 24 October): relevant summaries, source-backed facts, five story-specific questions and four missing-piece questions passed the final analysis-v3 check. The same published report was used because the friend's original stored story was unavailable locally.
- Kerala rabbit hole: history of student politics, then wider mobilisation. Cited nodes rendered; incomplete historical coverage explicitly reported. Level two ends without more questions.
- Curiosity Challenge: selected a history prediction, revealed the final level, saved the expedition, and confirmed the prediction persisted in Passport.
- Custom unrelated cake question: AI rejected it as off-topic.
- Jamia hunger-strike report: analysis/exploration rendered; excerpt fallback marked when one summary failed verification.
- Multi-publisher Jamia story: real AI Perspective Lens compared Scroll.in and Indian Express, with two verified comparison claims. Single-publisher case correctly declined to invent a comparison.
- Malayalam: real translation returned Malayalam script for a short summary. Full Malayalam UI and linguistic quality review are not covered by this audit.
- Classification and embeddings: real API requests returned a Kerala/education classification and a nonempty embedding.
- Time Machine: source-dated passages displayed with unclear dates separated. Knowledge map connected related Jamia coverage with inspectable headline evidence. Neither requires AI.

## Fixes

Old extractive and translation caches could survive AI activation. New version/mode checks upgrade them. Analysis now checks summary assertions, facts and question premises independently; rejected summaries become literal source excerpts. Extractive rabbit holes no longer create misleading next questions from capitalized words. Node verification sees longer evidence passages; unsupported nodes are dropped and evidence gaps remain visible. Reported source claims are not labeled established truth.

## Browser checks

Production frontend build at localhost:3001; isolated backend at localhost:8000. At 390×844 and 1280×900: native horizontal scrolling revealed feature panels; vertical scrolling at the card edge advanced stories; reverse scrolling returned and restored the selected panel; dock hid on forward gestures and returned on reverse gestures. Long content stayed scrollable. Previous/Next controls, explicit read saving, finite endpoint, embedded journey/back, graph evidence, Time Machine and Passport save worked. Local retry state also recovered after a deliberate backend restart.

Screenshots: `/tmp/finite-swipe-mobile.png` and `/tmp/finite-swipe-desktop.png` (local artifacts, not committed). Physical touch devices, Safari and a full accessibility audit remain pending. Native gesture physics come from the browser; long inner content scrolls before the next story, with Next available for immediate navigation.

## Automated checks and limits

43 backend regression tests passed. Frontend TypeScript, ESLint (zero warnings), and Next production build passed. Initial test invocation from the repository root failed import resolution; rerunning from backend passed. A cache regression fixture was made explicit about extractive mode. A dock edit syntax error was caught and corrected before the successful build.

Development allowance is $5 cumulative reservations, not a monthly reset or actual billed usage. Final analysis-v3 checkpoint: $2.266581 reserved, 56 requests; later browser requests may increase this. The 100-request ceiling also remains. Production's requested $15 is separate and awaits explicit activation approval. Model verification and these samples cannot guarantee correctness of every future answer; source provenance and incomplete coverage still matter.
