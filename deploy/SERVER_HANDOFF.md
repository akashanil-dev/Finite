# Finite server handoff

Finite is live at https://finite.akashanil.dev on Oracle ARM64, alongside Faber, Tuxos and Notes. Fresh production data was selected. AI and scheduling remain disabled; do not enable the laptop key without preserving its existing budget ledger.

## Authorization

The owner explicitly approved automatic deployment on every main push after successful checks and ARM64 image publication. This supersedes earlier instructions requiring approval for each routine release. All other server/configuration changes require a concrete proposal and explicit approval before execution.

## Installed deployment path

GitHub builds and publishes images; Oracle does not clone source or build it. The workflow uses repository secrets DEPLOY_HOST, DEPLOY_SSH_KEY and DEPLOY_KNOWN_HOSTS, and variable FINITE_DEPLOY_ENABLED=true. Set the variable false to disable deployment. No production environment reviewer gate is used.

The dedicated key permits only `deploy <full lowercase SHA>` through /usr/local/lib/finite/ssh-dispatch.sh. That directory, deploy.sh, compose.yml and the SSH authorization files are root-owned. Shell and file-transfer commands are rejected. Runtime data/backups/release markers remain in /opt/finite; environment is /etc/finite/backend.env. Protected script/config updates need separate approval and installation; do not replace them from Actions. The account has root-equivalent Docker access; command restrictions do not sandbox deployed images.

## Preserve shared infrastructure

Caddy runs in a container managed by /home/ubuntu/Perlite/docker-compose.caddy.yml. /home/ubuntu/Perlite/Caddyfile is mounted at /etc/caddy/Caddyfile. Independently reverify live mounts, networks and configuration before changes. Preserve perlite-net, finite-edge, Caddy volumes, /opt/tuxos and /run/tuxos mounts and every existing site. Never bring down the shared stack to deploy Finite.

Owner-supplied HTTPS results: Finite origin/public homepage and health returned 200; Faber/Tuxos retained 200; Notes retained its prior 401. This does not resolve Notes authentication/application issues. Caddy backup: /var/backups/finite-caddy-20261024T220242234822Z.

## Verification and recovery

The dedicated key successfully redeployed the existing 9d246ab release; backups and container health passed. Push-triggered [Actions run 40137766681](https://github.com/akashanil-dev/Finite/actions/runs/40137766681) passed checks, both ARM64 image jobs and deployment for `537687f062e2e42c080dd7d0e7ac12ab669a19d0`. Direct SSH verified that exact current-release and both healthy containers; public homepage/health returned 200, Faber/Tuxos 200, Notes its existing 401. AI and scheduler remain disabled. A prior database online-backup integrity check passed. Image rollback does not restore data, first deployments have no previous image, and post-deploy public HTTP check failures do not automatically roll back. Report actual CI, release SHA, container and HTTPS evidence; never infer live success solely from published images.

Read AGENTS.md, RULES.md, PROJECT_CONTEXT.md and deploy/README.md. Coordinate application changes with the laptop; no server repository clone is required. Never expose private keys, credential files or environment values.
