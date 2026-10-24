"use client";

import { useId, useState } from "react";
import { useApi } from "@/lib/hooks";
import { CitationChips } from "./citations";
import { ErrorNote, Skeleton } from "./ui";

type Evidence = { text: string; name: string; title: string; url: string; weight: number; kind: string };
type Connections = { connections: { story_id: string; title: string; concept: string; evidence: Evidence[] }[]; candidate_limit: number; limit: number };

export function ConnectionExplorer({ storyId }: { storyId: string }) {
  const [open, setOpen] = useState(false);
  const contentId = useId();
  const { data, loading, error, reload } = useApi<Connections>(open ? `/api/stories/${storyId}/connections` : null);
  return <section className="mt-4 rounded-3xl border border-line bg-card p-5">
    <button type="button" onClick={() => setOpen(!open)} aria-expanded={open} aria-controls={contentId} className="flex w-full items-center justify-between gap-3 text-left">
      <span><span className="block text-[11px] font-semibold uppercase tracking-[0.14em] text-muted">Connection Explorer</span><span className="mt-1 block font-serif text-xl">What else does this connect to?</span></span>
      <span className="shrink-0 text-sm text-accent">{open ? "Hide −" : "Connect +"}</span>
    </button>
    {open && <div id={contentId} className="mt-4">
      {loading && <div role="status"><p className="mb-3 text-xs text-muted">Looking for shared mentions in stored stories…</p><Skeleton lines={4} /></div>}
      {error && <ErrorNote message={error} onRetry={reload} />}
      {data && <>
        <p className="text-xs leading-relaxed text-muted">Shared mentions, not proof of a causal relationship. Compare the original coverage below; no new AI generation.</p>
        {!data.connections.length && <p className="mt-4 rounded-xl bg-paper p-3 text-sm">No source-backed matches found in the available stories. Connections need a saved concept and an explicit mention in both stories; we won&apos;t invent a link.</p>}
        <ol className="mt-4 space-y-4">
          {data.connections.map((connection, i) => <li key={connection.story_id} className="rounded-2xl border border-line bg-paper p-4">
            <p className="text-xs font-medium text-accent">{i + 1} · Shared mention: {connection.concept}</p>
            <h3 className="mt-2 break-words font-serif text-lg">{connection.title}</h3>
            <details className="mt-3">
              <summary className="cursor-pointer text-sm text-accent">Compare source evidence</summary>
              <div className="mt-3 space-y-4">
                {connection.evidence.map((evidence, index) => <div key={index} className="min-w-0">
                  <p className="text-[11px] font-semibold uppercase tracking-wide text-muted">{index === 0 ? "This story" : "Connected story"}</p>
                  <blockquote className="mt-1 break-words text-sm leading-relaxed">“{evidence.text}”</blockquote>
                  <CitationChips refs={[String(index)]} lookup={() => evidence} />
                </div>)}
              </div>
            </details>
          </li>)}
        </ol>
        <p className="mt-5 border-t border-line pt-3 text-xs leading-relaxed text-muted">End of connections · Up to {data.limit} matches from the latest {data.candidate_limit} stored stories, respecting your language and exclusion settings. Exact mentions can miss synonyms and translations. Quotes retain their original language.</p>
      </>}
    </div>}
  </section>;
}
