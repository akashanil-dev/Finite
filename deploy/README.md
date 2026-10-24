# Finite on Oracle Ampere

Target: `https://finite.akashanil.dev`, on the existing Tuxos Oracle server (ARM64, 4 cores, 24 GB RAM).

Status: **ARM64 images built, smoke-tested and published by [GitHub CI](https://github.com/akashanil-dev/Finite/actions/runs/40128562535) for `9d246ab5172e9eab681eb213a276aba2b0b8e2f0`; not deployed or verified on Oracle**. Local Docker daemon access was unavailable, so hosted CI performed container validation. Deployment was skipped because FINITE_DEPLOY_ENABLED is unset. Authentication/browser tests ran locally with no AI key.

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
2. Ensure Docker Engine and Compose v2.20+ (supports `up --wait`), Git, Python 3, curl and util-linux/flock are installed. Reuse the existing Docker installation. Check `uname -m` reports `aarch64`.
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

## GitHub setup and first deployment

1. Use a dedicated Ed25519 deployment SSH key. Put its public key in `/home/finite-deploy/.ssh/authorized_keys` (directory 700, file 600, owner finite-deploy). Prefix the key with `restrict` to disable forwarding and PTY. Keep the private key only in GitHub's production environment secret.
2. Create a GitHub environment named **production** in the Finite repository. Add:
   - `DEPLOY_HOST`: Oracle SSH hostname/IP.
   - `DEPLOY_SSH_KEY`: dedicated private deployment key.
   - `DEPLOY_KNOWN_HOSTS`: the server's SSH host-key line, verified against the server console. Do not disable host verification.
3. The workflow tests on every push/PR. Main builds and smoke-tests native ARM64 images, then pushes `ghcr.io/akashanil-dev/finite-backend:<sha>` and `finite-frontend:<sha>`. It uses the repository `GITHUB_TOKEN`, with package write permission only in the image job.
4. If GHCR packages are private, run `docker login ghcr.io` **as finite-deploy** on the server using a token with `read:packages`. Alternatively make these code-only images public. No `.env`, databases or cache data enter the images.
5. Leave repository variable `FINITE_DEPLOY_ENABLED` absent/false until the server setup, environment and verified host key are ready. Then set it to `true` and run the workflow manually on main. Configure environment approval if you want to approve each release.
6. Deployment pulls both images before changes, backs up SQLite with its online backup API, starts the Compose project and waits for both health checks. On failure it restores the previous image tag when one exists. The final workflow step checks the public HTTPS health and login pages. First deployment has no previous image to roll back to.
7. On the website, create your account and sign in. Registration never grants administrator privileges. After you verify your own account, grant access to ingestion/budget administration from the server only: `FINITE_IMAGE_TAG=$(cat /opt/finite/current-release) docker compose -f /opt/finite/compose.yml exec backend python -m app.manage_user YOUR_USERNAME --admin`. Username: 3–32 letters/numbers/underscores, case-insensitive; password: 8–128 characters, no complexity rules. There is no reset or email verification.

## Existing laptop data and budget

New accounts do not inherit the old local profile or private records. Old rows remain unassigned. Create your own account locally before explicitly claiming them:

```bash
cd backend
uv run python -m app.claim_legacy YOUR_USERNAME
```

Back up first. This assigns unowned briefings/journeys and copies the legacy profile only when the account has no saved profile. It is idempotent; it does not overwrite another user's records. Do not expose this command as a web endpoint.

If retaining local history on Oracle, migrate **before allowing server registrations**: stop the laptop backend, take consistent SQLite backups, then copy the data directory (including `ai_budget.sqlite3`, not `backend/.env`) through SSH into the server volume and set ownership to 10001:finite-deploy. Start Finite and verify sign-in and history. Do not overwrite an active server database. Never copy just the main DB while writes/WAL files are active. For a fresh server with no history, still preserve the existing budget ledger before enabling the same AI key; a fresh volume otherwise has a fresh installation allowance.

## Operations and rollback

```bash
sudo -iu finite-deploy
cd /opt/finite
export FINITE_IMAGE_TAG="$(cat current-release)"
docker compose -f compose.yml ps
docker compose -f compose.yml logs --tail=100 backend frontend
```

To roll back, run `bash /opt/finite/deploy.sh PREVIOUS_FULL_COMMIT_SHA`. Backups are in `/opt/finite/backups`; retain recent backups and copy them off-server. Image rollback does not restore the database automatically. Current migrations are additive; review future migrations before rolling back. Restrict backup permissions because they contain password hashes and personal history.

Enable the scheduler only after verifying ingestion and reviewing the remaining AI allowance. One scheduler can build briefings for each onboarded account. The $1 application ledger is shared by all accounts in the installation; it is not an account-wide OpenAI billing cap.

## Codex CLI on the server

Yes: a server-side Codex CLI can inspect the live Docker/Caddy setup and perform the server steps. Use a normal SSH login, install Node/npm if needed, then:

```bash
npm install -g @openai/codex
codex login --device-auth
cd /path/to/Finite
codex
```

Complete the device-code login yourself. Use your ChatGPT login, not Finite's nearly exhausted API key. Official references: [Codex installation](https://github.com/openai/codex), [headless authentication](https://learn.chatgpt.com/docs/auth).

This laptop chat and a separately installed server CLI do not automatically share messages or state. Coordinate through the same Git repository and `PROJECT_CONTEXT.md`; give the server CLI `deploy/SERVER_HANDOFF.md`, then bring its results back here (or provide an authorized SSH host alias for direct server work). Keep application edits on the laptop and server configuration work on the server to avoid conflicting changes.
