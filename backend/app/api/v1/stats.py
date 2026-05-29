from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.session import get_session
from ...models.models import Event
from ...schemas.stats import SummaryStats

router = APIRouter(tags=["stats"])


@router.get("/stats/summary", response_model=SummaryStats)
async def get_summary(session: AsyncSession = Depends(get_session)) -> SummaryStats:
    total_events = await session.scalar(select(func.count(Event.id)))
    pending_review = await session.scalar(select(func.count(Event.id)).where(Event.verification_status == "unverified"))
    confirmed_events = await session.scalar(select(func.count(Event.id)).where(Event.verification_status == "confirmed"))
    probable_events = await session.scalar(select(func.count(Event.id)).where(Event.verification_status == "probable"))
    events_with_media = await session.scalar(select(func.count(Event.id)).where(Event.has_media == True))
    return SummaryStats(
        total_events=total_events or 0,
        pending_review=pending_review or 0,
        confirmed_events=confirmed_events or 0,
        probable_events=probable_events or 0,
        events_with_media=events_with_media or 0,
    )
