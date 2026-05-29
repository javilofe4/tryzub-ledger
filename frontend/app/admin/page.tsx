export default function AdminPage() {
  return (
    <main className="page">
      <header className="page-header">
        <h1>Admin</h1>
        <p>Protected review endpoints require the configured ADMIN_TOKEN. Full user authentication is intentionally not implemented yet.</p>
      </header>
      <section className="panel">
        <table>
          <tbody>
            <tr><th>Raw item review</th><td>Use backend admin endpoints for pending raw source material.</td></tr>
            <tr><th>Event status</th><td>Manual verification, disputed status, and sensitive media flags are handled through protected API calls.</td></tr>
            <tr><th>Access model</th><td>Bearer token only for the first commit baseline.</td></tr>
          </tbody>
        </table>
      </section>
    </main>
  );
}
