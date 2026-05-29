from datetime import datetime
from typing import List

from pydantic import Field

from .base import BaseConfigModel


class EventSourceSchema(BaseConfigModel):
    id: int
    source_id: int
    raw_item_id: int | None
    source_url: str | None
    quote: str | None
    relationship: str | None
    created_at: datetime | None


class EventTranslationSchema(BaseConfigModel):
    id: int
    language_code: str
    title: str | None
    summary: str | None
    machine_translated: bool
    reviewed: bool
    created_at: datetime | None
    updated_at: datetime | None


class EventSummarySchema(BaseConfigModel):
    id: int
    title: str
    summary: str | None
    category: str | None
    verification_status: str | None
    confidence_score: int
    event_time: datetime | None
    location_name: str | None
    country: str | None
    admin1: str | None
    source_count: int
    has_sensitive_media: bool
    is_claim: bool
    created_at: datetime | None


class EventDetailSchema(EventSummarySchema):
    subcategory: str | None
    severity_score: int
    detected_time: datetime | None
    latitude: float | None
    longitude: float | None
    location_precision: str | None
    has_media: bool
    claim_actor: str | None
    propaganda_risk: str | None
    civilian_impact: str | None
    military_relevance: str | None
    event_sources: List[EventSourceSchema] = Field(default_factory=list)
    translations: List[EventTranslationSchema] = Field(default_factory=list)
