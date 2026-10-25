# Compact reader and saved editions QA

2026-10-25T06:46:00+05:30

- Backend: 51 tests pass, including account isolation, 23-edition pagination, retention, simultaneous refresh claims, first-creation restriction, no extra-edition chaining, empty attempts and schedule date uniqueness/midnight boundaries.
- Frontend: TypeScript, ESLint and production Next build pass.
- Browser: local production preview at 320×640, 390×844 and desktop. Quick/Standard/Deep fit and change summaries. Headline scrolls out of the reading area. Fixed dock remains 56px high while reading; document width matches viewport. With bilingual controls, reading track measures 552.5px at 390×844. Feature panels align after resizing; this check found and corrected a ResizeObserver alignment bug.
- Library: initial original retained, empty refresh consumed without an empty card; a second scheduled fixture generated a real 12-story extra from the copied corpus. All three cards remained after reload and server restart; originals retain read progress, and none of the consumed originals/extra has a refresh button.
- Boundary: test-only auth override and scheduled fixture in an isolated copied database; ingestion stubbed, existing source articles used, OpenAI key empty. Source extraction may perform ordinary publisher requests. No API credits spent. This is not a real scheduled-delivery test or physical-phone/Safari validation.
- Production: full Actions run 40149975675 passed for `f8a5379`; deployed account library empty-state was verified in the browser. Populated history/one-time creation checks above were local, not repeated with paid production generation. Scheduler was subsequently explicitly approved and activated; see deploy/SCHEDULER_APPROVAL.md.
