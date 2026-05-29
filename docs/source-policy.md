# Source Policy

Tryzub Ledger classifies sources by type, actor alignment, propaganda risk, and access model.

## Source types

- `official_government`
- `official_military`
- `media`
- `analysis`
- `osint`
- `ngo`
- `academic`
- `international_organization`
- `dataset`
- `map`
- `social`
- `unknown`

## Official claims

Official military or government claims are treated as source reports, not objective fact.
They are attributed, labeled, and scored for confidence.

## Propaganda risk

Sources may be tagged with low, medium, high, or unknown propaganda risk.
This helps analysts distinguish likely state messaging or unverifiable claims from more reliable reporting.

## No fabricated data

The platform does not invent events or claims. Records are created only from documented public sources or ingestion pipelines.

## Ingestion status

Each source is marked as one of:

- `active`: automated ingestion is enabled and reviewed.
- `planned`: listed for future implementation.
- `manual`: should be entered or reviewed by a human instead of scraped.
- `disabled`: should not be ingested.

Paid, credentialed, or fragile sources must not be implemented as free public connectors. API keys and private credentials must not be committed.
