"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { api, type Exploration, type NextQuestion } from "@/lib/api";
import { CuriosityChallenge } from "./curiosity-challenge";
import { CitationChips, ConfidenceBadge } from "./citations";
import { Button, ErrorNote, Eyebrow, Skeleton } from "./ui";

export type HoleStart = { question: string; angle: string; search: string[]; custom?: boolean };

type Props = {
  storyId: string;
  storyTitle: string;
  start: HoleStart;
  lang: string;
  maxDepth: number;
  briefingId: string | null;
  onClose: () => void;
};

export function RabbitHole({ storyId, storyTitle, start, lang, maxDepth, briefingId, onClose }: Props) {
  const [steps, setSteps] = useState<Exploration[]>([]);
  const [pending, setPending] = useState<HoleStart | null>(start);
  const [error, setError] = useState<string | null>(null);
  const [ended, setEnded] = useState(false);
  const [saved, setSaved] = useState(false);
  const [challenge, setChallenge] = useState<NextQuestion | null>(null);
  const [prediction, setPrediction] = useState<string | undefined>();

  const load = useCallback(
    (q: HoleStart, prev: Exploration[], isAlive: () => boolean = () => true) =>
      api<Exploration>(`/api/stories/${storyId}/explore`, {
        method: "POST",
        json: { ...q, depth: prev.length + 1, path: prev.map((s) => ({ question: s.question, key: s.key })), lang },
      })
        .then((out) => {
          if (!isAlive()) return;
          setSteps([...prev, out]);
          setPending(null);
          if (out.off_topic || out.depth >= maxDepth) setEnded(!out.off_topic);
        })
        .catch((e) => isAlive() && setError(e instanceof Error ? e.message : "Could not explore this question")),
    [storyId, lang, maxDepth],
  );

  useEffect(() => {
    let alive = true;
    load(start, [], () => alive);
    return () => {
      alive = false;
    };
  }, [load, start]);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [steps.length, ended]);

  const current = steps[steps.length - 1];
  const concepts = [...new Set(steps.flatMap((s) => s.concepts ?? []))];

  const goDeeper = (q: NextQuestion, guess?: string) => {
    setChallenge(null);
    setPrediction(guess);
    const next = { question: q.question, angle: q.angle, search: q.search ?? [] };
    setError(null);
    setPending(next);
    load(next, steps);
  };

  const save = async () => {
    await api("/api/journeys", {
      method: "POST",
      json: { story_id: storyId, path: steps.map((s) => ({ question: s.question, key: s.key, ...(s.depth === 2 && prediction ? { prediction } : {}) })), concepts },
    });
    setSaved(true);
  };

  const levels = Array.from({ length: maxDepth }, (_, i) => steps[i]?.question ?? (i === steps.length && pending ? pending.question : null));

  return (
    <div className="rise">
      <div className="flex items-center justify-between">
        <button onClick={onClose} className="text-sm text-muted">
          ← Back to story
        </button>
        <span className="text-xs text-muted">
          Level {Math.min(steps.length + (pending ? 1 : 0), maxDepth)} of {maxDepth}
        </span>
      </div>

      <JourneyMap storyTitle={storyTitle} levels={levels} ended={ended} />

      {error && <ErrorNote message={error} onRetry={() => {
            setError(null);
            if (pending) load(pending, steps);
          }} />}

      {pending && !error && (
        <div className="mt-6 rounded-3xl border border-line bg-card p-5">
          <Eyebrow>Digging into</Eyebrow>
          <h2 className="mt-1 font-serif text-xl">{pending.question}</h2>
          <p className="mt-2 text-xs text-muted">Gathering sources, writing with citations, then checking every claim…</p>
          <Skeleton lines={5} />
        </div>
      )}

      {current && !pending && current.off_topic && (
        <div className="mt-6 space-y-3 rounded-3xl border border-line bg-card p-5 text-sm">
          <p>That question seems unrelated to this story, so we didn&apos;t search for it. Finite keeps rabbit holes tied to the news you&apos;re reading.</p>
          <Button variant="ghost" onClick={onClose}>Back to story</Button>
        </div>
      )}

      {current && !pending && !current.off_topic && current.depth === 2 && prediction && (
        <aside className="mt-6 rounded-2xl border border-accent/30 bg-accent-soft p-4 text-sm" aria-label="Your prediction">
          <p className="font-medium">Your prediction: {prediction}</p>
          <p className="mt-1 text-muted">Compare your idea with the cited exploration below. Did the sources support it, suggest another connection, or leave it unresolved?</p>
        </aside>
      )}
      {current && !pending && !current.off_topic && <StepView step={current} />}

      {challenge && !pending && !ended && <CuriosityChallenge key={challenge.question} question={challenge.question} onReveal={(guess) => goDeeper(challenge, guess)} onCancel={() => setChallenge(null)} />}

      {current && !pending && !current.off_topic && !ended && !challenge && (
        <section className="mt-8">
          <Eyebrow>Level {current.depth + 1}: connections</Eyebrow>
          <h3 className="mt-1 font-serif text-xl">Go one level deeper?</h3>
          <div className="mt-4 space-y-2">
            {(current.next_questions ?? []).map((q) => (
              <button key={q.question} onClick={() => setChallenge(q)} className="flex w-full items-center justify-between rounded-2xl border border-line bg-card p-4 text-left transition hover:border-accent/50">
                <span className="text-sm font-medium">{q.question}</span>
                <span className="text-accent">→</span>
              </button>
            ))}
          </div>
          <button onClick={() => setEnded(true)} className="mt-4 w-full rounded-2xl border border-dashed border-line p-4 text-sm text-muted">
            End the expedition here
          </button>
        </section>
      )}

      {ended && (
        <section className="rise mt-8 rounded-3xl bg-ink p-6 text-paper">
          <div className="text-[11px] uppercase tracking-[0.14em] text-paper/60">Expedition complete</div>
          <h3 className="mt-2 font-serif text-2xl leading-snug">You went {steps.length} level{steps.length > 1 ? "s" : ""} beneath the headline.</h3>
          {concepts.length > 0 && (
            <>
              <p className="mt-4 text-sm text-paper/70">Knowledge areas unlocked</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {concepts.map((c) => (
                  <span key={c} className="rounded-full border border-paper/25 px-3 py-1 text-xs">{c}</span>
                ))}
              </div>
            </>
          )}
          <div className="mt-6 flex flex-col gap-2">
            <button onClick={save} disabled={saved} className="rounded-full bg-paper px-5 py-3 text-sm font-medium text-ink disabled:opacity-70">
              {saved ? "Saved to your Knowledge Passport ✓" : "Save to my Knowledge Passport"}
            </button>
            <Link href={briefingId ? "/briefing" : "/briefing"} className="rounded-full border border-paper/30 px-5 py-3 text-center text-sm">
              Return to the briefing
            </Link>
          </div>
        </section>
      )}
    </div>
  );
}

