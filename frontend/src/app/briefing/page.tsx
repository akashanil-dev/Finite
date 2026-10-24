"use client";

import Link from "next/link";
import { useState, useSyncExternalStore } from "react";
import { api, fmtTime, timeAgo, type Briefing } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { Button, CompletionFlower, ErrorNote, Eyebrow, Shell, Skeleton, TierBadge, Wordmark } from "@/components/ui";

const noop = () => () => {};

function useClientValue(get: () => string) {
  return useSyncExternalStore(noop, get, () => "");
}

function greeting() {
  const h = new Date().getHours();
  return h < 12 ? "Good morning" : h < 17 ? "Good afternoon" : "Good evening";
}

function today() {
  return new Date().toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long" });
}

export default function BriefingPage() {
  const { data: b, setData, error, loading } = useApi<Briefing | null>("/api/briefings/latest");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const date = useClientValue(today);
  const hello = useClientValue(greeting);

  const prepare = async () => {
    setBusy(true);
    setErr(null);
    try {
      setData(await api<Briefing>("/api/briefings", { method: "POST" }));
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Could not prepare a briefing");
    } finally {
      setBusy(false);
    }
  };

  const read = new Set(b?.read_ids ?? []);
  const total = b?.stories.length ?? 0;
  const done = b ? b.stories.filter((s) => read.has(s.id)).length : 0;

  return (
    <Shell>
      <header className="flex items-center justify-between">
        <Wordmark small />
        <span className="text-xs text-muted">{date}</span>
      </header>

      {loading && <div className="mt-10"><Skeleton lines={6} /></div>}
      {error && <div className="mt-8"><ErrorNote message={error} /></div>}

      {!loading && !b && (
        <div className="mt-16 space-y-4 text-center">
          <h1 className="font-serif text-3xl">No briefing yet</h1>
          <p className="text-sm text-muted">A finite collection of stories, chosen around your interests. Prepare your first edition when you’re ready.</p>
          <Button onClick={prepare} disabled={busy}>{busy ? "Preparing…" : "Prepare my briefing now"}</Button>
          {err && <ErrorNote message={err} />}
        </div>
      )}

      {b && (
        <>
          <section className="briefing-hero rise mt-8">
            <Eyebrow>{hello || "Your briefing"}</Eyebrow>
            <h1 className="mt-2 font-serif text-[2.1rem] leading-tight">
              A little news.<span className="italic">A bigger picture.</span>
            </h1>
            <p className="hero-caption mt-4 text-sm text-muted">
              {total} stories · Past {b.config.lookback_hours} hours · prepared {fmtTime(b.created_at)} · {b.config.depth} depth. This list is frozen and will not grow.
            </p>
            <div className="mt-5 flex items-center gap-3">
              <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-line">
                <div className="h-full rounded-full bg-accent transition-all" style={{ width: `${total ? (done / total) * 100 : 0}%` }} />
              </div>
              <span className="text-xs tabular-nums text-muted">
                {done} of {total}
              </span>
            </div>
          </section>

          <ol className="story-list mt-8">
            {b.stories.map((s, i) => {
              const isRead = read.has(s.id);
              return (
                <li key={s.id} className="rise" style={{ animationDelay: `${Math.min(i, 5) * 65}ms` }}>
                  <Link
                    href={`/story/${s.id}?b=${b.id}`}
                    className="story-card" data-read={isRead}
                  >
                    <div className="flex items-start gap-4">
                      <span className="story-number">{String(i + 1).padStart(2, "0")}</span>
                      <div className="min-w-0 flex-1">
                        <div className="mb-1.5 flex flex-wrap items-center gap-x-2 gap-y-1 text-[11px] text-muted">
                          {s.subfields.slice(0, 2).map((t) => (
                            <span key={t.id} className="uppercase tracking-wide">{t.name}</span>
                          ))}
                          <span>· {timeAgo(s.published_at)}</span>
                          {s.updated_at - s.published_at > 900 && <span className="text-accent">· updated {timeAgo(s.updated_at)}</span>}
                        </div>
                        <h2 className={`font-serif text-[1.2rem] leading-snug ${s.lang === "ml" ? "font-sans text-base" : ""}`}>{s.title}</h2>
                        {s.teaser && <p className="mt-1.5 line-clamp-2 text-sm text-muted">{s.teaser}</p>}
                        <div className="mt-3 flex flex-wrap items-center gap-1.5">
                          <TierBadge tier={s.sources[0]?.tier ?? "established"} label={s.sources[0]?.name} />
                          {s.sources.length > 1 && <span className="text-[11px] text-muted">+{s.sources.length - 1} more source{s.sources.length > 2 ? "s" : ""}</span>}
                          <span className="ml-auto text-xs text-accent">{isRead ? "Read ✓" : <span className="card-arrow">Read story ↗</span>}</span>
                        </div>
                      </div>
                    </div>
                  </Link>
                </li>
              );
            })}
          </ol>

          <section className={`completion mt-10 rounded-3xl p-6 text-center ${b.completed_at ? "bg-ink text-paper" : "border border-dashed border-line"}`}>
            {b.completed_at ? (
              <>
                <CompletionFlower />
                <div className="font-serif text-3xl">You&apos;re done for today.</div>
                <p className="mt-2 text-sm text-paper/70">
                  That&apos;s everything that mattered to you in the past {b.config.lookback_hours} hours. No more recommendations. Your saved briefing time is {b.config.delivery_time}. Automatic preparation depends on scheduled delivery being enabled.
                </p>
                <Link href="/passport" className="mt-4 inline-block text-sm underline">See what you learned →</Link>
              </>
            ) : (
              <>
                <div className="font-serif text-xl">The end of your briefing</div>
                <p className="mt-1 text-sm text-muted">{total - done} stories left. Then you&apos;re done. Nothing more will load.</p>
              </>
            )}
          </section>

          <div className="mt-6 text-center">
            <button onClick={prepare} disabled={busy} className="text-xs text-muted underline disabled:opacity-50">
              {busy ? "Preparing a fresh briefing…" : "Prepare a fresh briefing now (demo)"}
            </button>
            {err && <div className="mt-3"><ErrorNote message={err} /></div>}
          </div>
        </>
      )}
    </Shell>
  );
}
