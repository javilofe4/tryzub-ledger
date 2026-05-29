from ..schemas.event import EventSummarySchema
from ..api.v1.events import enum_value
from ..models.models import EventCategory, LocationPrecision, PropagandaRisk, VerificationStatus


def test_event_schema_serialization() -> None:
    data = {
        "id": 1,
        "title": "Test event",
        "summary": "A summary.",
        "category": "air_attack",
        "verification_status": "unverified",
        "confidence_score": 50,
        "event_time": None,
        "location_name": "Kyiv",
        "country": "Ukraine",
        "admin1": "Kyiv",
        "source_count": 1,
        "has_sensitive_media": False,
        "is_claim": False,
    }
    event = EventSummarySchema.model_validate(data)
    assert event.title == "Test event"
    assert event.confidence_score == 50


def test_geojson_enum_values_are_strings() -> None:
    properties = {
        "category": enum_value(EventCategory.air_attack),
        "verification_status": enum_value(VerificationStatus.reported),
        "propaganda_risk": enum_value(PropagandaRisk.low),
        "location_precision": enum_value(LocationPrecision.exact),
    }
    assert properties == {
        "category": "air_attack",
        "verification_status": "reported",
        "propaganda_risk": "low",
        "location_precision": "exact",
    }
