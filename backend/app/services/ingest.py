import hashlib
import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.models import RawItem, Source
from ..sources.connectors import StubConnector
from ..sources.registry import SOURCE_REGISTRY

logger = logging.getLogger(__name__)

CONNECTOR_MAP = {
    "russian-casualties-in-ua": StubConnector(),
    "isw": StubConnector(),
    "acled-ukraine-conflict-monitor": StubConnector(),
    "liveuamap": StubConnector(),
    "viina": StubConnector(),
    "oryx": StubConnector(),
    "ukrdailyupdate": StubConnector(),
    "ukraine-general-staff": StubConnector(),
    "russian-mod": StubConnector(),
    "osw-arms-deliveries": StubConnector(),
    "kaggle-missile-attacks": StubConnector(),
    "nasa-firms": StubConnector(),
    "reliefweb-hdx": StubConnector(),
}


def compute_hash(raw_content: str | bytes) -> str:
    if isinstance(raw_content, str):
        raw_content = raw_content.encode("utf-8")
    return hashlib.sha256(raw_content).hexdigest()


async def ingest_enabled_sources(session: AsyncSession) -> dict[str, Any]:
    results = {"processed": 0, "created": 0, "errors": []}
    for source_def in SOURCE_REGISTRY:
        if not source_def.enabled or source_def.ingestion_status != "active":
            continue
        source_result = await ingest_source_by_slug(session, source_def.slug)
        results["processed"] += source_result["processed"]
        results["created"] += source_result["created"]
        results["errors"].extend(source_result["errors"])
    return results


async def ingest_source_by_slug(session: AsyncSession, slug: str) -> dict[str, Any]:
    results = {"processed": 0, "created": 0, "errors": []}
    source_def = next((source for source in SOURCE_REGISTRY if source.slug == slug), None)
    if source_def is None:
        results["errors"].append(f"Unknown source slug: {slug}")
        return results

    connector = CONNECTOR_MAP.get(source_def.slug)
    if not connector:
        results["errors"].append(f"No connector for {source_def.slug}")
        return results

    try:
        raw_items = await connector.fetch()
        results["processed"] += 1
        for raw_item in raw_items:
            content = raw_item.get("raw_content") or str(raw_item.get("raw_json", ""))
            content_hash = compute_hash(content)
            existing = await session.execute(select(RawItem).where(RawItem.content_hash == content_hash))
            if existing.scalars().first():
                continue
            source = await session.execute(select(Source).where(Source.slug == source_def.slug))
            source_obj = source.scalars().first()
            if not source_obj:
                results["errors"].append(f"Source not seeded in database: {source_def.slug}")
                continue
            item = RawItem(
                source_id=source_obj.id,
                external_id=raw_item.get("external_id"),
                url=raw_item.get("url"),
                title=raw_item.get("title"),
                raw_content=raw_item.get("raw_content"),
                raw_json=raw_item.get("raw_json"),
                content_hash=content_hash,
                language_code=raw_item.get("language_code", "en"),
            )
            session.add(item)
            results["created"] += 1
        await session.commit()
    except Exception as exc:  # pragma: no cover
        logger.exception("Source ingestion failed for %s", source_def.slug)
        results["errors"].append(f"{source_def.slug}: {exc}")
        await session.rollback()
    return results
