from ..services.confidence import score_event


def test_confidence_scoring_baseline() -> None:
    event = {"location_precision": "exact", "has_media": True, "is_claim": False, "verification_status": "reported", "propaganda_risk": "low"}
    sources = [{"reliability_score": 70}, {"reliability_score": 20}]
    result = score_event(event, sources)
    assert result["score"] >= 0
    assert result["label"] in {"very_low", "low", "medium", "high", "very_high"}
    assert "Precise geolocation." in result["explanation"]
