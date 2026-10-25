# Proposed production scheduler activation — not yet approved

After the compact-reader release passes CI/CD:

1. Read-only: verify current release, container health, scheduler flag and remaining production budget without exposing keys.
2. Back up `/etc/finite/backend.env` into a root-only timestamped `/var/backups/finite-scheduler-*` directory, preserving ownership/mode.
3. Change only `FINITE_SCHEDULER_ENABLED` to `true`. Preserve the API key, $15 cap, request ceiling, databases and budget reservations.
4. Recreate only Finite backend using `/usr/local/lib/finite/compose.yml` and `/opt/finite/current-release`; no pulls, Caddy/DNS/network or other application changes.
5. Verify health and effective scheduler flag. Inspect one scheduler tick and saved-edition metadata without printing personal content or secrets. Do not alter user schedules for a test.

Impact: brief backend interruption. Background ingestion can start immediately and can use remaining production API allowance; due onboarded users receive saved editions if matching new stories exist. Later checks run every five minutes and ingestion follows its configured interval. It does not guarantee new matching stories every day or an exact delivery minute.

Rollback if startup fails: restore the saved environment and recreate only that backend at the same release. Preserve any newly created editions and budget reservations. A real clock-triggered delivery remains unverified until observed.
