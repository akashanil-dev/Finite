# Agent guide for this project

> **Start here:** [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) is the canonical shared project context (what Finite is, its architecture, feature status, decisions, bugs, roadmap and current state). This file defines *how* agents work; it does not duplicate the project specification.

## Event requirements

- Read [RULES.md](RULES.md) before working. Build the project from scratch during Devin Hacks Kochi (24–25 October 2026); do not import a pre-built project.
- Libraries, APIs and public datasets are allowed. Document their sources and use.
- Record the actual contribution of Devin and any other AI tools in [AI_USAGE.md](AI_USAGE.md).
- Keep the code repository, short project description and working demo up to date in [SUBMISSION.md](SUBMISSION.md).

## Use basic coding patterns

- Prefer straightforward, idiomatic code: small functions, clear names, simple data structures, and modules with one clear responsibility.
- Use the project's existing patterns. Add an abstraction only when an actual repeated need makes the code easier to understand.
- Choose the simplest implementation that meets the current requirement. Avoid unnecessary layers, generic frameworks, premature optimization and speculative features.
- Keep dependencies few and purposeful. Reuse appropriate standard libraries and established libraries instead of reimplementing them.
- Validate inputs, handle errors explicitly, and show useful failure messages. Do not hide failures behind fabricated success or demo data.
- Keep changes focused. Explain the reason for non-obvious decisions in short comments or project documentation.

## Document every meaningful change

- Update [CHANGELOG.md](CHANGELOG.md) in the same commit as each meaningful change. Record the date and time with timezone, what changed, why, the affected files or feature, the validation performed, and known limitations.
- Update [README.md](README.md) whenever setup, commands, environment requirements, project behaviour or demo instructions change.
- Update [AI_USAGE.md](AI_USAGE.md) whenever Devin or another AI tool makes a meaningful contribution. Record the task, the assistance, human review status, checks and any corrections. Brief summaries are enough.
- Keep claims accurate. Distinguish implemented and verified behaviour from planned or incomplete work. Never invent test results, deployment success, AI usage or commit timestamps.

## Make regular, timely commits

1. Inspect `git status` before editing and identify the files that belong to the current task.
2. Finish a small, coherent change, run appropriate checks, and update its documentation.
3. Review the diff and explicitly stage only the files for that change.
4. Commit after each completed milestone. While actively building, aim for a commit about every 30 minutes when meaningful changes are ready.
5. Commit completed work before a break or the end of a work session. If work is incomplete, document its state and use an honest `wip:` message.
6. Use short, descriptive messages, such as `feat: add perspective lens` or `fix: handle empty briefing`.
7. Do not create empty commits to satisfy the clock, and do not backdate commits.
8. Push committed checkpoints to the project repository regularly when the owner has approved it.

## Check work and protect credentials

- Use the project's actual commands (below) and report what ran and what passed, failed or could not be checked.
- Keep credentials, API keys and private data out of commits and logs. Use `backend/.env` (gitignored) and keep `backend/.env.example` sanitized.

## Project commands (Finite)

- Backend: `cd backend && uv sync && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`
- Frontend: `cd frontend && npm install && npm run dev -- -H 0.0.0.0 -p 3000`
- Frontend checks: `cd frontend && npx tsc --noEmit && npx eslint src && npx next build`
- Backend import check: `cd backend && uv run python -c "import app.main"`
- Next.js here is v16 with Cache Components enabled. Read `frontend/node_modules/next/dist/docs/` before changing frontend routing or data fetching. Client hooks that read URL data (`useParams`, `useSearchParams`, `usePathname`) must sit inside `<Suspense>` on dynamic routes.
- Local state lives in `backend/data/` (SQLite and the LLM cache, gitignored). `OPENAI_API_KEY` in `backend/.env` enables AI mode; without it the app runs in extractive mode.

## Persistent Project Context and Documentation Maintenance

`PROJECT_CONTEXT.md` is the project's continuously maintained memory, shared across all agents. These rules are **mandatory** for every agent and environment (Devin, Claude Code, Codex, Cursor and others).

1. **Read the project context before development.** At the start of a session, read `PROJECT_CONTEXT.md`, this file and [RULES.md](RULES.md) before making substantial changes. Also inspect the actual repository state (`git status`, recent commits, relevant source files); never rely on documentation alone.
2. **Keep `PROJECT_CONTEXT.md` up to date.** Update it whenever development meaningfully changes the project. This includes:
   - Adding, completing, changing, removing or deprecating a feature.
   - Changing the architecture, dependencies, API contracts, database schema, integrations, or auth and security behaviour.
   - Resolving a significant bug or discovering an important limitation.
   - Changing a major UI/UX decision, the product requirements or the roadmap.
   - Making a consequential technical decision.

   Documentation updates are part of finishing a feature, not an optional follow-up.
3. **Update the documentation in the same task.** For a significant change:
   1. Implement it.
   2. Test or otherwise verify it.
   3. Update the feature inventory (section C).
   4. Update the architecture (D), if affected.
   5. Update the roadmap (K).
   6. Record decisions (H).
   7. Record remaining limitations (J).
   8. Report the actual verification status.

   Do this before declaring the task complete. Never mark a feature COMPLETE unless its acceptance criteria have been verified.
4. **Preserve existing knowledge.** Make targeted edits; do not rewrite the whole document for a small change. Keep valid decisions, rationale and outstanding requirements. Remove information only when it has been superseded, and note consequential reversals in section H. Avoid contradictory or duplicated content.
5. **Keep it accurate.** Do not:
   - Invent features or architectural details.
   - Claim tests passed when they weren't run.
   - Treat speculative ideas as approved requirements.
   - Hide problems or silently drop requirements.
   - Expose secrets.
   - Present stale information as current.

   Label uncertain information explicitly.
6. **Keep it agent-agnostic.** `PROJECT_CONTEXT.md` must not depend on any agent's private memory, conversation history, proprietary session IDs, hidden reasoning or temporary state. Instructions specific to one tool belong in that tool's instruction file; shared project knowledge belongs in `PROJECT_CONTEXT.md`.
7. **Avoid unnecessary churn.** Formatting, trivial refactors and typo fixes don't need context updates unless they change documented behaviour. Update when understanding, functionality, architecture, requirements or status actually change.
8. **Keep the instruction files consistent.** This file and `RULES.md` point to `PROJECT_CONTEXT.md` as the canonical context and contain behavioural rules, not a copy of the specification. If they conflict, follow the organizers' and owner's instructions first, then fix the inconsistency.
9. **Reconcile the context at the end of each task.** Before declaring a substantial task complete, check:
   - Is the feature inventory accurate?
   - Are architectural changes documented?
   - Are known bugs and limitations current?
   - Are completed tasks marked correctly?
   - Are remaining tasks clearly identified?
   - Are important decisions preserved?
   - Does section M still describe how to resume?

   Then refresh section I (current state) and add a row to the **Context Maintenance Log** with the date and commit.

## Before submission

- Complete [SUBMISSION.md](SUBMISSION.md).
- Confirm the README gives reproducible setup and demo steps, and that the demo matches the submitted code.
- Update the changelog and AI usage record, commit, and push before the **code freeze at 8:00 AM IST on 25 October 2026**.
- Record the final submitted commit SHA in SUBMISSION.md.
