import asyncio
import logging

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.models import Conflict, Source
from app.sources.registry import SOURCE_REGISTRY

logger = logging.getLogger(__name__)

MAIN_CONFLICT = {
    "slug": "russia-war-against-ukraine",
    "name": "Russia's war against Ukraine",
    "description": "Primary conflict record for attributed open-source documentation.",
    "active": True,
}


async def seed_sources() -> dict[str, int]:
    created = 0
    updated = 0
    async with AsyncSessionLocal() as session:
        conflict = await session.scalar(select(Conflict).where(Conflict.slug == MAIN_CONFLICT["slug"]))
        if conflict is None:
            session.add(Conflict(**MAIN_CONFLICT))
            created += 1
        else:
            for key, value in MAIN_CONFLICT.items():
                setattr(conflict, key, value)
            updated += 1

        for source_def in SOURCE_REGISTRY:
            source = await session.scalar(select(Source).where(Source.slug == source_def.slug))
            payload = source_def.model_dump()
            if source is None:
                session.add(Source(**payload))
                created += 1
            else:
                for key, value in payload.items():
                    setattr(source, key, value)
                updated += 1

        await session.commit()
    return {"created": created, "updated": updated}


async def async_main() -> None:
    result = await seed_sources()
    logger.info("Seed complete: %s", result)
    print(result)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