function JourneyMap({ storyTitle, levels, ended }: { storyTitle: string; levels: (string | null)[]; ended: boolean }) {
  const items = [{ label: "The event", text: storyTitle, state: "done" as const }, ...levels.map((q, i) => ({ label: `Level ${i + 1}`, text: q ?? (i === 0 ? "Context" : "Connections"), state: q ? ("done" as const) : ("todo" as const) }))];
  return (
    <ol className="relative mt-5 space-y-3 border-l border-line pl-5">
      {items.map((it, i) => (
        <li key={i} className="relative">
          <span className={`absolute -left-[26px] top-1 h-3 w-3 rounded-full border-2 ${it.state === "done" ? "border-accent bg-accent" : "border-line bg-paper"}`} />
          <div className="text-[10px] uppercase tracking-[0.14em] text-muted">{it.label}</div>
          <div className={`line-clamp-1 text-sm ${it.state === "done" ? "" : "text-muted"}`}>{it.text}</div>
        </li>
      ))}
      <li className="relative">
        <span className={`absolute -left-[26px] top-1 h-3 w-3 rotate-45 border-2 ${ended ? "border-warm bg-warm" : "border-line bg-paper"}`} />
        <div className="text-[10px] uppercase tracking-[0.14em] text-muted">Endpoint</div>
        <div className={`text-sm ${ended ? "text-warm" : "text-muted"}`}>Expedition complete</div>
      </li>
    </ol>
  );
}

function StepView({ step }: { step: Exploration }) {
  const lookup = (r: string) => step.sources?.[r];
  return (
    <section className="mt-6">
      <Eyebrow>Level {step.depth}</Eyebrow>
      <h2 className="mt-1 font-serif text-[1.7rem] leading-tight">{step.question}</h2>
      {step.insufficient && (
        <p className="mt-3 rounded-2xl bg-warm-soft p-3 text-xs text-warm">
          We couldn&apos;t find enough reliable sources to fully answer this. Here is what the sources do support.
        </p>
      )}
      <div className="mt-5 space-y-3">
        {step.nodes.map((n, i) => (
          <article key={i} className="rise rounded-3xl border border-line bg-card p-5" style={{ animationDelay: `${i * 60}ms` }}>
            <div className="mb-2 flex items-start justify-between gap-3">
              <h3 className="font-medium leading-snug">{n.heading}</h3>
              <ConfidenceBadge level={n.confidence} />
            </div>
            <p className="text-[15px] leading-relaxed text-ink/90">
              {n.text}
              <CitationChips refs={n.citations} lookup={lookup} />
            </p>
          </article>
        ))}
      </div>
      {step.timeline && step.timeline.length > 0 && (
        <div className="mt-6">
          <Eyebrow>Time machine</Eyebrow>
          <ol className="mt-3 space-y-4 border-l-2 border-accent/30 pl-5">
            {step.timeline.map((t, i) => (
              <li key={i} className="relative">
                <span className="absolute -left-[27px] top-1.5 h-2.5 w-2.5 rounded-full bg-accent" />
                <div className="font-serif text-lg text-accent">{t.date}</div>
                <p className="text-sm">
                  {t.event}
                  <CitationChips refs={t.citations} lookup={lookup} />
                </p>
              </li>
            ))}
          </ol>
        </div>
      )}
      <p className="mt-4 text-[11px] text-muted">
        {step.mode === "ai" ? "Written only from the cited sources, then fact-checked claim by claim." : "Extractive mode: passages quoted directly from the cited sources."}
        {!!step.dropped_claims && ` ${step.dropped_claims} unsupported claim${step.dropped_claims > 1 ? "s were" : " was"} removed.`}
        {step.translation === "unavailable" && " Translation unavailable without an AI key."}
      </p>
    </section>
  );
}
