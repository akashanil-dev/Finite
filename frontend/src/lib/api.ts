export type Subfield = { id: string; name: string };
export type Field = { id: string; name: string; subfields: Subfield[] };

export type Meta = {
  app_name: string;
  mock_mode: boolean;
  max_depth: number;
  taxonomy: Field[];
  languages: { id: string; name: string; native?: string }[];
  periods: { id: string; label: string; range: string; time: string }[];
  depths: { id: Depth; label: string; desc: string }[];
  last_ingest: { at: number; articles_seen: number } | null;
};

export type Depth = "quick" | "standard" | "deep";

export type Profile = {
  onboarded: boolean;
  languages: string[];
  ui_language: string;
  interests: Record<string, number>;
  excluded_subfields: string[];
  excluded_sources: string[];
  delivery_time: string;
  timezone: string;
  lookback_hours: number;
  stories_per_briefing: number;
  depth: Depth;
};

export type SourceRef = { id: string; name: string; tier: string; weight: number; url: string; title: string };

export type StoryCard = {
  id: string;
  title: string;
  lang: string;
  story_type: string;
  subfields: { id: string; name: string; score: number }[];
  published_at: number;
  updated_at: number;
  sources: SourceRef[];
  teaser: string;
  analyzed: boolean;
};

export type Briefing = {
  id: number;
  created_at: number;
  window_start: number;
  window_end: number;
  config: Profile;
  stories: StoryCard[];
  read_ids: string[];
  completed_at: number | null;
};

export type Cited = { text: string; citations: string[] };
export type Question = { id: string; question: string; angle: string; blurb: string; search: string[] };

export type Analysis = {
  summary: Record<Depth, string>;
  what_happened: Cited[];
  missing_piece: { question: string; why: string }[];
  questions: Question[];
  concepts: string[];
  story_type: string;
  mode: "ai" | "extractive";
  translation?: string;
  articles: { ref: string; source: string; title: string; url: string; tier: string; weight: number; published_at: number; updated_at: number }[];
};

export type ExploreNode = { heading: string; text: string; citations: string[]; confidence: "verified" | "reported" | "disputed" };
export type NextQuestion = { question: string; angle: string; search: string[] };

export type Exploration = {
  key: string;
  question: string;
  title?: string;
  angle: string;
  depth: number;
  max_depth: number;
  nodes: ExploreNode[];
  timeline?: { date: string; event: string; citations: string[] }[];
  next_questions?: NextQuestion[];
  concepts?: string[];
  insufficient?: boolean;
  off_topic?: boolean;
  dropped_claims?: number;
  mode?: string;
  translation?: string;
  sources?: Record<string, { kind: string; name: string; title: string; url: string; weight: number }>;
};

export type Passport = {
  journeys: { id: number; story_id: string; story_title: string; path: { question: string; prediction?: string }[]; concepts: string[]; created_at: number }[];
  concepts: { name: string; count: number }[];
  areas: { name: string; count: number }[];
  briefings_completed: number;
  questions_explored: number;
};

export type SourcesIndex = {
  tiers: Record<string, { label: string; description: string }>;
  sources: { id: string; name: string; homepage: string; lang: string; tier: string; weight: number; rationale: string; feed: string }[];
  context_sources: { id: string; name: string; homepage: string; tier: string; weight: number; rationale: string }[];
  methodology: string[];
};

function base() {
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  if (typeof window !== "undefined") return `${window.location.protocol}//${window.location.hostname}:8000`;
  return "http://localhost:8000";
}

export async function api<T>(path: string, init?: RequestInit & { json?: unknown }): Promise<T> {
  const { json, ...rest } = init ?? {};
  const res = await fetch(base() + path, {
    ...rest,
    headers: { "Content-Type": "application/json", ...(rest.headers ?? {}) },
    body: json !== undefined ? JSON.stringify(json) : rest.body,
    cache: "no-store",
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail ?? detail;
    } catch {}
    throw new Error(detail);
  }
  return res.json();
}

export const PRIORITY_LABELS: Record<number, string> = { 1: "Occasional", 2: "Moderate", 3: "High" };

export function timeAgo(ts: number) {
  const s = Date.now() / 1000 - ts;
  if (s < 3600) return `${Math.max(1, Math.round(s / 60))}m ago`;
  if (s < 86400) return `${Math.round(s / 3600)}h ago`;
  return `${Math.round(s / 86400)}d ago`;
}

export function fmtTime(ts: number) {
  return new Date(ts * 1000).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" });
}
