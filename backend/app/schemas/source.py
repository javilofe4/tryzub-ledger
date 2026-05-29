from datetime import datetime
from typing import List

from pydantic import Field

from .base import BaseConfigModel


class SourceSchema(BaseConfigModel):
    id: int
    slug: str
    name: str
    url: str | None
    language_codes: List[str] = Field(default_factory=list)
    source_type: str | None
    actor_alignment: str | None
    reliability_score: int
    propaganda_risk: str | None
    access_type: str | None
    raw_data_available: bool
    update_frequency_minutes: int
    enabled: bool
    ingestion_status: str | None
    notes: str | None
    created_at: datetime | None
    updated_at: datetime | None
