from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.session import get_session
from ...models.models import Source
from ...schemas.source import SourceSchema

router = APIRouter(tags=["sources"])


@router.get("/sources", response_model=List[SourceSchema])
async def list_sources(session: AsyncSession = Depends(get_session)) -> List[SourceSchema]:
    result = await session.execute(select(Source).order_by(Source.name.asc()))
    return result.scalars().all()


@router.get("/sources/{source_id}", response_model=SourceSchema)
async def get_source(source_id: int, session: AsyncSession = Depends(get_session)) -> SourceSchema:
    source = await session.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source
