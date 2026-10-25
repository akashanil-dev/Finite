# Finite

**News that ends. Understanding that doesn't.**

Finite is a finite, personalised daily news briefing (English and Malayalam). Most news apps answer *what happened* and then keep you scrolling. Finite also helps you see **why it happened, how we got here, and what it connects to**, through source-backed "rabbit holes" that go a fixed number of levels deep and always end. You finish your briefing, and you're done.

Built solo by Akash A ([@akashanil-dev](https://github.com/akashanil-dev)) with Devin at **[Devin Hacks Kochi](https://www.devinhacks.in/)**, 24–25 October 2026.

| Event document | Purpose |
| --- | --- |
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | Canonical architecture, requirements, current state and handoff |
| [RULES.md](RULES.md) | Devin Hacks Kochi event details and rules |
| [SUBMISSION.md](SUBMISSION.md) | Submission details and checklist |
| [CHANGELOG.md](CHANGELOG.md) | Timestamped development log |
| [AI_USAGE.md](AI_USAGE.md) | How Devin and other AI tools were used |
| [AGENTS.md](AGENTS.md) | Conventions and commands for coding agents |

## How it works

1. **Curiosity profile:** choose fields and subfields and give each a priority (occasional, moderate or high). You can also exclude subjects and sources. Choosing Malayalam adds Malayalam outlets to the sources Finite reads.
2. **Briefing schedule:** pick a delivery time, a lookback window (24, 30 or 48 hours; default 30) and the number of stories. Finite prepares the briefing 30 minutes before delivery, then freezes it.
3. **Finite feed:** a numbered list of source-backed stories with a progress bar and an explicit *"You're done for today"* ending.
4. **Story:** quick (30s), standard (2 min) or deep (5 min) summary, key facts with citations, original publish and update times, sources with credibility tier, and **The Missing Piece** (what the coverage didn't explain).
5. **Rabbit holes:** questions chosen to fit the type of story, plus *ask your own*. Level 1 gives context and Level 2 gives connections, then the expedition is complete. Every claim is cited and labelled *established*, *reported* or *disputed*, with a timeline where relevant.
6. **Curiosity Challenges:** before following a Level 2 connection, optionally predict a shared history, similar mechanism or wider impact. Reveal the cited exploration and reflect; there are no scores or invented correct answers. Skip or return to the connection choices anytime before revealing. Your prediction is saved with the journey. No extra AI calls are required.
7. **Knowledge Passport:** the concepts you've explored, with no streaks.
8. **Perspective Lens:** open “Compare” on a story to see headlines and short original excerpts from up to eight distinct publishers. With AI enabled, cited claims are grouped as corroborated, reported, disputed or opinion only after an explicit support check. Failed checks fall back to source excerpts. Aggregators are excluded; one publisher cannot count as multiple perspectives. Comparisons are English; excerpts retain their original language.
9. **Sources page:** a public credibility index of every outlet Finite reads, with its tier, confidence weight and the reason for it.

## Stack

- **Backend:** Python 3.13, FastAPI, SQLite, feedparser, trafilatura, scikit-learn, OpenAI SDK (optional)
- **Frontend:** Next.js 16, React 19, Tailwind CSS 4. Mobile-first and installable on phones as a web app.

| Path | Purpose |
| --- | --- |
| `backend/app/taxonomy.py` | Interest fields and subfields, with keywords for sorting stories into them |
| `backend/app/sources.py` | Source credibility index |
| `backend/app/ingest.py` | Reads RSS feeds, detects language, sorts articles into topics, fetches full text when needed |
| `backend/app/briefing.py` | Lookback window, skipping stories already sent, grouping duplicates, weighted ranking, freezing the briefing |
| `backend/app/analysis.py` | Summaries, key facts with citations, the Missing Piece, story-specific questions |
| `backend/app/rabbithole.py` | Cited rabbit holes with a depth limit and claim checking, generated once per story and shared |
| `backend/app/retrieval.py` | Source passages from the story's articles plus Wikipedia background |
| `backend/app/translate.py` | Malayalam translation (cached) |
| `backend/app/llm.py` | OpenAI wrapper with an on-disk cache |
| `backend/app/main.py` | API routes and the background scheduler |
| `frontend/src/app/*` | Onboarding, briefing, story and rabbit hole, passport, sources and settings screens |

## Run locally

Prerequisites: Python 3.13 with [uv](https://docs.astral.sh/uv/), Node.js 20+ with npm, and internet access.

```bash
# backend (port 8000)
cd backend
cp .env.example .env        # optional: set OPENAI_API_KEY
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# frontend (port 3000), in another terminal
cd frontend
npm install
npm run dev -- -H 0.0.0.0 -p 3000
```

Open http://localhost:3000. On a phone on the same network, open `http://<laptop-ip>:3000`. The app calls the API on port 8000 of the same host; set `NEXT_PUBLIC_API_URL` to use a different address.

**Without `OPENAI_API_KEY`** the app runs in *extractive mode*: summaries and rabbit holes quote source passages directly, and Malayalam translation is unavailable. The UI labels which mode produced the content.

### Checks

```bash
cd frontend && npx tsc --noEmit && npx eslint src && npx next build
cd backend && uv run python -c "import app.main"
uv run python -m unittest discover -s tests -v
```

### Build troubleshooting

If a restricted agent run fails with a Turbopack CSS-worker `binding to a port: Operation not permitted` error, run the build in an environment that permits local ports. If the same error persists after permissions are restored, move the generated `frontend/.next` directory aside and rebuild. A fresh cache resolved this failure during browser QA; no framework/configuration changes were needed. Do not move `.next` while serving the production build.

## Status

- **Working, tested without an AI key:** reading 29 English and Malayalam feeds, sorting stories into topics, grouping duplicates, weighted ranking, frozen briefings with read progress and completion, story summaries and questions, rabbit holes with a depth limit, ask-your-own, Knowledge Passport, the sources page, and the scheduler.
- **Verified on a live-key sample (25 Oct):** AI summaries and questions (`gpt-6-luna`), AI rabbit holes (`gpt-6.1-sol`) with claim-by-claim checking, embedding-based duplicate grouping, and Malayalam translation.
- **Known limitations:**
  - Single local user only.
  - Topic sorting without a key is approximate.
  - Duplicate grouping without a key sometimes splits one event into two stories.
  - Source weights are editorial judgements.
  - Perspective Lens and Curiosity Challenges pass a real-key desktop browser sample, including the endpoint and saved prediction. Earlier no-key mobile checks pass; live-AI mobile and broader editorial quality remain pending.

## Data and attribution

Publisher RSS feeds are listed in `backend/app/sources.py`. Finite shows short summaries with attribution and always links to the original article. Background passages come from the [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) (CC BY-SA), and each citation links to the article used. Fonts are Inter, Newsreader and Noto Sans Malayalam (Google Fonts).

### Local AI testing allowance

Finite reserves a conservative cost before every uncached OpenAI request, up to **`FINITE_AI_BUDGET_USD` total** (default $1, maximum $15) or 100 requests for this installation. The ledger lives in gitignored `backend/data/ai_budget.sqlite3`; it persists across restarts and does not reset monthly. Do not delete it to retry. `GET /api/ai-budget` reports reserved allowance, not actual billed usage. Cache hits cost no allowance; failures retain their reservation. When a request cannot fit, generation falls back to extractive mode and translation is unavailable.

Only the three default models have reviewed rates; unknown model overrides are blocked. Rates deliberately exceed standard published prices, input is conservatively counted by UTF-8 bytes plus framing, outputs are capped at 12,000 tokens, and SDK retries are disabled. Review rates against [OpenAI pricing](https://developers.openai.com/api/docs/pricing) before changing models. This guards this installation only: other apps, other checkouts, existing processes running older code, provider price changes and deleted ledgers are outside its scope. Restart the backend to load it.

AI mode now recovers from previously cached extractive story summaries after a key is added. JSON requests include the required input instruction. Live classification, embedding clustering and story generation were verified on stored news on 25 October 2026; this is a sample check, not a quality guarantee across all news.

Live AI QA (25 October): summaries, Missing Piece, Perspective Lens, two-level rabbit holes, unsupported-claim removal, challenges/Passport and Malayalam rendering were exercised in the browser. Rabbit-hole claims and dated timeline events require an explicit positive support verdict; verification failure removes them. Malformed translations fall back to the original payload. The sample is not a comprehensive editorial audit; Malayalam quality needs human review.

For controlled local demos without scheduled/background ingestion, use `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --lifespan off` **after the database has already been initialized**. Normal startup retains scheduling. This session restarted the existing backend in this controlled mode to activate the guard without spending the remaining allowance on automatic ingestion.

### Time Machine

Open a story and select **Time Machine → Trace +**. **Events in the sources** shows up to 12 dated source quotations, separating earlier background, current developments and dates needing context. Missing years and conflicting dates are not guessed. **Coverage history** shows article publication/update timestamps separately from event dates. Citations open the supporting publisher links.

This feature reads stored text only and makes no AI calls. It recognizes English date expressions and keeps excerpts in their original language; it is not a complete archive or independently verified account. Production desktop browser QA passed for citations, chronology, coverage history, empty states and error/retry. Standalone years require temporal context to avoid treating ordinary counts as dates. No additional API allowance was used.

### Connection Explorer
Open **Connection Explorer** on a story to compare up to three other stored stories sharing a saved concept. Expand **Compare source evidence** for quotations and original-source citations on both sides. This is literal shared-mention discovery, not causal inference; synonyms/translations may be missed. It respects language/source/topic exclusions and needs no additional AI calls.

Connection Explorer opens in **Knowledge map** view. Select a story node to reveal quoted evidence and citations from both stories; **List view** retains the original comparison cards. The map has at most three branches and uses no additional AI calls.

### Accounts

Open `/login` to create an account or sign in. Usernames are case-insensitive (3–32 letters, numbers or underscores). Passwords need 8–128 characters, with no character-composition rules. No password reset or email verification is included. **Settings → Sign out** ends the current session.

Profiles, briefings/read progress and Passport journeys belong to each account; article coverage and source-backed AI caches remain shared. Cookies are HttpOnly and expire after 30 days; logout revokes the server-side session. Passwords use salted scrypt ([OWASP guidance](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)); plaintext passwords/tokens are not stored. Login is throttled by username and peer IP. All data APIs require sign-in; only health and login/registration are public. Browser writes require the `X-Finite-Request: 1` header and an allowed origin.

`FINITE_ALLOWED_ORIGINS` must list the exact frontend origin; `FINITE_SECURE_COOKIES=true` is required behind HTTPS in production. Use `FINITE_SCHEDULER_ENABLED=false` when testing to avoid automatic ingestion. `FINITE_DATA_DIR` optionally relocates persistent state. Accounts require no OpenAI key.

Existing local data is preserved, but not given to the first registrant. After creating your own account and backing up the SQLite database, explicitly assign legacy history with `cd backend && uv run python -m app.claim_legacy YOUR_USERNAME`. This never overwrites an already-saved account profile. Administrative ingestion/budget access is granted locally with `uv run python -m app.manage_user YOUR_USERNAME --admin` (or `--revoke-admin`); registration never grants admin privileges.

### Oracle containers and GitHub deployment

Target: `finite.akashanil.dev` on Oracle Ampere. See [server setup and deployment](deploy/README.md) and [server-side Codex handoff](deploy/SERVER_HANDOFF.md). Two ARM64 containers sit behind the existing Caddy; persistent data stays outside images. The workflow checks code, builds and smoke-tests images, then deploys only when `FINITE_DEPLOY_ENABLED=true` and repository Actions secrets are configured. Automatic deployment on main pushes is verified; the live site is https://finite.akashanil.dev. Deployment uses a forced-command SSH key and root-owned server configuration. AI and scheduling remain disabled.

Live production QA scope and remaining verification boundaries are recorded in [LIVE_QA.md](LIVE_QA.md). Source-exclusion checkboxes are checked when excluded. Saved delivery times take effect only when scheduled delivery is enabled; production scheduling remains disabled.

## Visual design and motion

Finite uses a warm cream canvas, charcoal navigation, lime highlights and lavender/mint/yellow exploration cards. Mobile has a floating navigation dock; desktop has a navigation rail and a side-by-side reader at wide widths. Interactions include spring-like card lifts, gliding reading-depth selections, folding panels and a one-time completion flower. Reduced-motion preferences suppress decorative animation. No animation library or generated artwork was added.

The owner's [finite-ideas Pinterest board](https://in.pinterest.com/gutgbihgg/finite-ideas/) informed the palette and card compositions; no reference artwork was copied. UI QA uses an isolated database and `OPENAI_API_KEY=''`, `FINITE_SCHEDULER_ENABLED=false` so visual testing does not consume AI budget. Physical-device and cross-browser accessibility/performance audits remain pending.

Interest priorities are explicit Off / Occasional / Moderate / High choices in onboarding and Settings. Settings use animated section selectors and show saving feedback before confirmation.

See [DESIGN_QA.md](DESIGN_QA.md) for the visual references, redesign test coverage and deployed release evidence.


### Public homepage

`/` introduces Finite without requiring an account or backend request. Get started opens `/signup`; Log in opens `/login`. Successful authentication continues through `/start` to onboarding or the briefing. The existing account pages remain protected.

Connection Explorer uses conservative headline relevance: both stories must name the same subject and share at least two additional meaningful words. Candidates are ranked before selecting up to three. An empty result is expected when evidence is weak; synonyms and body-only links may be missed. Existing cached analyses are revalidated without AI regeneration.

Development AI allowance is now $5; the separately approved production allowance is $15. Set the value in the environment without deleting the existing ledger. The production template does not enable AI: an API key and explicit server-change approval are still required. Analysis validates summaries, factual claims and question premises against retrieved sources; failed summaries use literal excerpts, and unsupported questions are removed. AI checks reduce errors but cannot guarantee factual correctness.
