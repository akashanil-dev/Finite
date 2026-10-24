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
# Run SQLite backup as the application UID inside the existing container. Opening
# WAL databases from the host deploy account can create sidecars the app cannot write.
for name in finite.db ai_budget.sqlite3; do
    [[ -f "$root/data/$name" ]] || continue
    backend="$(docker compose -f "$compose_file" ps -q backend)"
    [[ -n "$backend" ]] || { echo 'Existing database requires a running backend for backup.' >&2; exit 1; }
    stamp="$(date -u +%Y%m%dT%H%M%S%N)"
    backup="$root/backups/$stamp-$name"
    if timeout 60 docker exec -i "$backend" python - "$name" > "$backup.tmp" <<'PYBACKUP'
import pathlib, sqlite3, sys, tempfile, time
source = pathlib.Path('/data') / sys.argv[1]
deadline = time.monotonic() + 45

def progress(status, remaining, total):
    if time.monotonic() > deadline:
        raise TimeoutError('Database backup timed out')

with tempfile.TemporaryDirectory() as temporary:
    target = pathlib.Path(temporary) / 'backup.db'
    with sqlite3.connect(f"file:{source}?mode=ro", uri=True, timeout=5) as src, sqlite3.connect(target) as dst:
        src.backup(dst, pages=256, progress=progress)
        if dst.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise RuntimeError('Backup integrity check failed')
    with target.open('rb') as stream:
        import shutil
        shutil.copyfileobj(stream, sys.stdout.buffer)
PYBACKUP
    then
        mv -- "$backup.tmp" "$backup"
    else
        rm -f -- "$backup.tmp"
        echo "Backup failed for $name; deployment stopped." >&2
        exit 1
    fi
done
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
