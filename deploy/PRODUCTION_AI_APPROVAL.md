# Proposed production AI activation — requires owner approval

This batch was explicitly approved by the owner and executed on 25 October 2026 after CI run 40148109626 passed. The backend became healthy, AI enabled was confirmed, and the independent production ledger reported $15 available before the live sample. Backup: `/var/backups/finite-ai-20261025T005142Z`. Routine SHA deployments are already authorized; changing Oracle AI configuration is a separate owner-required approval.

After the new release passes CI/CD:

1. Read-only: verify the deployed SHA, backend health, `/etc/finite/backend.env` metadata, and existing budget ledger status without printing key values.
2. Create a root-only timestamped backup of `/etc/finite/backend.env` on Oracle.
3. Securely transfer the existing laptop backend API key over SSH into the server-only environment file (never command-line arguments, Git, GitHub secrets, logs or chat). Preserve its ownership/mode. Set `FINITE_AI_BUDGET_USD=15`, keep `FINITE_SCHEDULER_ENABLED=false`, and leave all other settings intact.
4. Recreate only the backend with the current deployed release's Compose configuration. Do not alter Caddy, DNS, networks or other applications. Preserve `/opt/finite/data`, including any existing `ai_budget.sqlite3`; do not create or reset a ledger for this step.
5. Verify health and the effective non-secret budget/scheduler settings, then run one bounded production AI/browser sample within the $15 production guard. The application also has a 100-request ceiling; this is not an account-wide billing limit.

Impact: a brief backend interruption and subsequent user-triggered OpenAI usage up to the application guard. No scheduled ingestion is enabled. Existing users' cached extractive stories can regenerate on demand.

Rollback on failure: restore the backed-up environment file and recreate only the backend at the same release. Preserve all databases and reservations, including any incurred during validation. Report failure and verify service health; do not erase usage to restore allowance.
