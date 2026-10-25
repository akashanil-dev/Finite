"use client";

import Link from "next/link";
import "./sources.css";
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
          <section className="sources-methodology" aria-labelledby="methodology-title">
            <div className="sources-heading">
              <div>
                <span className="sources-eyebrow">How we choose sources</span>
                <h2 id="methodology-title">A weight is a guide, not a guarantee.</h2>
              </div>
              <span className="sources-version">Methodology v0</span>
            </div>
            <p className="sources-intro">We make our editorial choices visible so you can decide what to read.</p>
            <dl className="sources-principles">
              <div><dt>Ranking, explained</dt><dd>Weights help order your feed. They are editorial judgments, not a fact-check score.</dd></div>
              <div><dt>Links need context</dt><dd>Aggregators help us discover stories. A shared link alone does not corroborate a claim.</dd></div>
              <div><dt>First-hand isn’t proof</dt><dd>A primary source tells you what an institution said. It does not automatically establish that it is true.</dd></div>
            </dl>
            <div className="sources-footer">
              <details>
                <summary>Read the full methodology</summary>
                <ul>{data.methodology.map(m => <li key={m}>{m}</li>)}</ul>
              </details>
              <Link href="/settings">Manage excluded sources <span aria-hidden="true">↗</span></Link>
            </div>
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
