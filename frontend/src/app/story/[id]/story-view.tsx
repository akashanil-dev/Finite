"use client";

import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api, fmtTime, type Analysis, type Depth, type Meta, type Profile, type StoryCard } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { CitationChips } from "@/components/citations";
import { ConnectionExplorer } from "@/components/connection-explorer";
import { TimeMachine } from "@/components/time-machine";
import { PerspectiveLens } from "@/components/perspective-lens";
import { RabbitHole, type HoleStart } from "@/components/rabbit-hole";
import { ErrorNote, Eyebrow, Shell, Skeleton, TierBadge, WeightBar } from "@/components/ui";

type StoryResp = { card: StoryCard; analysis: Analysis };

export default function StoryView() {
  const { id } = useParams<{ id: string }>();
  const bid = useSearchParams().get("b");
  const meta = useApi<Meta>("/api/meta");
  const profile = useApi<Profile>("/api/profile");
  const [langChoice, setLang] = useState<string | null>(null);
  const [depthChoice, setDepth] = useState<Depth | null>(null);
  const lang = langChoice ?? profile.data?.ui_language ?? null;
  const depth = depthChoice ?? profile.data?.depth ?? "standard";
  const story = useApi<StoryResp>(lang ? `/api/stories/${id}?lang=${lang}` : null);
  const [hole, setHole] = useState<HoleStart | null>(null);
  const [ask, setAsk] = useState("");

  useEffect(() => {
    if (bid) api(`/api/briefings/${bid}/read`, { method: "POST", json: { story_id: id } }).catch(() => {});
  }, [bid, id]);

  useEffect(() => {
    window.scrollTo({ top: 0 });
  }, [hole]);

  const s = story.data;
  const a = s?.analysis;
  const lookup = (r: string) => {
    const art = a?.articles.find((x) => x.ref === r);
    return art && { name: art.source, title: art.title, url: art.url, weight: art.weight, kind: "news" };
  };
  const mlAvailable = profile.data?.languages.includes("ml");

  if (hole && s)
    return (
      <Shell>
        <RabbitHole
          storyId={id}
          storyTitle={s.card.title}
          start={hole}
          lang={lang ?? "en"}
          maxDepth={meta.data?.max_depth ?? 2}
          briefingId={bid}
          onClose={() => setHole(null)}
        />
      </Shell>
    );

  return (
    <Shell>
      <div className="flex items-center justify-between">
        <Link href="/briefing" className="text-sm text-muted">← Briefing</Link>
        {mlAvailable && (
          <div className="flex rounded-full border border-line p-0.5 text-xs">
            {[["en", "English"], ["ml", "മലയാളം"]].map(([l, label]) => (
              <button key={l} onClick={() => setLang(l)} className={`rounded-full px-3 py-1 ${lang === l ? "bg-ink text-paper" : "text-muted"}`}>
                {label}
              </button>
            ))}
          </div>
        )}
      </div>

      {story.error && <div className="mt-6"><ErrorNote message={story.error} onRetry={story.reload} /></div>}
      {!s && !story.error && (
        <div className="mt-8 space-y-4">
          <p className="text-xs text-muted">Reading the coverage and preparing your briefing note…</p>
          <Skeleton lines={2} />
          <Skeleton lines={6} />
        </div>
      )}

      {s && a && (
        <article className="rise mt-6">
          <div className="flex flex-wrap gap-x-2 text-[11px] uppercase tracking-wide text-muted">
            {s.card.subfields.map((t) => <span key={t.id}>{t.name}</span>)}
          </div>
          <h1 className={`mt-2 font-serif text-[1.9rem] leading-[1.15] ${s.card.lang === "ml" ? "font-sans text-2xl" : ""}`}>{s.card.title}</h1>
          <div className="mt-3 flex flex-wrap gap-x-4 text-xs text-muted">
            <span>First published {fmtTime(s.card.published_at)}</span>
            {s.card.updated_at - s.card.published_at > 900 && <span className="text-accent">Updated {fmtTime(s.card.updated_at)}</span>}
          </div>

          <section className="mt-6 rounded-3xl border border-line bg-card p-5">
            <div className="flex items-center justify-between">
              <Eyebrow>What happened</Eyebrow>
              <div className="flex rounded-full bg-paper p-0.5 text-[11px]">
                {(["quick", "standard", "deep"] as Depth[]).map((d) => (
                  <button key={d} onClick={() => setDepth(d)} className={`rounded-full px-2.5 py-1 capitalize ${depth === d ? "bg-ink text-paper" : "text-muted"}`}>
                    {d}
                  </button>
                ))}
              </div>
            </div>
            <p className="mt-3 font-serif text-[1.15rem] leading-relaxed">{a.summary[depth]}</p>
            {a.what_happened.length > 0 && (
              <ul className="mt-4 space-y-2 border-t border-line pt-4 text-sm">
                {a.what_happened.map((f, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-accent" />
                    <span>
                      {f.text}
                      <CitationChips refs={f.citations} lookup={lookup} />
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="mt-4">
            <details className="rounded-3xl border border-line bg-card p-5">
              <summary className="flex cursor-pointer list-none items-center justify-between">
                <Eyebrow>Sources · {a.articles.length}</Eyebrow>
                <span className="text-xs text-muted">Show</span>
              </summary>
              <ul className="mt-3 space-y-3">
                {a.articles.map((x) => (
                  <li key={x.ref} className="text-sm">
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium">{x.source}</span>
                      <WeightBar weight={x.weight} />
                    </div>
                    <a href={x.url} target="_blank" rel="noreferrer" className="text-muted underline decoration-line underline-offset-2">{x.title}</a>
                    <div className="mt-1"><TierBadge tier={x.tier} /></div>
                  </li>
                ))}
              </ul>
            </details>
          </section>

          <PerspectiveLens key={id} storyId={id} />
          <ConnectionExplorer key={`connections-${id}`} storyId={id} />
          <TimeMachine key={`timeline-${id}`} storyId={id} />

          {a.missing_piece.length > 0 && (
            <section className="mt-4 rounded-3xl border border-warm/25 bg-warm-soft/60 p-5">
              <Eyebrow>The missing piece</Eyebrow>
              <p className="mt-1 text-sm text-muted">What the coverage didn&apos;t explain:</p>
              <ul className="mt-3 space-y-2.5">
                {a.missing_piece.map((m, i) => (
                  <li key={i}>
                    <button
                      onClick={() => setHole({ question: m.question, angle: "context", search: a.concepts.slice(0, 2) })}
                      className="text-left text-[15px] font-medium text-warm underline decoration-warm/30 underline-offset-4"
                    >
                      {m.question}
                    </button>
                    {m.why && <p className="text-xs text-muted">{m.why}</p>}
                  </li>
                ))}
              </ul>
            </section>
          )}

          <section className="mt-8">
            <h2 className="font-serif text-2xl">Where would you like to go from here?</h2>
            <div className="mt-4 grid gap-2.5">
              {a.questions.map((q) => (
                <button
                  key={q.id}
                  onClick={() => setHole({ question: q.question, angle: q.angle, search: q.search ?? [] })}
                  className="group flex items-center justify-between rounded-2xl border border-line bg-card p-4 text-left transition hover:border-accent/50"
                >
                  <span>
                    <span className="block font-medium">{q.question}</span>
                    <span className="text-xs text-muted">{q.blurb}</span>
                  </span>
                  <span className="text-accent transition group-hover:translate-x-0.5">→</span>
                </button>
              ))}
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (ask.trim()) setHole({ question: ask.trim(), angle: "context", search: [], custom: true });
              }}
              className="mt-4 rounded-2xl border border-dashed border-line p-3"
            >
              <label className="text-xs text-muted">Or ask your own question about this story</label>
              <div className="mt-2 flex gap-2">
                <input
                  value={ask}
                  onChange={(e) => setAsk(e.target.value)}
                  placeholder="e.g. Has this happened before?"
                  maxLength={300}
                  className="min-w-0 flex-1 rounded-full border border-line bg-card px-4 py-2 text-sm outline-none focus:border-accent"
                />
                <button type="submit" className="rounded-full bg-ink px-4 text-sm text-paper disabled:opacity-40" disabled={!ask.trim()}>
                  Ask
                </button>
              </div>
              <p className="mt-2 text-[11px] text-muted">Answered only from sources, with citations. If we can&apos;t find a sourced answer, we&apos;ll say so.</p>
            </form>
          </section>

          <p className="mt-8 text-center text-[11px] text-muted">
            {a.mode === "ai" ? "Summary written by AI from the linked sources." : "Extractive summary: sentences quoted from the linked sources."}
            {a.translation === "unavailable" && " Malayalam translation needs an AI key."}
          </p>
        </article>
      )}
    </Shell>
  );
}
