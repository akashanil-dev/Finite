"use client";

import { useState } from "react";
import { useApi } from "@/lib/hooks";
import { CitationChips } from "./citations";
import { Fold, ErrorNote, Skeleton, TierBadge } from "./ui";

type Lens = {
  mode: "ai" | "extractive";
  status: string;
  total_outlets: number;
  outlets: { ref: string; name: string; title: string; url: string; weight: number; tier: string; excerpt: string }[];
  claims: { text: string; category: "established" | "reported" | "disputed" | "opinion"; citations: string[] }[];
};
const categories = { established: "Corroborated in this coverage", reported: "Reported claims", disputed: "Disputed claims", opinion: "Attributed opinion" };

export function PerspectiveLens({ storyId }: { storyId: string }) {
  const [open, setOpen] = useState(false);
  const [requested, setRequested] = useState(false);
  const { data, loading, error, reload } = useApi<Lens>(requested ? `/api/stories/${storyId}/perspectives` : null);
  return (
    <section className="feature-panel feature-lens mt-4 rounded-3xl p-5">
      <button type="button" onClick={() => { setRequested(true); setOpen(!open); }} aria-expanded={open} aria-controls="perspective-content" className="flex w-full items-center justify-between gap-3 text-left">
        <span><span className="block text-[11px] font-semibold uppercase tracking-[0.14em] text-muted">Perspective Lens</span><span className="mt-1 block font-serif text-xl">How is this story being covered?</span></span>
        <span className="shrink-0 whitespace-nowrap text-sm text-accent">{open ? "Hide −" : "Compare +"}</span>
      </button>
      <Fold open={open} id="perspective-content">
        {loading && <div role="status"><p className="mb-3 text-xs text-muted">Comparing the available coverage…</p><Skeleton lines={5} /></div>}
        {error && <ErrorNote message={error} onRetry={reload} />}
        {data && <>
          <p className="text-xs leading-relaxed text-muted">
            {data.mode === "ai" ? "AI comparison · Each displayed claim passed a source-support check. Corroboration here is not independent proof." : "Source comparison · Original headlines and excerpts, without AI interpretation."}
            {" "}Different wording does not necessarily mean disagreement. Source weights are editorial judgments.
          </p>
          {data.status === "insufficient_sources" && <p className="mt-3 rounded-xl bg-paper p-3 text-sm">We need coverage from at least two distinct publishers to compare perspectives. {data.outlets.length ? "Here is the source available in this story." : "No eligible publisher coverage is available in this story."}</p>}
          {data.mode === "ai" && <div className="mt-5 space-y-4">
            {Object.entries(categories).map(([category, label]) => {
              const claims = data.claims.filter((c) => c.category === category);
              return claims.length > 0 && <div key={category}><h3 className="text-xs font-semibold uppercase tracking-wide text-accent">{label}</h3><ul className="mt-2 space-y-3 text-sm leading-relaxed">{claims.map((c, i) => <li key={i}>{c.text}<CitationChips refs={c.citations} lookup={(ref) => data.outlets.find((o) => o.ref === ref)} /></li>)}</ul></div>;
            })}
          </div>}
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {data.outlets.map((o) => <article key={o.ref} className="min-w-0 rounded-2xl border border-line bg-paper p-4">
              <TierBadge tier={o.tier} label={o.name} />
              <h3 className="mt-2 break-words font-serif text-lg leading-snug"><a href={o.url} target="_blank" rel="noreferrer" className="underline decoration-line underline-offset-4">{o.title}</a></h3>
              {o.excerpt ? <blockquote className="mt-3 text-sm leading-relaxed text-muted">“{o.excerpt}”</blockquote> : <p className="mt-3 text-xs text-muted">No excerpt available; open the original headline.</p>}
            </article>)}
          </div>
          <p className="mt-3 text-[11px] text-muted">{data.outlets.length} of {data.total_outlets} distinct publishers shown · One article per publisher · Aggregators excluded. Original excerpts retain their source language; AI comparisons are in English.</p>
        </>}
      </Fold>
    </section>
  );
}
