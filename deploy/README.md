# Finite on Oracle Ampere

## Automatic deployment

The owner approved automatic deployment on pushes to main. Checks run on pushes/PRs; main builds and smoke-tests ARM64 images, publishes commit-SHA tags, and deploys over SSH when `FINITE_DEPLOY_ENABLED=true`. No production environment or paid reviewer gate is required. Unrelated server changes still require explicit approval.

Repository Actions secrets: `DEPLOY_HOST` (Oracle SSH address), `DEPLOY_SSH_KEY` (dedicated private key), `DEPLOY_KNOWN_HOSTS` (verified host key). Never commit values. The configured Ed25519 fingerprint matches `SHA256:l0cKgYBY5QHSzkHs0jpyiGtKQUvfO+8hspwpBpf2/tM`.

The key uses `restrict,command="/usr/local/lib/finite/ssh-dispatch.sh"` and permits only `deploy <40-character lowercase SHA>`. Deployment scripts and Compose live in root-owned `/usr/local/lib/finite`; SSH configuration is root-owned. Scripts are 0755, Compose/authorized_keys 0644, directories 0755. The workflow cannot upload files or obtain a shell. The deploy account retains root-equivalent Docker access; the forced command limits the key interface, not the privilege of malicious application images.

Protected script/Compose changes require a separately approved server installation; normal releases update only application images. The existing `/opt/finite` copies are historical and are not used by the Actions dispatcher. Set `FINITE_DEPLOY_ENABLED=false` to disable automated releases.

