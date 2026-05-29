# Data Model

Tryzub Ledger is designed around a normalized conflict and event tracking model.

## Key tables

- `conflicts`: tracks major conflict contexts and enables multi-conflict support.
- `sources`: stores metadata about each source, including reliability, propaganda risk, language, and access mode.
- `raw_items`: preserves ingested raw payloads and source references.
- `events`: stores normalized event summaries, geolocation, classification, confidence, and review state.
- `event_sources`: associates events with raw reports and relationships.
- `event_versions`: records event edits and changes over time.
- `event_reviews`: tracks human review actions and review status.
- `event_translations`: stores translated titles and summaries with review workflows.
- `locations`, `actors`, `equipment_loss_claims`, `casualty_claims`, `frontline_snapshots`, `territorial_control_areas`, `media_assets`, `ai_summaries`, `weekly_reports`: support richer structured analysis.

## Geospatial support

- `events.geom` stores event point geometry.
- `territorial_control_areas.geom` stores polygon geometries.
- `frontline_snapshots.geom` stores line or multi-line geometries.

The model is migration-ready and intentionally extensible for future OSINT event normalization.

## Seeded records

The seed command creates the main conflict record and source registry rows only. It does not create events, claims, casualties, losses, territorial changes, or frontline data.
