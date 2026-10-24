"use client";

import { type SourcesIndex } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { ErrorNote, Eyebrow, Shell, Skeleton, TierBadge, WeightBar } from "@/components/ui";

export default function SourcesPage() {
  const { data, error } = useApi<SourcesIndex>("/api/sources");
  return (
    <Shell>
      <Eyebrow>Transparency</Eyebrow>
      <h1 className="mt-2 font-serif text-3xl">Our sources</h1>
      <p className="mt-2 text-sm text-muted">Every outlet Finite reads, how much we trust it, and why.</p>
      {error && <div className="mt-6"><ErrorNote message={error} /></div>}
      {!data && !error && <div className="mt-8"><Skeleton lines={6} /></div>}
      {data && (
        <>
          <section className="mt-6 rounded-3xl bg-ink p-5 text-sm text-paper">
            <div className="text-[11px] uppercase tracking-[0.14em] text-paper/60">Methodology v0</div>
            <ul className="mt-3 space-y-2 text-paper/85">
              {data.methodology.map((m) => <li key={m}>— {m}</li>)}
            </ul>
          </section>
          {Object.entries(data.tiers).map(([tid, t]) => {
            const list = data.sources.filter((s) => s.tier === tid);
            const ctx = data.context_sources.filter((s) => s.tier === tid);
            if (!list.length && !ctx.length) return null;
            return (
              <section key={tid} className="mt-8">
                <div className="flex items-center gap-2">
                  <TierBadge tier={tid} label={t.label} />
                </div>
                <p className="mt-1 text-xs text-muted">{t.description}</p>
                <ul className="mt-3 divide-y divide-line rounded-3xl border border-line bg-card">
                  {[...list, ...ctx].sort((a, b) => b.weight - a.weight).map((s) => (
                    <li key={s.id} className="p-4">
                      <div className="flex items-center justify-between gap-3">
                        <a href={s.homepage} target="_blank" rel="noreferrer" className="font-medium">
                          {s.name}
                          {"lang" in s && s.lang === "ml" && <span className="ml-2 text-xs text-warm">മലയാളം</span>}
                        </a>
                        <WeightBar weight={s.weight} />
                      </div>
                      <p className="mt-1 text-xs text-muted">{s.rationale}</p>
                    </li>
                  ))}
                </ul>
              </section>
            );
          })}
        </>
      )}
    </Shell>
  );
}
