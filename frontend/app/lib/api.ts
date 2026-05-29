export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export type EventSummary = {
  id: number;
  title: string;
  summary: string | null;
  category: string | null;
  verification_status: string | null;
  confidence_score: number;
  event_time: string | null;
  location_name: string | null;
  country: string | null;
  admin1: string | null;
  source_count: number;
  has_sensitive_media: boolean;
  is_claim: boolean;
};

export type SourceSummary = {
  id: number;
  slug: string;
  name: string;
  url: string | null;
  source_type: string | null;
  actor_alignment: string | null;
  propaganda_risk: string | null;
  reliability_score: number;
  enabled: boolean;
  ingestion_status: string | null;
};

export async function fetchJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });
    return res.ok ? ((await res.json()) as T) : fallback;
  } catch {
    return fallback;
  }
}
