#!/usr/bin/env bash
# Forced SSH command. Install root-owned alongside deploy.sh and compose.yml.
set -euo pipefail
command_pattern='^deploy ([0-9a-f]{40})$'
if [[ "${SSH_ORIGINAL_COMMAND:-}" =~ $command_pattern ]]; then
    release="${BASH_REMATCH[1]}"
else
    echo 'Only deploy followed by a full lowercase commit SHA is permitted.' >&2
    exit 1
fi
# Do not inherit Compose overrides, shell startup files or image-prefix overrides.
exec /usr/bin/env -i HOME=/home/finite-deploy USER=finite-deploy LOGNAME=finite-deploy \
    PATH=/usr/bin:/bin DOCKER_CONFIG=/home/finite-deploy/.docker \
    /bin/bash --noprofile --norc /usr/local/lib/finite/deploy.sh "$release"
