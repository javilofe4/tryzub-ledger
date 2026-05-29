from typing import Any, Dict, List

from .base import RawItemPayload, SourceConnector


class StubConnector(SourceConnector):
    slug = "stub"
    name = "Stub Connector"

    async def fetch(self) -> List[RawItemPayload]:
        # No credentialed public source is implemented yet. This stub preserves connector structure.
        return []

    async def normalize(self, raw_item: RawItemPayload) -> List[Dict[str, Any]]:
        return []


class PlannedConnector(SourceConnector):
    slug = "planned"
    name = "Planned Source Connector"

    async def fetch(self) -> List[RawItemPayload]:
        return []

    async def normalize(self, raw_item: RawItemPayload) -> List[Dict[str, Any]]:
        return []


class PublicApiConnector(SourceConnector):
    slug = "public-api"
    name = "Public API Connector"

    async def fetch(self) -> List[RawItemPayload]:
        return []

    async def normalize(self, raw_item: RawItemPayload) -> List[Dict[str, Any]]:
        return []
