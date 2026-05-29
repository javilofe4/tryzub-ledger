from fastapi import APIRouter

router = APIRouter(tags=["map"])


@router.get("/map/layers")
async def get_map_layers() -> dict:
    return {
        "layers": [
            {
                "id": "events",
                "title": "Events",
                "description": "Event point layer from public OSINT documentation.",
                "source": "/api/v1/events.geojson",
                "type": "point",
            },
            {
                "id": "territorial_control",
                "title": "Territorial control (scaffold)",
                "description": "Planned territorial control geometry layer.",
                "source": "planned",
                "type": "polygon",
            },
        ]
    }
