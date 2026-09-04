# AGENTS.md

## Project

`job-monitor` collects Work24 job postings, stores them in MariaDB, filters them by rules, and sends matching jobs to Slack.

## Structure

- `collector-work24/` — Work24 collector (Python)
- `database/` — MariaDB schema and SQL
- `docs/` — design and technical documentation

## Development

- Core: Java 21 / Spring Boot / Maven
- DB: MariaDB / MyBatis
- UI: Thymeleaf
- Notification: Slack
- Collector: Python
- Use the existing tools and project structure. Avoid unnecessary new dependencies or abstractions.
- Read relevant `docs/` before changing architecture or data flow.

## Collector

- Work24 is the current job-data source.
- Avoid unnecessary requests and preserve existing pagination/collection behavior.
- Prefer idempotent collection and DB updates.
- Keep credentials in environment variables; never hard-code secrets.

## Testing

- Python: run `pytest` from `collector-work24/` for collector changes.
- Java: run the relevant Maven tests for Java changes.
- Add or update tests when behavior changes.
- Fix errors introduced by your changes before finishing.

## Git

- Do not commit, create branches, push, release, or deploy unless explicitly requested.
- Do not modify unrelated files or rewrite history.
- Keep changes focused on the requested task.

## Database

- Do not make destructive schema/data changes unless explicitly requested.
- Update `database/` when the schema changes.
- Never commit passwords, API keys, tokens, webhooks, or secret `.env` files.

## Completion

Before finishing:

1. Verify the requested behavior.
2. Run relevant tests.
3. Check the changed files.
4. Check for secrets.
5. Report what changed and what was tested.
