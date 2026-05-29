export default function ChatPage() {
  return (
    <main className="page">
      <header className="page-header">
        <h1>Grounded Chat</h1>
        <p>Analytical chat is disabled by default. Any future assistant must be citation-grounded and must refuse tactical or targeting assistance.</p>
      </header>
      <section className="panel empty-state">AI provider is disabled unless explicitly configured.</section>
    </main>
  );
}
