"use client";

import { useId, useState } from "react";
import { useApi } from "@/lib/hooks";
import { CitationChips } from "./citations";
import { ErrorNote, Skeleton } from "./ui";

type Evidence = { text: string; name: string; title: string; url: string; weight: number; kind: string };
type Connections = { connections: { story_id: string; title: string; concept: string; evidence: Evidence[] }[]; candidate_limit: number; limit: number };

export function ConnectionExplorer({ storyId, storyTitle }: { storyId: string; storyTitle: string }) {
  const [open, setOpen] = useState(false);
  const contentId = useId();
  const [view, setView] = useState<"map" | "list">("map");
  const [selected, setSelected] = useState<string | null>(null);
  const evidenceId = useId();
  const { data, loading, error, reload } = useApi<Connections>(open ? `/api/stories/${storyId}/connections` : null);
  const active = data?.connections.find((connection) => connection.story_id === selected);
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
        {!!data.connections.length && <>
          <div className="mt-4 flex gap-2" role="group" aria-label="Connection view">
            {(["map", "list"] as const).map((mode) => <button key={mode} type="button" aria-pressed={view === mode} onClick={() => setView(mode)} className={`rounded-full border border-line px-4 py-2 text-sm ${view === mode ? "bg-ink text-paper" : "bg-paper"}`}>{mode === "map" ? "Knowledge map" : "List view"}</button>)}
          </div>
          {view === "map" && <div className="mt-4">
            <p className="text-xs text-muted">Select a story node to compare its sources. Each branch is a shared mention; this map ends here.</p>
            <div className="mt-4 rounded-2xl border border-line bg-paper p-3 sm:p-4" role="group" aria-label="Knowledge graph">
              <div className="mx-auto max-w-sm rounded-2xl border-2 border-accent bg-card p-4 text-center">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-accent">This story · starting point</p>
                <p className="mt-2 break-words font-serif text-base">{storyTitle}</p>
              </div>
              <div aria-hidden="true" className="h-6 w-1/2 border-b border-r border-accent/50" />
              <div className="space-y-3 border-l border-accent/50 pl-3 sm:pl-5">
                {data.connections.map((connection, i) => <div key={connection.story_id} className="relative">
                  <span aria-hidden="true" className="absolute -left-3 top-7 w-3 border-t border-accent/50 sm:-left-5 sm:w-5" />
                  <button type="button" aria-pressed={selected === connection.story_id} aria-controls={evidenceId} onClick={() => setSelected(connection.story_id)} className={`w-full rounded-xl border p-3 text-left focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent ${selected === connection.story_id ? "border-accent bg-accent/10" : "border-line bg-card"}`}>
                    <span className="block break-words text-xs font-medium text-accent">{i + 1} · Shared mention: {connection.concept}</span>
                    <span className="mt-1 block break-words font-serif text-base">{connection.title}</span>
                    <span className="mt-2 block text-xs text-muted">{selected === connection.story_id ? "Selected · evidence below" : "Compare evidence →"}</span>
                  </button>
                </div>)}
              </div>
            </div>
            <div id={evidenceId} className="mt-4 rounded-2xl border border-line p-4" aria-live="polite">
              {active ? <>
                <h3 className="break-words font-serif text-lg">Shared mention: {active.concept}</h3>
                <p className="mt-1 break-words text-sm text-muted">{active.title}</p>
                {active.evidence.map((evidence, index) => <div key={`${active.story_id}-${index}`} className="mt-4 min-w-0">
                  <p className="text-[11px] font-semibold uppercase tracking-wide text-muted">{index === 0 ? "This story" : "Connected story"}</p>
                  <blockquote className="mt-1 break-words text-sm leading-relaxed">“{evidence.text}”</blockquote>
                  <CitationChips refs={[String(index)]} lookup={() => evidence} />
                </div>)}
              </> : <p className="text-sm text-muted">Choose a connected story above to see the evidence on both sides.</p>}
            </div>
          </div>}
        </>}
        {view === "list" && <ol className="mt-4 space-y-4">
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
        </ol>}
        <p className="mt-5 border-t border-line pt-3 text-xs leading-relaxed text-muted">End of connections · Up to {data.limit} matches from the latest {data.candidate_limit} stored stories, respecting your language and exclusion settings. Exact mentions can miss synonyms and translations. Quotes retain their original language.</p>
      </>}
    </div>}
  </section>;
}
