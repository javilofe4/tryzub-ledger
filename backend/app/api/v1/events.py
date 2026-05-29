from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.session import get_session
from ...models.models import Event
from ...schemas.event import EventDetailSchema, EventSummarySchema

router = APIRouter(tags=["events"])


def enum_value(value):
    return getattr(value, "value", value)


@router.get("/events", response_model=List[EventSummarySchema])
async def list_events(
    category: str | None = Query(None),
    verification_status: str | None = Query(None),
    confidence_label: str | None = Query(None),
    source: int | None = Query(None),
    country: str | None = Query(None),
    admin1: str | None = Query(None),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[EventSummarySchema]:
    query = select(Event)
    if category:
        query = query.where(Event.category == category)
    if verification_status:
        query = query.where(Event.verification_status == verification_status)
    if country:
        query = query.where(Event.country == country)
    if admin1:
        query = query.where(Event.admin1 == admin1)
    if start_date:
        query = query.where(Event.event_time >= start_date)
    if end_date:
        query = query.where(Event.event_time <= end_date)
    query = query.order_by(Event.event_time.desc().nullslast()).limit(200)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/events/{event_id}", response_model=EventDetailSchema)
async def get_event(event_id: int, session: AsyncSession = Depends(get_session)) -> EventDetailSchema:
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get("/events.geojson")
async def events_geojson(session: AsyncSession = Depends(get_session)) -> dict:
    query = select(Event).order_by(Event.event_time.desc().nullslast()).limit(500)
    result = await session.execute(query)
    events = result.scalars().all()
    features = []
    for event in events:
        if event.latitude is None or event.longitude is None:
            continue
        features.append(
            {
                "type": "Feature",
                "id": event.id,
                "geometry": {
                    "type": "Point",
                    "coordinates": [event.longitude, event.latitude],
                },
                "properties": {
                    "title": event.title,
                    "category": enum_value(event.category),
                    "verification_status": enum_value(event.verification_status),
                    "propaganda_risk": enum_value(event.propaganda_risk),
                    "location_precision": enum_value(event.location_precision),
                    "confidence_score": event.confidence_score,
                    "location_name": event.location_name,
                    "source_count": event.source_count,
                    "has_sensitive_media": event.has_sensitive_media,
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}
