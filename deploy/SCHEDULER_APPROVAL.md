# Production scheduler activation — approved and executed

After the compact-reader release passes CI/CD:

1. Read-only: verify current release, container health, scheduler flag and remaining production budget without exposing keys.
2. Back up `/etc/finite/backend.env` into a root-only timestamped `/var/backups/finite-scheduler-*` directory, preserving ownership/mode.
3. Change only `FINITE_SCHEDULER_ENABLED` to `true`. Preserve the API key, $15 cap, request ceiling, databases and budget reservations.
4. Recreate only Finite backend using `/usr/local/lib/finite/compose.yml` and `/opt/finite/current-release`; no pulls, Caddy/DNS/network or other application changes.
5. Verify health and effective scheduler flag. Inspect one scheduler tick and saved-edition metadata without printing personal content or secrets. Do not alter user schedules for a test.

Impact: brief backend interruption. Background ingestion can start immediately and can use remaining production API allowance; due onboarded users receive saved editions if matching new stories exist. Later checks run every five minutes and ingestion follows its configured interval. It does not guarantee new matching stories every day or an exact delivery minute.

Rollback if startup fails: restore the saved environment and recreate only that backend at the same release. Preserve any newly created editions and budget reservations. A real clock-triggered delivery remains unverified until observed.

## Execution evidence — 25 October 2026

Owner explicitly approved this batch. After Actions run 40149975675 passed and release `f8a537905b08e053bc3461be77c7a18b8b55bd72` was verified, the environment was backed up to `/var/backups/finite-scheduler-20261025T012150Z/backend.env`. Only the scheduler flag changed; only the backend was recreated. Both containers were healthy and public `/api/health` returned 200. No rollback was required.

The first scheduled ingestion completed: 974 articles seen and 34 classified in 24.3 seconds. Production reservations were $0.795639 of $15, 25 of 100 requests, at that checkpoint; this is not billed usage or a permanently current balance. No scheduled edition row existed at verification time; real delivery remains unobserved. No user schedule was altered for testing.
