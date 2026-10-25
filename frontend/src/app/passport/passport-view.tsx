"use client";

import Link from "next/link";
import { fmtTime, type Passport } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { ErrorNote, Eyebrow, Shell, Skeleton } from "@/components/ui";

export default function PassportPage() {
  const { data: p, error } = useApi<Passport>("/api/passport");
  const maxArea = Math.max(1, ...(p?.areas.map((a) => a.count) ?? [1]));
  return (
    <Shell>
      <Eyebrow>Knowledge passport</Eyebrow>
      <h1 className="mt-2 font-serif text-3xl leading-tight">Where your curiosity has taken you</h1>
      <p className="mt-2 text-sm text-muted">Your saved explorations, questions and reading history. A record of curiosity, not a measure of mastery.</p>

      {error && <div className="mt-6"><ErrorNote message={error} /></div>}
      {!p && !error && <div className="mt-8"><Skeleton lines={5} /></div>}

      {p && (
        <>
          <div className="passport-stats rise mt-6 grid grid-cols-3 gap-3">
            {[
              [p.journeys.length, "Saved expeditions"],
              [p.questions_explored, "Question steps"],
              [p.briefings_completed, "Briefings marked read"],
            ].map(([n, l]) => (
              <div key={l} className="rounded-2xl border border-line bg-card p-3 text-center">
                <div className="font-serif text-3xl">{n}</div>
                <div className="text-[11px] text-muted">{l}</div>
              </div>
            ))}
          </div>

          <p className="mt-3 text-xs leading-relaxed text-muted">Question steps count the questions in saved expeditions, including repeats. A briefing is finished when all its stories are marked read.</p>

          {p.journeys.length === 0 ? (
            <div className="mt-10 rounded-3xl border border-dashed border-line p-6 text-center text-sm text-muted">
              Open a rabbit hole from any story and save the expedition. The ideas you discover will collect here.
              <div className="mt-3"><Link href="/briefing" className="text-accent underline">Go to your briefing</Link></div>
            </div>
          ) : (
            <>
              {p.concepts.length > 0 && (
                <section className="passport-panel mt-8" aria-labelledby="passport-concepts">
                  <h2 id="passport-concepts" className="font-serif text-2xl">Ideas you encountered</h2>
                  <p className="mt-2 text-sm leading-relaxed text-muted">Labels collected from your saved explorations. Each count shows how many expeditions included that idea.</p>
                  <ul className="passport-concepts mt-5">
                    {p.concepts.map((c) => (
                      <li key={c.name}>
                        <span>{c.name}</span>
                        <span className="passport-count">{c.count} {c.count === 1 ? "expedition" : "expeditions"}</span>
                      </li>
                    ))}
                  </ul>
                </section>
              )}
              {p.areas.length > 0 && (
                <section className="passport-panel mt-6" aria-labelledby="passport-fields">
                  <h2 id="passport-fields" className="font-serif text-2xl">Topics you returned to</h2>
                  <p className="mt-2 text-sm leading-relaxed text-muted">Counts are saved expeditions grouped by their starting story’s topics. One expedition can appear in several topics.</p>
                  <p className="mt-2 text-xs leading-relaxed text-muted">Bar lengths compare frequency with your most explored topic. They do not show completion or proficiency.</p>
                  <ul className="mt-5 space-y-4">
                    {p.areas.map((a) => (
                      <li key={a.name}>
                        <div className="passport-topic-label">
                          <span>{a.name}</span>
                          <span className="passport-count">{a.count} {a.count === 1 ? "expedition" : "expeditions"}</span>
                        </div>
                        <div aria-hidden="true" className="mt-2 h-1.5 overflow-hidden rounded-full bg-line">
                          <div className="h-full rounded-full bg-accent" style={{ width: `${(a.count / maxArea) * 100}%` }} />
                        </div>
                      </li>
                    ))}
                  </ul>
                </section>
              )}
              <section className="mt-8">
                <Eyebrow>Saved expeditions</Eyebrow>
                <ul className="mt-3 space-y-3">
                  {p.journeys.map((j) => (
                    <li key={j.id} className="rounded-2xl border border-line bg-card p-4">
                      <Link href={`/story/${j.story_id}`} className="font-serif text-lg leading-snug">{j.story_title}</Link>
                      <ol className="mt-2 space-y-1 border-l border-line pl-3 text-sm text-muted">
                        {j.path.map((s, i) => <li key={i}>{s.question}{s.prediction && <span className="mt-1 block text-xs text-accent">Your prediction: {s.prediction}</span>}</li>)}
                      </ol>
                      <div className="mt-2 text-[11px] text-muted">{fmtTime(j.created_at)}</div>
                    </li>
                  ))}
                </ul>
              </section>
            </>
          )}
        </>
      )}
    </Shell>
  );
}
