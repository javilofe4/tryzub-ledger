# Tryzub Ledger

Tryzub Ledger is an AGPL-3.0 open-source intelligence platform for documenting, structuring, verifying, mapping, and analyzing public information about Russia's war against Ukraine.

It is intended for analysts, journalists, researchers, and civil-society users who need attributed records, source review, geospatial context, confidence scoring, and multilingual presentation.

This project is an independent community initiative. It is not affiliated with the Ukrainian government, UNITED24, NATO, any military, or any intelligence service. For the official Ukraine donation and reference site, see https://u24.gov.ua/.

## Safety Boundary

Tryzub Ledger may document public events, official claims, source contradictions, losses, attacks, geospatial references, and analytical context with attribution and confidence scoring.

It must not provide targeting assistance, tactical recommendations, operational guidance, instructions for harming people, or fabricated conflict events.

## Stack

- Frontend: Next.js, TypeScript, MapLibre GL
- Backend: Python, FastAPI, SQLAlchemy, Alembic
- Database: PostgreSQL with PostGIS
- Workers: Celery with Redis
- Deployment: Docker Compose
- License: AGPL-3.0

## Docker Start

```bash
copy .env.example .env
docker compose up --build
```

Services:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

The Compose startup waits for Postgres, applies Alembic migrations, seeds the conflict and source registry records, then starts the API.

## Backend Local Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head
python -m app.scripts.seed_sources
pytest
```

Useful commands:

```bash
python -m app.scripts.ingest --enabled
python -m app.scripts.ingest --source isw
celery -A app.workers.celery_app.celery worker --loglevel=info
```

Connectors are stubs unless explicitly implemented. Stub connectors return empty results and must not fabricate events.

## Frontend Local Setup

```bash
cd frontend
npm install
npm run dev
npm run typecheck
```

Set `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` for local frontend access to the backend.

## Migrations

Schema changes are managed through Alembic:

```bash
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

`AUTO_CREATE_DB=true` is only an explicit development fallback and is disabled by default.

## Source Seeding

The seed command is idempotent:

```bash
cd backend
python -m app.scripts.seed_sources
```

It creates or updates the main conflict record and source registry entries. It does not create conflict events.

## Data Policy

No fake war data is permitted. Events must come from documented public sources, manual analyst entry, or carefully reviewed ingestion pipelines with attribution. Official claims are stored as claims, not as verified fact.

## Known Limitations

- Full login/auth is not implemented; admin routes use `ADMIN_TOKEN`.
- Source connectors are mostly planned or manual and return no records until safely implemented.
- Event normalization from raw items is not implemented.
- Report drafting and grounded chat are placeholders.
- Docker build sanity depends on local access to package registries for Python and Node dependencies.
