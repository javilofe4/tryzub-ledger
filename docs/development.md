# Development

## Environment

Copy `.env.example` to `.env` and replace local placeholders. Do not commit real `.env` files or credentials.

`NEXT_PUBLIC_API_BASE_URL` should be `http://localhost:8000` for local browser access.

## Backend

```bash
cd backend
pip install -e ".[dev]"
alembic upgrade head
python -m app.scripts.seed_sources
pytest
```

Run ingestion without creating fabricated records:

```bash
python -m app.scripts.ingest --enabled
python -m app.scripts.ingest --source isw
```

## Frontend

```bash
cd frontend
npm install
npm run dev
npm run typecheck
```

## Docker

```bash
docker compose up --build
```

Compose starts PostGIS, Redis, the FastAPI backend, the Celery worker, and the Next.js frontend. The backend startup waits for Postgres, applies migrations, and seeds registry data.
