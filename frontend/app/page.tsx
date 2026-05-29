import { fetchJson } from "./lib/api";

type Summary = {
  total_events: number;
  pending_review: number;
  confirmed_events: number;
  probable_events: number;
  events_with_media: number;
};

export default async function Home() {
  const summary = await fetchJson<Summary | null>("/api/v1/stats/summary", null);

  return (
    <main className="page">
      <header className="page-header">
        <h1>Overview</h1>
        <p>Analyst workspace for attributed open-source documentation, verification review, and source registry management.</p>
      </header>
      <section>
        {summary ? (
          <div className="metric-grid">
            <div className="metric"><div className="metric-label">Total events</div><div className="metric-value">{summary.total_events}</div></div>
            <div className="metric"><div className="metric-label">Pending review</div><div className="metric-value">{summary.pending_review}</div></div>
            <div className="metric"><div className="metric-label">Confirmed</div><div className="metric-value">{summary.confirmed_events}</div></div>
            <div className="metric"><div className="metric-label">Probable</div><div className="metric-value">{summary.probable_events}</div></div>
            <div className="metric"><div className="metric-label">Events with media</div><div className="metric-value">{summary.events_with_media}</div></div>
          </div>
        ) : (
          <div className="panel empty-state">Unable to load summary. The backend may not be ready.</div>
        )}
      </section>
    </main>
  );
}
