# Project submission

Prepared for **Devin Hacks Kochi** (24–25 October 2026). Submit through the organizers' announced method before the 8:00 AM IST code freeze on 25 October.

## Project

- **Project name:** Finite
- **One-line description:** A finite, personalised daily news briefing (English and Malayalam) that lets you open any story into a source-backed rabbit hole explaining why it happened, how we got here and what it connects to. Then it ends: no endless scroll.
- **Short description:** News apps are built for endless scrolling and only answer "what happened?". Finite gives you one frozen, finite briefing a day, ranked by your weighted interests and a public source credibility index. Any story can be opened into a cited rabbit hole with a depth limit: context, then connections, then "Expedition complete". It is for readers who want to understand the news without doomscrolling.
- **Code repository URL:** https://github.com/akashanil-dev/Finite
- **Final submitted implementation commit SHA:** TODO (fill in at code freeze)
- **Working demo:** local demo, see below
- **Demo access requirements:** Python 3.13 with uv, Node.js 20+ and internet access. An OpenAI API key is optional; without it the app runs in extractive mode.

## Participant

| Participant name | GitHub handle | Contribution |
| --- | --- | --- |
| Akash A | [@akashanil-dev](https://github.com/akashanil-dev) | Concept, product decisions and direction; built with Devin (see [AI_USAGE.md](AI_USAGE.md)) |

## Run and demonstrate

- **Install:** `cd backend && uv sync`, then `cd frontend && npm install`
- **Environment variables:** `OPENAI_API_KEY` (optional), in `backend/.env`. See `backend/.env.example`.
- **Start:** `cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`, then `cd frontend && npm run dev -- -H 0.0.0.0 -p 3000`, and open http://localhost:3000
- **Demo walkthrough:**
  1. Onboarding: languages, weighted interests, exclusions and schedule.
  2. Prepare the first briefing.
  3. Read the finite feed.
  4. Open a story: summaries, cited facts, the Missing Piece.
  5. Open a rabbit hole, choose a Level 2 connection, predict its connection type (or skip), reveal the cited exploration, reach "Expedition complete", and save it to the Knowledge Passport.
  6. On a multi-publisher story, expand Perspective Lens and compare the attributed excerpts. AI grouping requires a working key.
  7. Expand Time Machine: inspect dated source passages, unresolved dates and separate coverage history. No AI calls are needed.
  8. Show the Sources page.
- **Checks performed and results:** see [CHANGELOG.md](CHANGELOG.md)
- **Known limitations:** see the Status section of [README.md](README.md)
- **Libraries, APIs and data used:** see the Data and attribution section of [README.md](README.md)
- **AI usage record:** [AI_USAGE.md](AI_USAGE.md)
- **Development change log:** [CHANGELOG.md](CHANGELOG.md)

## Submission checklist

- [x] The project was started from scratch at the event.
- [x] Solo participation.
- [x] AI usage (Devin) is documented.
- [ ] The repository URL, description and working demo are submitted through the organizers' form.
- [ ] README setup and demo instructions match the final code.
- [ ] Final checks and known limitations are documented.
- [ ] The final implementation is committed and pushed, and its SHA is recorded above.
- [x] No credentials or private data are in the repository.

Live AI demo verification (25 October): real-key summaries, Perspective Lens, Missing Piece/questions, cited two-level exploration, challenge/Passport and Malayalam rendering passed in isolated browser QA. Classification/embeddings passed via backend calls. A persistent $1 guard limits this installation; $0.776700 is reserved so far (not actual billed usage). Malayalam editorial quality and final submitted SHA remain pending.

Connection Explorer demo: open an OpenAI story, expand Connection Explorer, then Compare source evidence. Up to three cited inline comparisons end the exploration; no extra AI calls. Production desktop browser verified with real stored coverage, citation popovers, failure/retry, empty state and finite ending.

Knowledge graph demo: expand Connection Explorer, select a story node in Knowledge map, inspect both cited excerpts, then switch to List view. Desktop browser verified; three-branch maximum with no additional AI generation.

Accounts demo: create a username/password account at `/login`, save preferences, sign out and sign back in. Per-user API isolation and desktop browser flow verified; no reset flow. Oracle target is `finite.akashanil.dev`; container/CI setup prepared but not yet deployed or HTTPS-verified. Do not list this hostname as a working hosted demo until verification succeeds.

Hosted validation: [GitHub run 40128562535](https://github.com/akashanil-dev/Finite/actions/runs/40128562535) passed code checks and both ARM64 image build/smoke/publish jobs at `9d246ab`. Production deployment skipped; hostname is not yet a verified working demo.
