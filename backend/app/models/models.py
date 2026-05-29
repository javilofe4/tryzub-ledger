import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from ..db.base import Base


class SourceType(enum.Enum):
    official_government = "official_government"
    official_military = "official_military"
    media = "media"
    analysis = "analysis"
    osint = "osint"
    ngo = "ngo"
    academic = "academic"
    international_organization = "international_organization"
    dataset = "dataset"
    map = "map"
    social = "social"
    unknown = "unknown"


class ActorAlignment(enum.Enum):
    ukraine = "ukraine"
    russia = "russia"
    belarus = "belarus"
    nato = "nato"
    international = "international"
    independent = "independent"
    unknown = "unknown"


class PropagandaRisk(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    unknown = "unknown"


class VerificationStatus(enum.Enum):
    unverified = "unverified"
    reported = "reported"
    probable = "probable"
    confirmed = "confirmed"
    disputed = "disputed"
    retracted = "retracted"
    false = "false"


class LocationPrecision(enum.Enum):
    exact = "exact"
    approximate = "approximate"
    city = "city"
    oblast = "oblast"
    country = "country"
    unknown = "unknown"


class EventCategory(enum.Enum):
    air_attack = "air_attack"
    missile_attack = "missile_attack"
    drone_attack = "drone_attack"
    shelling = "shelling"
    ground_combat = "ground_combat"
    territorial_change = "territorial_change"
    equipment_loss = "equipment_loss"
    casualty_claim = "casualty_claim"
    air_defense = "air_defense"
    infrastructure_damage = "infrastructure_damage"
    civilian_harm = "civilian_harm"
    naval_activity = "naval_activity"
    border_incident = "border_incident"
    diplomatic = "diplomatic"
    sanctions = "sanctions"
    military_aid = "military_aid"
    propaganda_claim = "propaganda_claim"
    analysis = "analysis"
    other = "other"


class RelationshipType(enum.Enum):
    primary_report = "primary_report"
    corroborating_report = "corroborating_report"
    contradicting_report = "contradicting_report"
    official_claim = "official_claim"
    evidence = "evidence"
    analysis = "analysis"
    correction = "correction"


class Conflict(Base):
    __tablename__ = "conflicts"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    events = relationship("Event", back_populates="conflict")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(120), unique=True, nullable=False)
    name = Column(String(250), nullable=False)
    url = Column(String(500))
    language_codes = Column(ARRAY(String), default=[])
    source_type = Column(SAEnum(SourceType, native_enum=False), default=SourceType.unknown)
    actor_alignment = Column(SAEnum(ActorAlignment, native_enum=False), default=ActorAlignment.unknown)
    reliability_score = Column(Integer, default=0)
    propaganda_risk = Column(SAEnum(PropagandaRisk, native_enum=False), default=PropagandaRisk.unknown)
    access_type = Column(String(80), default="public")
    license_note = Column(String(250))
    raw_data_available = Column(Boolean, default=False)
    update_frequency_minutes = Column(Integer, default=60)
    enabled = Column(Boolean, default=False)
    ingestion_status = Column(String(40), default="planned")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    raw_items = relationship("RawItem", back_populates="source")
    event_sources = relationship("EventSource", back_populates="source")


