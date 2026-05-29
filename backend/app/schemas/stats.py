from pydantic import BaseModel


class SummaryStats(BaseModel):
    total_events: int
    pending_review: int
    confirmed_events: int
    probable_events: int
    events_with_media: int


class WeeklyReportSummary(BaseModel):
    week_start: str
    week_end: str
    report_count: int
