import Link from "next/link";
import { EventSummary, fetchJson } from "../lib/api";

export default async function EventsPage() {
  const events = await fetchJson<EventSummary[]>("/api/v1/events", []);

  return (
    <main className="page">
      <header className="page-header">
        <h1>Events</h1>
        <p>Structured event records appear here only after attributed source ingestion or manual review workflows create them.</p>
      </header>
      <section className="panel" style={{ marginBottom: "16px" }}>
        <div className="filter-grid">
          <label>Category<select defaultValue=""><option value="">All categories</option><option value="air_attack">Air attack</option><option value="civilian_harm">Civilian harm</option><option value="infrastructure_damage">Infrastructure damage</option></select></label>
          <label>Verification<select defaultValue=""><option value="">All statuses</option><option value="unverified">Unverified</option><option value="reported">Reported</option><option value="probable">Probable</option><option value="confirmed">Confirmed</option><option value="disputed">Disputed</option></select></label>
          <label>Country<input placeholder="Country" /></label>
          <label>Admin region<input placeholder="Admin 1" /></label>
        </div>
      </section>
      {events.length === 0 ? (
        <div className="panel empty-state">No events ingested yet. Seed sources, enable verified connectors, and run ingestion.</div>
      ) : (
        <div className="panel">
          <table>
            <thead><tr><th>Title</th><th>Status</th><th>Confidence</th><th>Location</th><th>Sources</th></tr></thead>
            <tbody>
          {events.map((event) => (
            <tr key={event.id}>
              <td><Link href={`/events/${event.id}`}>{event.title}</Link><br />{event.summary}</td>
              <td>{event.verification_status}</td>
              <td>{event.confidence_score}</td>
              <td>{event.location_name || event.admin1 || event.country || "Unknown"}</td>
              <td>{event.source_count}</td>
            </tr>
          ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}
