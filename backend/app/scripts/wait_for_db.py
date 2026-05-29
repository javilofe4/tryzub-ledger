import asyncio
import logging

from sqlalchemy import text

from app.db.session import engine

logger = logging.getLogger(__name__)


async def wait_for_db(attempts: int = 30, delay_seconds: float = 2.0) -> None:
    for attempt in range(1, attempts + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return
        except Exception as exc:
            if attempt == attempts:
                raise
            logger.info("Database not ready yet (%s/%s): %s", attempt, attempts, exc)
            await asyncio.sleep(delay_seconds)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(wait_for_db())


if __name__ == "__main__":
    main()
