# Verification Model

Tryzub Ledger models event confidence and verification separately.

## Verification statuses

- `unverified`
- `reported`
- `probable`
- `confirmed`
- `disputed`
- `retracted`
- `false`

## Confidence scoring

Confidence scoring is a decision-support signal, not an objective truth.

### Example scoring rules

Positive factors:
- +20 structured reliable source
- +15 source with strong reliability score
- +15 visual evidence
- +15 precise geolocation
- +15 two independent sources
- +10 official source identified
- +10 consistent reporting pattern

Negative factors:
- -25 only one belligerent source
- -20 single unverified source
- -20 vague location
- -15 likely duplicate
- -20 propagandistic wording
- -30 contradiction between sources

Confidence values are normalized to 0-100 with labels from `very_low` to `very_high`.

Verification status and confidence scores are analytical aids. They do not convert official claims or single-source reports into fact without attribution and review.
