"""Initial schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-27
"""

from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    ]


source_type = sa.Enum(
    "official_government",
    "official_military",
    "media",
    "analysis",
    "osint",
    "ngo",
    "academic",
    "international_organization",
    "dataset",
    "map",
    "social",
    "unknown",
    native_enum=False,
)
actor_alignment = sa.Enum("ukraine", "russia", "belarus", "nato", "international", "independent", "unknown", native_enum=False)
propaganda_risk = sa.Enum("low", "medium", "high", "unknown", native_enum=False)
verification_status = sa.Enum("unverified", "reported", "probable", "confirmed", "disputed", "retracted", "false", native_enum=False)
location_precision = sa.Enum("exact", "approximate", "city", "oblast", "country", "unknown", native_enum=False)
event_category = sa.Enum(
    "air_attack",
    "missile_attack",
    "drone_attack",
    "shelling",
    "ground_combat",
    "territorial_change",
    "equipment_loss",
    "casualty_claim",
    "air_defense",
    "infrastructure_damage",
    "civilian_harm",
    "naval_activity",
    "border_incident",
    "diplomatic",
    "sanctions",
    "military_aid",
    "propaganda_claim",
    "analysis",
    "other",
    native_enum=False,
)
relationship_type = sa.Enum(
    "primary_report",
    "corroborating_report",
    "contradicting_report",
    "official_claim",
    "evidence",
    "analysis",
    "correction",
    native_enum=False,
)


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "conflicts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=100), nullable=False, unique=True),
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        *timestamps(),
    )
    op.create_index("ix_conflicts_id", "conflicts", ["id"])

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False, unique=True),
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=True),
        sa.Column("language_codes", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("source_type", source_type, nullable=True),
        sa.Column("actor_alignment", actor_alignment, nullable=True),
        sa.Column("reliability_score", sa.Integer(), nullable=True),
        sa.Column("propaganda_risk", propaganda_risk, nullable=True),
        sa.Column("access_type", sa.String(length=80), nullable=True),
        sa.Column("license_note", sa.String(length=250), nullable=True),
        sa.Column("raw_data_available", sa.Boolean(), nullable=True),
        sa.Column("update_frequency_minutes", sa.Integer(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("ingestion_status", sa.String(length=40), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        *timestamps(),
    )
    op.create_index("ix_sources_id", "sources", ["id"])

    op.create_table(
        "actors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("alignment", actor_alignment, nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_actors_id", "actors", ["id"])

    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("geom", geoalchemy2.Geometry(geometry_type="POINT", srid=4326), nullable=True),
        sa.Column("country", sa.String(length=120), nullable=True),
        sa.Column("admin1", sa.String(length=120), nullable=True),
        sa.Column("admin2", sa.String(length=120), nullable=True),
        sa.Column("precision", location_precision, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_locations_id", "locations", ["id"])

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conflict_id", sa.Integer(), sa.ForeignKey("conflicts.id"), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("category", event_category, nullable=True),
        sa.Column("subcategory", sa.String(length=120), nullable=True),
        sa.Column("verification_status", verification_status, nullable=True),
        sa.Column("confidence_score", sa.Integer(), nullable=True),
        sa.Column("severity_score", sa.Integer(), nullable=True),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("detected_time", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("location_name", sa.String(length=250), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("geom", geoalchemy2.Geometry(geometry_type="POINT", srid=4326), nullable=True),
        sa.Column("country", sa.String(length=120), nullable=True),
        sa.Column("admin1", sa.String(length=120), nullable=True),
        sa.Column("admin2", sa.String(length=120), nullable=True),
        sa.Column("location_precision", location_precision, nullable=True),
        sa.Column("source_count", sa.Integer(), nullable=True),
        sa.Column("has_media", sa.Boolean(), nullable=True),
        sa.Column("has_sensitive_media", sa.Boolean(), nullable=True),
        sa.Column("is_claim", sa.Boolean(), nullable=True),
        sa.Column("claim_actor", sa.String(length=120), nullable=True),
        sa.Column("propaganda_risk", propaganda_risk, nullable=True),
        sa.Column("civilian_impact", sa.Text(), nullable=True),
        sa.Column("military_relevance", sa.Text(), nullable=True),
        *timestamps(),
    )
    op.create_index("ix_events_id", "events", ["id"])

    op.create_table(
        "raw_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("external_id", sa.String(length=250), nullable=True),
        sa.Column("url", sa.String(length=1000), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("raw_content", sa.Text(), nullable=True),
        sa.Column("raw_json", sa.JSON(), nullable=True),
        sa.Column("content_hash", sa.String(length=128), nullable=True),
        sa.Column("language_code", sa.String(length=10), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("processing_status", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_raw_items_id", "raw_items", ["id"])
    op.create_index("ix_raw_items_content_hash", "raw_items", ["content_hash"])

    op.create_table(
        "event_sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("raw_item_id", sa.Integer(), sa.ForeignKey("raw_items.id"), nullable=True),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("quote", sa.Text(), nullable=True),
        sa.Column("relationship", relationship_type, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_event_sources_id", "event_sources", ["id"])

    op.create_table(
        "event_versions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("changed_by", sa.String(length=120), nullable=True),
        sa.Column("change_type", sa.String(length=120), nullable=True),
        sa.Column("previous_data", sa.JSON(), nullable=True),
        sa.Column("new_data", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_event_versions_id", "event_versions", ["id"])

    op.create_table(
        "event_reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("reviewer_name", sa.String(length=120), nullable=True),
        sa.Column("review_status", sa.String(length=120), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_event_reviews_id", "event_reviews", ["id"])

    op.create_table(
        "event_translations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("machine_translated", sa.Boolean(), nullable=True),
        sa.Column("reviewed", sa.Boolean(), nullable=True),
        *timestamps(),
    )
    op.create_index("ix_event_translations_id", "event_translations", ["id"])

    op.create_table(
        "equipment_loss_claims",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("equipment_type", sa.String(length=250), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("claim_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_equipment_loss_claims_id", "equipment_loss_claims", ["id"])

    op.create_table(
        "casualty_claims",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("civilian_count", sa.Integer(), nullable=True),
        sa.Column("military_count", sa.Integer(), nullable=True),
        sa.Column("injured_count", sa.Integer(), nullable=True),
        sa.Column("claim_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_casualty_claims_id", "casualty_claims", ["id"])

    op.create_table(
        "frontline_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=250), nullable=True),
        sa.Column("geom", geoalchemy2.Geometry(geometry_type="MULTILINESTRING", srid=4326), nullable=True),
        sa.Column("reported_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_frontline_snapshots_id", "frontline_snapshots", ["id"])

    op.create_table(
        "territorial_control_areas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=250), nullable=True),
        sa.Column("geom", geoalchemy2.Geometry(geometry_type="MULTIPOLYGON", srid=4326), nullable=True),
        sa.Column("reported_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_territorial_control_areas_id", "territorial_control_areas", ["id"])

    op.create_table(
        "media_assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("raw_item_id", sa.Integer(), sa.ForeignKey("raw_items.id"), nullable=True),
        sa.Column("url", sa.String(length=1000), nullable=True),
        sa.Column("media_type", sa.String(length=80), nullable=True),
        sa.Column("sensitive", sa.Boolean(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_media_assets_id", "media_assets", ["id"])

    op.create_table(
        "weekly_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conflict_id", sa.Integer(), sa.ForeignKey("conflicts.id"), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("period_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=80), nullable=True),
        sa.Column("reviewed", sa.Boolean(), nullable=True),
        *timestamps(),
    )
    op.create_index("ix_weekly_reports_id", "weekly_reports", ["id"])

    op.create_table(
        "ai_summaries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=True),
        sa.Column("report_id", sa.Integer(), sa.ForeignKey("weekly_reports.id"), nullable=True),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("prompt_version", sa.String(length=120), nullable=True),
        sa.Column("model_name", sa.String(length=120), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("citations", sa.JSON(), nullable=True),
        sa.Column("reviewed", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_ai_summaries_id", "ai_summaries", ["id"])


def downgrade() -> None:
    for table in [
        "ai_summaries",
        "weekly_reports",
        "media_assets",
        "territorial_control_areas",
        "frontline_snapshots",
        "casualty_claims",
        "equipment_loss_claims",
        "event_translations",
        "event_reviews",
        "event_versions",
        "event_sources",
        "raw_items",
        "events",
        "locations",
        "actors",
        "sources",
        "conflicts",
    ]:
        op.drop_table(table)
