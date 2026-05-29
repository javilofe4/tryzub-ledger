# Architecture

Tryzub Ledger is a monorepo with separate backend, frontend, and worker components.

## Backend

- Python FastAPI application in `backend/app`
- SQLAlchemy + Alembic for database models and migrations
- PostgreSQL + PostGIS for structured and geospatial data
- Redis + Celery for background ingestion tasks

## Frontend

- Next.js + TypeScript in `frontend`
- App Router with pages for dashboard, map, events, sources, admin, reports, and chat
- MapLibre GL for geospatial rendering

## Workers

- Celery worker defined in `backend/app/workers/celery_app.py`
- Scheduled ingestion tasks are scaffolded for later source pipelines

## Ingestion flow

1. Source registry defines planned and active sources.
2. Connector classes fetch raw payloads and preserve raw items.
3. The ingestion service computes hashes, avoids duplicates, and creates raw records.
4. Normalized event creation is planned as a follow-on step.

Stub and planned connectors return empty results. They must not emit sample events or inferred facts.

## Database lifecycle

- Alembic is the primary schema strategy.
- The initial migration creates the PostGIS extension and all current model tables.
- `AUTO_CREATE_DB=true` is reserved for explicit local development fallback only.
- `python -m app.scripts.seed_sources` seeds the main conflict and source registry records without creating events.

## Admin review flow

- Admin endpoints are protected by `ADMIN_TOKEN`.
- Reviewers can inspect pending events, update verification status, mark sensitive content, and add review notes.
- Translation review and version history are scaffolded in the data model.
