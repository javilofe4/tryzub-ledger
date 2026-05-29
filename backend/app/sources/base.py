from abc import ABC, abstractmethod
from typing import Any, Dict, List


RawItemPayload = Dict[str, Any]


class SourceConnector(ABC):
    slug: str
    name: str

    @abstractmethod
    async def fetch(self) -> List[RawItemPayload]:
        raise NotImplementedError

    @abstractmethod
    async def normalize(self, raw_item: RawItemPayload) -> List[Dict[str, Any]]:
        raise NotImplementedError
