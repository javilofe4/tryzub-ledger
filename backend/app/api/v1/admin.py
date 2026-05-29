from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...admin.deps import get_admin_token
from ...db.session import get_session
from ...models.models import Event, EventReview, EventTranslation, RawItem, VerificationStatus
from ...schemas.admin import (
    RawItemSchema,
    ReviewUpdateRequest,
    SensitiveUpdateRequest,
    StatusUpdateRequest,
    TranslationReviewRequest,
)
from ...schemas.event import EventSummarySchema

router = APIRouter(tags=["admin"], dependencies=[Depends(get_admin_token)])


@router.get("/admin/raw-items", response_model=list[RawItemSchema])
async def list_raw_items(session: AsyncSession = Depends(get_session)) -> list[RawItemSchema]:
    result = await session.execute(select(RawItem).order_by(RawItem.fetched_at.desc()).limit(200))
    return result.scalars().all()


@router.get("/admin/events/pending")
async def pending_events(session: AsyncSession = Depends(get_session)) -> list[EventSummarySchema]:
    result = await session.execute(select(Event).where(Event.verification_status == "unverified").order_by(Event.event_time.desc().nullslast()).limit(200))
    return result.scalars().all()


@router.post("/admin/events/{event_id}/review")
async def review_event(event_id: int, payload: ReviewUpdateRequest, session: AsyncSession = Depends(get_session)) -> dict:
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    review = EventReview(
        event_id=event_id,
        reviewer_name=payload.reviewer_name,
        review_status=payload.review_status,
        notes=payload.notes,
    )
    session.add(review)
    await session.commit()
    return {"detail": "Review saved"}


@router.post("/admin/events/{event_id}/status")
async def update_event_status(event_id: int, payload: StatusUpdateRequest, session: AsyncSession = Depends(get_session)) -> dict:
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    try:
        event.verification_status = VerificationStatus(payload.verification_status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid verification status")
    if payload.confidence_score is not None:
        event.confidence_score = payload.confidence_score
    await session.commit()
    return {"detail": "Event status updated"}


@router.post("/admin/events/{event_id}/merge")
async def merge_event(event_id: int, session: AsyncSession = Depends(get_session)) -> dict:
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"detail": "Merge endpoint scaffolded. Manual merge workflow required."}


@router.post("/admin/events/{event_id}/sensitive")
async def mark_sensitive(event_id: int, payload: SensitiveUpdateRequest, session: AsyncSession = Depends(get_session)) -> dict:
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.has_sensitive_media = payload.has_sensitive_media
    await session.commit()
    return {"detail": "Sensitive flag updated"}


@router.post("/admin/events/{event_id}/translation-review")
async def translation_review(event_id: int, payload: TranslationReviewRequest, session: AsyncSession = Depends(get_session)) -> dict:
    translation = await session.execute(
        select(EventTranslation)
        .where(EventTranslation.event_id == event_id)
        .where(EventTranslation.language_code == payload.language_code)
    )
    translation = translation.scalars().first()
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    translation.reviewed = payload.reviewed
    await session.commit()
    return {"detail": "Translation review updated"}
