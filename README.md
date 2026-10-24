# Finite

**News that ends. Understanding that doesn't.**

Finite is a finite, personalised daily news briefing (English and Malayalam). Most news apps answer *what happened* and then keep you scrolling. Finite also helps you see **why it happened, how we got here, and what it connects to**, through source-backed "rabbit holes" that go a fixed number of levels deep and always end. You finish your briefing, and you're done.

Built solo by Akash A ([@akashanil-dev](https://github.com/akashanil-dev)) with Devin at **[Devin Hacks Kochi](https://www.devinhacks.in/)**, 24–25 October 2026.

| Event document | Purpose |
| --- | --- |
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
6. **Knowledge Passport:** the concepts you've explored, with no streaks.
7. **Sources page:** a public credibility index of every outlet Finite reads, with its tier, confidence weight and the reason for it.

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
```

## Status

- **Working, tested without an AI key:** reading 29 English and Malayalam feeds, sorting stories into topics, grouping duplicates, weighted ranking, frozen briefings with read progress and completion, story summaries and questions, rabbit holes with a depth limit, ask-your-own, Knowledge Passport, the sources page, and the scheduler.
- **Built but not yet tested with a real key:** AI summaries and questions (`gpt-6-luna`), AI rabbit holes (`gpt-6.1-sol`) with claim-by-claim checking, embedding-based duplicate grouping, and Malayalam translation.
- **Known limitations:**
  - Single local user only.
  - Topic sorting without a key is approximate.
  - Duplicate grouping without a key sometimes splits one event into two stories.
  - Source weights are editorial judgements.
  - Perspective Lens and Curiosity Challenges are planned.

## Data and attribution

Publisher RSS feeds are listed in `backend/app/sources.py`. Finite shows short summaries with attribution and always links to the original article. Background passages come from the [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) (CC BY-SA), and each citation links to the article used. Fonts are Inter, Newsreader and Noto Sans Malayalam (Google Fonts).
