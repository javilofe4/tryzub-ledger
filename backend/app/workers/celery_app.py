import asyncio
from celery import Celery

from ..core.config import settings
from ..services.ingest import ingest_enabled_sources

celery = Celery(
    "tryzub_ledger_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)
celery.conf.task_serializer = "json"
celery.conf.result_serializer = "json"
celery.conf.accept_content = ["json"]
celery.conf.result_expires = 3600


@celery.task(name="tryzub_ledger.ingest_enabled_sources")
def ingest_enabled_sources_task() -> dict:
    # Worker task executes the source ingestion pipeline.
    return asyncio.run(ingest_enabled_sources_task_impl())


async def ingest_enabled_sources_task_impl() -> dict:
    from ..db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        return await ingest_enabled_sources(session)
