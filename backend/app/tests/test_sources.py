from ..sources.registry import SOURCE_REGISTRY
from ..models.models import ActorAlignment, PropagandaRisk, SourceType


def test_source_registry_has_entries() -> None:
    assert len(SOURCE_REGISTRY) >= 10
    assert any(source.slug == "isw" for source in SOURCE_REGISTRY)
    assert any(source.slug == "ukraine-general-staff" for source in SOURCE_REGISTRY)


def test_source_registry_values_match_enums() -> None:
    source_types = {item.value for item in SourceType}
    actor_alignments = {item.value for item in ActorAlignment}
    propaganda_risks = {item.value for item in PropagandaRisk}

    for source in SOURCE_REGISTRY:
        assert source.source_type in source_types
        assert source.actor_alignment in actor_alignments
        assert source.propaganda_risk in propaganda_risks
