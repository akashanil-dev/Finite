"use client";

import { useId, useState } from "react";
import { useApi } from "@/lib/hooks";
import { CitationChips } from "./citations";
import { ErrorNote, Skeleton } from "./ui";

type Timeline = {
  status: string;
  coverage_year: string | null;
  total_events: number;
  events: { date: string; text: string; precision: string; group: string; citations: string[] }[];
  coverage: { title: string; published_at: string | null; updated_at: string | null; citations: string[] }[];
  sources: Record<string, { name: string; title: string; url: string; weight: number; kind: string }>;
};

function timestamp(value: string) {
  return new Date(value).toLocaleString("en-IN", { year: "numeric", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
}

export function TimeMachine({ storyId }: { storyId: string }) {
  const [open, setOpen] = useState(false);
  const [view, setView] = useState<"events" | "coverage">("events");
  const contentId = useId();
  const { data, loading, error, reload } = useApi<Timeline>(open ? `/api/stories/${storyId}/timeline` : null);
  const lookup = (ref: string) => data?.sources[ref];
  const groups = [
    ["background", "Earlier background", "Dates before the first coverage year in this story."],
    ["current", "Current developments", "Dated passages from the coverage year onward; plans and claims remain attributed to their sources."],
    ["unresolved", "Dates needing context", "Missing years, multiple dates or unclear dates stay outside the ordered timeline. We have not filled in the gaps."],
  ];

  return (
    <section className="mt-4 rounded-3xl border border-line bg-card p-5">
      <button type="button" onClick={() => setOpen(!open)} aria-expanded={open} aria-controls={contentId} className="flex w-full items-center justify-between gap-3 text-left">
        <span><span className="block text-[11px] font-semibold uppercase tracking-[0.14em] text-muted">Time Machine</span><span className="mt-1 block font-serif text-xl">How did this story unfold?</span></span>
        <span className="shrink-0 whitespace-nowrap text-sm text-accent">{open ? "Hide −" : "Trace +"}</span>
      </button>
      {open && <div id={contentId} className="mt-4">
        {loading && <div role="status"><p className="mb-3 text-xs text-muted">Finding dated passages in the stored coverage…</p><Skeleton lines={5} /></div>}
        {error && <ErrorNote message={error} onRetry={reload} />}
        {data && <>
          <p className="text-xs leading-relaxed text-muted">A timeline of source passages, not a complete historical archive. Quotes retain their original language. No new AI generation.</p>
          <div className="mt-4 flex flex-wrap gap-2" role="group" aria-label="Timeline view">
            <button type="button" aria-pressed={view === "events"} onClick={() => setView("events")} className={`rounded-full border border-line px-3 py-2 text-xs ${view === "events" ? "bg-ink text-paper" : "bg-paper"}`}>Events in the sources</button>
            <button type="button" aria-pressed={view === "coverage"} onClick={() => setView("coverage")} className={`rounded-full border border-line px-3 py-2 text-xs ${view === "coverage" ? "bg-ink text-paper" : "bg-paper"}`}>Coverage history</button>
          </div>
          {view === "events" && <>
            {data.status === "no_dated_events" && <p className="mt-4 rounded-xl bg-paper p-3 text-sm">We couldn&apos;t identify explicit dates in the available passages. This does not mean nothing happened earlier. Coverage history still shows when these articles were published.</p>}
            {groups.map(([group, title, description]) => {
              const events = data.events.filter((event) => event.group === group);
              return events.length > 0 && <div key={group} className="mt-5">
                <h3 className="font-serif text-lg">{title}</h3>
                <p className="mt-1 text-xs leading-relaxed text-muted">{description}</p>
                <ol className="mt-4 space-y-5 border-l-2 border-accent/25 pl-4">
                  {events.map((event, i) => <li key={i} className="relative min-w-0">
                    <span aria-hidden="true" className="absolute -left-[22px] top-1.5 h-2.5 w-2.5 rounded-full bg-accent" />
                    <p className="break-words font-medium text-accent">{event.date}</p>
                    {event.precision === "year" && <p className="text-[11px] text-muted">Year only · exact date not supplied</p>}
                    <blockquote className="mt-1 break-words text-sm leading-relaxed">“{event.text}”</blockquote>
                    <CitationChips refs={event.citations} lookup={lookup} />
                  </li>)}
                </ol>
              </div>;
            })}
            {data.events.length > 0 && <p className="mt-5 text-[11px] text-muted">{data.events.length} of {data.total_events} dated passages shown · Dates are as reported, not independently verified. Different accounts may disagree. English date expressions are recognized; other dates may be missed.</p>}
          </>}
          {view === "coverage" && <div className="mt-4">
            <p className="text-xs leading-relaxed text-muted">Publication and update timestamps from the stored feeds, shown in your local timezone. These are not dates of the events themselves. An update timestamp does not tell us what changed.</p>
            {!data.coverage.length && <p className="mt-3 text-sm">No stored articles are available for this story.</p>}
            <ol className="mt-4 space-y-4 border-l-2 border-line pl-4">
              {data.coverage.map((article, i) => <li key={i} className="min-w-0">
                <p className="text-xs text-accent">{article.published_at ? `Published ${timestamp(article.published_at)}` : "Publication date unavailable"}</p>
                <p className="mt-1 break-words font-serif text-base">{article.title}</p>
                {article.updated_at && <p className="mt-1 text-xs text-muted">Updated {timestamp(article.updated_at)}</p>}
                <CitationChips refs={article.citations} lookup={lookup} />
              </li>)}
            </ol>
          </div>}
          <p className="mt-5 border-t border-line pt-3 text-xs text-muted">End of the available timeline. New evidence may fill the gaps.</p>
        </>}
      </div>}
    </section>
  );
}
