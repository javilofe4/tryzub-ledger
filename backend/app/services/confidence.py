def confidence_label(score: int) -> str:
    if score >= 80:
        return "very_high"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    if score >= 20:
        return "low"
    return "very_low"


def score_event(event: dict, sources: list[dict] | None = None) -> dict:
    if sources is None:
        sources = []
    score = 40
    explanation = ["Base confidence score."]
    reliable_sources = sum(1 for source in sources if source.get("reliability_score", 0) >= 60)
    if reliable_sources >= 1:
        score += 15
        explanation.append("Structured reliable source available.")
    if len(sources) >= 2:
        score += 15
        explanation.append("Multiple independent sources.")
    if event.get("location_precision") == "exact":
        score += 15
        explanation.append("Precise geolocation.")
    if event.get("has_media"):
        score += 15
        explanation.append("Media evidence reported.")
    if event.get("is_claim"):
        score -= 20
        explanation.append("Event is reported as a claim.")
    if reliable_sources == 0 and len(sources) <= 1:
        score -= 20
        explanation.append("Only one or no reliable source.")
    if event.get("propaganda_risk") == "high":
        score -= 20
        explanation.append("High propaganda risk source.")
    if event.get("verification_status") == "disputed":
        score -= 30
        explanation.append("Contradictory or disputed reporting.")
    score = max(0, min(score, 100))
    return {
        "score": score,
        "label": confidence_label(score),
        "explanation": explanation,
    }
