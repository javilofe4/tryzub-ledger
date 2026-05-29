import { notFound } from "next/navigation";
import { API_BASE_URL, EventSummary } from "../../lib/api";

type EventDetail = EventSummary & {
  latitude: number | null;
  longitude: number | null;
  location_precision: string | null;
  propaganda_risk: string | null;
  civilian_impact: string | null;
  military_relevance: string | null;
};

async function fetchEvent(id: string): Promise<EventDetail | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/events/${id}`, { cache: "no-store" });
    return res.ok ? res.json() : null;
  } catch {
    return null;
  }
}

export default async function EventDetailPage({ params }: { params: { id: string } }) {
  const event = await fetchEvent(params.id);
  if (!event) {
    notFound();
  }

  return (
    <main className="page">
      <header className="page-header">
        <h1>{event.title}</h1>
        <p>{event.summary || "No summary has been recorded for this event."}</p>
      </header>
      <dl className="panel">
        <dt>Verification status</dt>
        <dd>{event.verification_status}</dd>
        <dt>Confidence score</dt>
        <dd>{event.confidence_score}</dd>
        <dt>Location</dt>
        <dd>{event.location_name}</dd>
        <dt>Coordinates</dt>
        <dd>{event.latitude !== null && event.longitude !== null ? `${event.latitude}, ${event.longitude}` : "Not geocoded"}</dd>
        <dt>Propaganda risk</dt>
        <dd>{event.propaganda_risk}</dd>
      </dl>
    </main>
  );
}
