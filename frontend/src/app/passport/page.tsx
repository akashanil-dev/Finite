"use client";

import Link from "next/link";
import { fmtTime, type Passport } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { ErrorNote, Eyebrow, Shell, Skeleton } from "@/components/ui";

export default function PassportPage() {
  const { data: p, error } = useApi<Passport>("/api/passport");
  const max = Math.max(1, ...(p?.concepts.map((c) => c.count) ?? [1]));
  return (
    <Shell>
      <Eyebrow>Knowledge passport</Eyebrow>
      <h1 className="mt-2 font-serif text-3xl leading-tight">What you&apos;ve come to understand</h1>
      <p className="mt-2 text-sm text-muted">No streaks, no pressure. Just a map of what you&apos;ve explored.</p>

      {error && <div className="mt-6"><ErrorNote message={error} /></div>}
      {!p && !error && <div className="mt-8"><Skeleton lines={5} /></div>}

      {p && (
        <>
          <div className="mt-6 grid grid-cols-3 gap-2">
            {[
              [p.journeys.length, "expeditions"],
              [p.questions_explored, "questions"],
              [p.briefings_completed, "briefings finished"],
            ].map(([n, l]) => (
              <div key={l} className="rounded-2xl border border-line bg-card p-3 text-center">
                <div className="font-serif text-3xl">{n}</div>
                <div className="text-[11px] text-muted">{l}</div>
              </div>
            ))}
          </div>

          {p.concepts.length === 0 ? (
            <div className="mt-10 rounded-3xl border border-dashed border-line p-6 text-center text-sm text-muted">
              Open a rabbit hole from any story and save the expedition. The ideas you discover will collect here.
              <div className="mt-3"><Link href="/briefing" className="text-accent underline">Go to your briefing</Link></div>
            </div>
          ) : (
            <>
              <section className="mt-8">
                <Eyebrow>Knowledge areas unlocked</Eyebrow>
                <div className="mt-3 flex flex-wrap gap-2">
                  {p.concepts.map((c) => (
                    <span
                      key={c.name}
                      className="rounded-full border border-accent/30 bg-accent-soft px-3 py-1 text-accent"
                      style={{ fontSize: `${12 + (c.count / max) * 6}px` }}
                    >
                      {c.name}
                    </span>
                  ))}
                </div>
              </section>
              {p.areas.length > 0 && (
                <section className="mt-8">
                  <Eyebrow>Fields explored</Eyebrow>
                  <ul className="mt-3 space-y-2">
                    {p.areas.map((a) => (
                      <li key={a.name} className="flex items-center gap-3 text-sm">
                        <span className="w-40 shrink-0">{a.name}</span>
                        <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-line">
                          <span className="block h-full rounded-full bg-accent" style={{ width: `${(a.count / p.areas[0].count) * 100}%` }} />
                        </span>
                        <span className="w-4 text-right text-xs text-muted">{a.count}</span>
                      </li>
                    ))}
                  </ul>
                </section>
              )}
              <section className="mt-8">
                <Eyebrow>Expeditions</Eyebrow>
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
