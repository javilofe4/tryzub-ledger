from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api.v1 import admin as admin_router
from .api.v1 import ai as ai_router
from .api.v1 import events as events_router
from .api.v1 import map as map_router
from .api.v1 import sources as sources_router
from .api.v1 import stats as stats_router
from .db.base import Base
from .db.session import engine

app = FastAPI(
    title="Tryzub Ledger API",
    description="Open-source intelligence documentation platform for Russia-Ukraine conflict analysis.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router.router, prefix="/api/v1")
app.include_router(sources_router.router, prefix="/api/v1")
app.include_router(admin_router.router, prefix="/api/v1")
app.include_router(ai_router.router, prefix="/api/v1")
app.include_router(stats_router.router, prefix="/api/v1")
app.include_router(map_router.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event() -> None:
    if settings.AUTO_CREATE_DB:
        # Development fallback only. Production schema changes must use Alembic.
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


@app.get("/health", tags=["Health"])
async def health() -> dict:
    return {"status": "ok", "service": "tryzub-ledger"}
