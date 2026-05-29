import { fetchJson, SourceSummary } from "../lib/api";

export default async function SourcesPage() {
  const sources = await fetchJson<SourceSummary[]>("/api/v1/sources", []);

  return (
    <main className="page">
      <header className="page-header">
        <h1>Sources</h1>
        <p>Registry entries describe source provenance, access status, and ingestion readiness. Planned or manual sources do not run automated collection.</p>
      </header>
      {sources.length === 0 ? (
        <div className="panel empty-state">No sources available. Run the source seed command after applying migrations.</div>
      ) : (
        <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Alignment</th>
              <th>Risk</th>
              <th>Status</th>
              <th>Enabled</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((source) => (
              <tr key={source.id}>
                <td>{source.url ? <a href={source.url}>{source.name}</a> : source.name}</td>
                <td>{source.source_type}</td>
                <td>{source.actor_alignment}</td>
                <td>{source.propaganda_risk}</td>
                <td>{source.ingestion_status}</td>
                <td>{source.enabled ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      )}
    </main>
  );
}
