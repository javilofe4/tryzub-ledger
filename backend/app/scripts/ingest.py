import argparse
import asyncio
import logging

from app.db.session import AsyncSessionLocal
from app.services.ingest import ingest_enabled_sources, ingest_source_by_slug

logger = logging.getLogger(__name__)


async def async_main(args: argparse.Namespace) -> None:
    async with AsyncSessionLocal() as session:
        if args.source:
            result = await ingest_source_by_slug(session, args.source)
        else:
            result = await ingest_enabled_sources(session)
    logger.info("Ingestion complete: %s", result)
    print(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Tryzub Ledger source ingestion.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--enabled", action="store_true", help="Ingest all enabled active sources.")
    group.add_argument("--source", help="Ingest one source by registry slug.")
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = build_parser()
    asyncio.run(async_main(parser.parse_args()))


if __name__ == "__main__":
    main()
