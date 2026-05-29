import "./globals.css";
import "maplibre-gl/dist/maplibre-gl.css";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Tryzub Ledger",
  description: "Open-source intelligence platform for documenting conflict data.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const navItems = [
    { href: "/", label: "Overview" },
    { href: "/map", label: "Map" },
    { href: "/events", label: "Events" },
    { href: "/sources", label: "Sources" },
    { href: "/reports", label: "Reports" },
    { href: "/chat", label: "Chat" },
    { href: "/admin", label: "Admin" },
  ];

  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <aside className="sidebar">
            <div>
              <div className="brand">Tryzub Ledger</div>
              <div className="subtle">OSINT documentation workspace</div>
            </div>
            <nav className="nav-list" aria-label="Primary navigation">
              {navItems.map((item) => (
                <Link key={item.href} href={item.href}>
                  {item.label}
                </Link>
              ))}
            </nav>
          </aside>
          <div className="content-shell">{children}</div>
        </div>
      </body>
    </html>
  );
}
