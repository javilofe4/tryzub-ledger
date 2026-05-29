from datetime import datetime

from pydantic import BaseModel


class ReviewUpdateRequest(BaseModel):
    reviewer_name: str
    review_status: str
    notes: str | None = None


class StatusUpdateRequest(BaseModel):
    verification_status: str
    confidence_score: int | None = None
    notes: str | None = None


class SensitiveUpdateRequest(BaseModel):
    has_sensitive_media: bool
    notes: str | None = None


class TranslationReviewRequest(BaseModel):
    language_code: str
    reviewed: bool
    notes: str | None = None


class RawItemSchema(BaseModel):
    id: int
    source_id: int
    external_id: str | None
    url: str | None
    title: str | None
    content_hash: str | None
    published_at: datetime | None
    fetched_at: datetime | None
    processing_status: str | None
    error_message: str | None

    model_config = {"from_attributes": True}
