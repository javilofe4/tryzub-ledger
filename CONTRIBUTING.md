# Contributing to Tryzub Ledger

## Local development

1. Copy `.env.example` to `.env`.
2. Start core services:
   ```bash
   docker compose up --build
   ```
3. Backend tests:
   ```bash
   ./scripts/test.sh
   ```
4. Frontend lint/typecheck:
   ```bash
   ./scripts/lint.sh
   ```

## Adding a source connector

1. Add a new source definition in `backend/app/sources/registry.py`.
2. Implement a connector in `backend/app/sources/connectors.py`.
3. Add connector mapping in `backend/app/services/ingest.py`.
4. Confirm the connector preserves raw payloads and computes content hashes.
5. Do not create fabricated event records.

## Coding standards

- Use TypeScript for frontend code.
- Use Python typing and Pydantic schemas for backend code.
- Keep the analyst UI sober and focused.
- Do not add non-free or credentialed source integrations without clear documentation.

## Issues and PRs

- Open issues for missing connectors, data model questions, and UI/UX improvements.
- Provide clear change summaries and tests for features.
