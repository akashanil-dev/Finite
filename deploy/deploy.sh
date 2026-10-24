#!/usr/bin/env bash
# Run on Oracle as finite-deploy. Images are immutable commit-SHA tags.
set -euo pipefail
umask 077
release="${1:?usage: deploy.sh COMMIT_SHA}"
[[ "$release" =~ ^[0-9a-f]{40}$ ]] || { echo 'Expected a full commit SHA' >&2; exit 1; }
root=/opt/finite
# Production installs this script and Compose file together in a root-owned directory.
config_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
compose_file="$config_dir/compose.yml"
exec 9>"$root/deploy.lock"
flock -n 9 || { echo 'Another deployment is running' >&2; exit 1; }
cd "$root"
previous="$(cat current-release 2>/dev/null || true)"
export FINITE_IMAGE_TAG="$release"
# Download everything before touching the running release.
docker compose -f "$compose_file" pull
mkdir -p backups
# SQLite online backup includes committed WAL data. Keep both databases, including the budget ledger.
python3 - <<'PY'
import datetime, pathlib, sqlite3
root = pathlib.Path('/opt/finite')
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
for name in ('finite.db', 'ai_budget.sqlite3'):
    source = root / 'data' / name
    if source.exists():
        with sqlite3.connect(f"file:{source}?mode=ro", uri=True) as src, sqlite3.connect(root / 'backups' / f'{stamp}-{name}') as dst:
            src.backup(dst)
PY
if docker compose -f "$compose_file" up -d --wait --wait-timeout 120; then
    printf '%s\n' "$release" > current-release
    printf '%s\n' "$previous" > previous-release
    echo "Finite release $release is healthy."
else
    echo 'Deployment failed; restoring previous images when available.' >&2
    if [[ "$previous" =~ ^[0-9a-f]{40}$ ]]; then
        export FINITE_IMAGE_TAG="$previous"
        docker compose -f "$compose_file" up -d --wait --wait-timeout 120
    fi
    exit 1
fi
