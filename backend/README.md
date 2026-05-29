# Tryzub Ledger Backend

FastAPI API, Alembic migrations, Celery worker tasks, and source ingestion scaffolding for Tryzub Ledger.

## Common Commands

```bash
pip install -e ".[dev]"
alembic upgrade head
python -m app.scripts.seed_sources
python -m app.scripts.ingest --enabled
pytest
```

Schema changes should be managed through Alembic migrations. `AUTO_CREATE_DB=true` exists only as an explicit local-development fallback.