class RawItem(Base):
    __tablename__ = "raw_items"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    external_id = Column(String(250))
    url = Column(String(1000))
    title = Column(String(500))
    raw_content = Column(Text)
    raw_json = Column(JSON)
    content_hash = Column(String(128), index=True)
    language_code = Column(String(10), default="en")
    published_at = Column(DateTime(timezone=True))
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    processing_status = Column(String(64), default="pending")
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source = relationship("Source", back_populates="raw_items")
    event_sources = relationship("EventSource", back_populates="raw_item")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    conflict_id = Column(Integer, ForeignKey("conflicts.id"), nullable=False)
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    category = Column(SAEnum(EventCategory, native_enum=False), default=EventCategory.other)
    subcategory = Column(String(120))
    verification_status = Column(SAEnum(VerificationStatus, native_enum=False), default=VerificationStatus.unverified)
    confidence_score = Column(Integer, default=0)
    severity_score = Column(Integer, default=0)
    event_time = Column(DateTime(timezone=True))
    detected_time = Column(DateTime(timezone=True), server_default=func.now())
    location_name = Column(String(250))
    latitude = Column(Float)
    longitude = Column(Float)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
    country = Column(String(120))
    admin1 = Column(String(120))
    admin2 = Column(String(120))
    location_precision = Column(SAEnum(LocationPrecision, native_enum=False), default=LocationPrecision.unknown)
    source_count = Column(Integer, default=0)
    has_media = Column(Boolean, default=False)
    has_sensitive_media = Column(Boolean, default=False)
    is_claim = Column(Boolean, default=False)
    claim_actor = Column(String(120))
    propaganda_risk = Column(SAEnum(PropagandaRisk, native_enum=False), default=PropagandaRisk.unknown)
    civilian_impact = Column(Text)
    military_relevance = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    conflict = relationship("Conflict", back_populates="events")
    event_sources = relationship("EventSource", back_populates="event")
    event_versions = relationship("EventVersion", back_populates="event")
    event_reviews = relationship("EventReview", back_populates="event")
    translations = relationship("EventTranslation", back_populates="event")
    media_assets = relationship("MediaAsset", back_populates="event")
    ai_summaries = relationship("AISummary", back_populates="event")


class EventSource(Base):
    __tablename__ = "event_sources"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    raw_item_id = Column(Integer, ForeignKey("raw_items.id"), nullable=True)
    source_url = Column(String(1000))
    quote = Column(Text)
    relationship = Column(SAEnum(RelationshipType, native_enum=False), default=RelationshipType.primary_report)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="event_sources")
    source = relationship("Source", back_populates="event_sources")
    raw_item = relationship("RawItem", back_populates="event_sources")


class EventVersion(Base):
    __tablename__ = "event_versions"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    changed_by = Column(String(120))
    change_type = Column(String(120))
    previous_data = Column(JSON)
    new_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="event_versions")


class EventReview(Base):
    __tablename__ = "event_reviews"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    reviewer_name = Column(String(120))
    review_status = Column(String(120))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="event_reviews")


class EventTranslation(Base):
    __tablename__ = "event_translations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    language_code = Column(String(10), nullable=False)
    title = Column(String(500))
    summary = Column(Text)
    machine_translated = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    event = relationship("Event", back_populates="translations")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
    country = Column(String(120))
    admin1 = Column(String(120))
    admin2 = Column(String(120))
    precision = Column(SAEnum(LocationPrecision, native_enum=False), default=LocationPrecision.unknown)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    alignment = Column(SAEnum(ActorAlignment, native_enum=False), default=ActorAlignment.unknown)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EquipmentLossClaim(Base):
    __tablename__ = "equipment_loss_claims"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    equipment_type = Column(String(250))
    quantity = Column(Integer)
    claim_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CasualtyClaim(Base):
    __tablename__ = "casualty_claims"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    civilian_count = Column(Integer)
    military_count = Column(Integer)
    injured_count = Column(Integer)
    claim_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FrontlineSnapshot(Base):
    __tablename__ = "frontline_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    geom = Column(Geometry(geometry_type="MULTILINESTRING", srid=4326))
    reported_at = Column(DateTime(timezone=True))
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TerritorialControlArea(Base):
    __tablename__ = "territorial_control_areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    geom = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326))
    reported_at = Column(DateTime(timezone=True))
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    raw_item_id = Column(Integer, ForeignKey("raw_items.id"), nullable=True)
    url = Column(String(1000))
    media_type = Column(String(80), default="image")
    sensitive = Column(Boolean, default=False)
    description = Column(Text)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="media_assets")


class AISummary(Base):
    __tablename__ = "ai_summaries"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    report_id = Column(Integer, ForeignKey("weekly_reports.id"), nullable=True)
    language_code = Column(String(10), nullable=False)
    prompt_version = Column(String(120))
    model_name = Column(String(120))
    summary = Column(Text)
    citations = Column(JSON)
    reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="ai_summaries")


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(Integer, primary_key=True, index=True)
    conflict_id = Column(Integer, ForeignKey("conflicts.id"), nullable=False)
    language_code = Column(String(10), nullable=False)
    title = Column(String(500))
    summary = Column(Text)
    body = Column(Text)
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    status = Column(String(80), default="draft")
    reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