Verified setup: restricted shell/file-transfer commands rejected; deployment of the existing release through the dedicated key passed backup/health checks. Push-triggered [Actions run 40137766681](https://github.com/akashanil-dev/Finite/actions/runs/40137766681) passed checks, both ARM64 image jobs and deployment for `537687f062e2e42c080dd7d0e7ac12ab669a19d0`. Direct SSH verified that exact current-release and both healthy containers; public homepage/health returned 200, Faber/Tuxos 200, Notes its existing 401. AI and scheduler remain disabled. Finite is already live at https://finite.akashanil.dev; AI and scheduler remain disabled.

## Architecture and reference

Tuxos (`../tuxos/deploy` and its GitHub workflow) supplied the existing-host pattern: GitHub Actions over SSH, `/opt/<app>`, health checks and rollback, and the shared Caddy container. Tuxos itself uses systemd and static files; Finite uses two unprivileged containers. We do not change Tuxos files or services.

- Next.js standalone frontend (Node 24), FastAPI backend (Python 3.13), native ARM64 images in GHCR tagged by full commit SHA.
- Existing Caddy handles HTTPS and same-origin `/api/*`; no backend/frontend host ports exposed.
- `/opt/finite/data` persists SQLite, sessions, source/cache data and **the AI budget ledger** across releases. Do not replace/delete it to regain allowance.
- Backend one worker only while scheduler is in-process. Scheduler defaults off in deployment example. No API key is supplied by CI or embedded in images.
- Resource ceilings: backend 3 GB/1.5 cores, frontend 1 GB/1 core. Leave capacity for Tuxos and other sites; measure actual usage after deployment.
- Cookies are HttpOnly, SameSite=Lax and Secure in production. Exact allowed origin and custom request header protect browser writes. Caddy limits bodies to 64 KB.
- Login throttling uses persistent username and peer-IP buckets. The container intentionally ignores forwarded headers: behind Caddy, IP throttling is shared across visitors, while username buckets are separate. This is conservative for the initial launch. Configure an explicitly trusted proxy before changing this; never blindly trust client `X-Forwarded-For`.

## One-time server setup

First inspect existing services, disk space, Docker version and Caddy's Compose file. Do not stop Tuxos or replace the existing Caddyfile. The Tuxos checkout records `/home/ubuntu/Perlite/Caddyfile`; confirm this path on the live server.

1. Create a DNS A record for `finite.akashanil.dev` pointing to the same Oracle public IPv4 as Tuxos. Only add AAAA if IPv6 is actually configured. Keep the existing 80/443 ingress rules; do not open 3000/8000. With Cloudflare, use Full (strict) TLS.
2. Ensure Docker Engine and Compose v2.20+ (supports `up --wait`), Python 3, curl and util-linux/flock are installed. Reuse the existing Docker installation. Check `uname -m` reports `aarch64`.
3. Create a dedicated deploy account and directories (as the server administrator):

```bash
sudo useradd --create-home --shell /bin/bash finite-deploy
sudo usermod -aG docker finite-deploy
sudo install -d -o finite-deploy -g finite-deploy -m 750 /opt/finite
sudo install -d -o 10001 -g finite-deploy -m 2770 /opt/finite/data
sudo install -d -o finite-deploy -g finite-deploy -m 700 /opt/finite/backups
sudo install -d -o finite-deploy -g finite-deploy -m 700 /etc/finite
sudo docker network create finite-edge
```

Skip already-existing users/directories/networks after verifying their ownership. Docker-group access is root-equivalent: give this account only the dedicated deployment key and use a protected GitHub production environment.

4. Copy `deploy/backend.env.example` to `/etc/finite/backend.env`, owned by `finite-deploy`, mode 600. Leave `OPENAI_API_KEY` empty and `FINITE_SCHEDULER_ENABLED=false` initially. Never paste secrets into chat or Git.
5. In the **existing Caddy Compose file**, add this network to its `caddy` service while preserving its existing networks, volumes, ports and services:

```yaml
services:
  caddy:
    networks:
      # retain every existing network here, including default if currently implicit
      - default
      - finite-edge
networks:
  # retain existing definitions
  finite-edge:
    external: true
    name: finite-edge
```

Append the site block from `deploy/Caddyfile` to the existing mounted Caddyfile. Validate the composed configuration (`docker compose config`) and Caddy syntax (`docker compose exec caddy caddy validate --config /etc/caddy/Caddyfile`). Once Finite images are running, recreate only Caddy with `docker compose up -d --no-deps caddy` to apply the new network. Verify all existing sites afterward. No new Caddy instance should bind ports 80/443.

## GitHub setup and release verification

The automatic deployment setup above is installed. Server GHCR credentials belong to finite-deploy; private-image pulls require a valid read:packages token. Renew it before expiry. Images are built on GitHub, never on Oracle; no server checkout is required.

The deploy script pulls images, backs up existing SQLite databases, starts containers and waits for health. It restores previous images after a Compose health failure when a prior release exists. It does not restore databases. A public HTTPS failure in the later workflow check does not automatically trigger rollback. Review migrations before reverting releases.

Confirm successful Actions deployment, `/opt/finite/current-release`, container health, public `/api/health` and `/login`. A backup test passed on Oracle; the budget ledger is absent while AI is disabled. Fresh production data was selected. No laptop account/history migration was performed.

## Existing laptop data and budget

New accounts do not inherit the old local profile or private records. Old rows remain unassigned. Create your own account locally before explicitly claiming them:

```bash
cd backend
uv run python -m app.claim_legacy YOUR_USERNAME
```

Back up first. This assigns unowned briefings/journeys and copies the legacy profile only when the account has no saved profile. It is idempotent; it does not overwrite another user's records. Do not expose this command as a web endpoint.

If retaining local history on Oracle, migrate **before allowing server registrations**: stop the laptop backend, take consistent SQLite backups, then copy the data directory (including `ai_budget.sqlite3`, not `backend/.env`) through SSH into the server volume and set ownership to 10001:finite-deploy. Start Finite and verify sign-in and history. Do not overwrite an active server database. Never copy just the main DB while writes/WAL files are active. The owner subsequently approved separate allowances: $5 development and $15 production. Preserve each installation’s existing ledger; do not copy/reset the development ledger as part of production activation. These application caps do not impose an account-wide billing limit.

## Operations and rollback

```bash
sudo -iu finite-deploy
cd /opt/finite
export FINITE_IMAGE_TAG="$(cat current-release)"
docker compose -f compose.yml ps
docker compose -f compose.yml logs --tail=100 backend frontend
```

To roll back, run `bash /usr/local/lib/finite/deploy.sh PREVIOUS_FULL_COMMIT_SHA`. Backups are in `/opt/finite/backups`; retain recent backups and copy them off-server. Image rollback does not restore the database automatically. Current migrations are additive; review future migrations before rolling back. Restrict backup permissions because they contain password hashes and personal history.

Enable the scheduler only after verifying ingestion and reviewing the remaining AI allowance. One scheduler can build briefings for each onboarded account. The $1 application ledger is shared by all accounts in the installation; it is not an account-wide OpenAI billing cap.

## Codex CLI on the server

Yes: a server-side Codex CLI can inspect the live Docker/Caddy setup and perform the server steps. Use a normal SSH login, install Node/npm if needed, then:

```bash
npm install -g @openai/codex
codex login --device-auth
codex
```

Complete the device-code login yourself. Use your ChatGPT login, not Finite's nearly exhausted API key. Official references: [Codex installation](https://github.com/openai/codex), [headless authentication](https://learn.chatgpt.com/docs/auth).

This laptop chat and a separately installed server CLI do not automatically share messages or state. Provide the server CLI with the current deployment files, `PROJECT_CONTEXT.md` and `deploy/SERVER_HANDOFF.md`, then bring its results back here (or provide an authorized SSH host alias for direct server work). Keep application edits on the laptop and server configuration work on the server to avoid conflicting changes.

Backups run inside the existing backend container as UID 10001 and stream to private host backup files after integrity checking (60-second outer timeout). Do not open production WAL databases as the host deploy user: that can create sidecars the app cannot write. If a database exists but the backend is stopped, deployment aborts; recover the backend or arrange an approved offline backup first.

Production AI was explicitly approved and enabled on 25 October 2026 with `FINITE_AI_BUDGET_USD=15`; scheduling remains disabled. Environment backup: `/var/backups/finite-ai-20261025T005142Z/backend.env` (server-only, private). Future deployments retain `/etc/finite/backend.env` and `/opt/finite/data/ai_budget.sqlite3`.
