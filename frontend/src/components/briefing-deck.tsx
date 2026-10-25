"use client";

import Link from "next/link";
import "./briefing-stack.css";
import { useEffect, useRef, useState } from "react";
import { api, fmtTime, type Briefing } from "@/lib/api";
import { StoryReader } from "@/app/story/[id]/story-view";
import { CompletionFlower, ErrorNote } from "./ui";

export function BriefingDeck({ briefing, onChange }: { briefing: Briefing; onChange: (briefing: Briefing) => void }) {
  const deck = useRef<HTMLDivElement>(null);
  const [index, setIndex] = useState(0);
  const [visited, setVisited] = useState(() => new Set([0]));
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const count = briefing.stories.length;
  useEffect(() => {
    const root = deck.current;
    if (!root) return;
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting) {
        const next = Number((entry.target as HTMLElement).dataset.index);
        setIndex(next);
        setVisited(previous => previous.has(next) ? previous : new Set([...previous, next]));
      }
    }, { root, threshold: 0.6 });
    root.querySelectorAll('[data-index]').forEach(element => observer.observe(element));
    return () => observer.disconnect();
  }, [briefing.id]);
  function go(next: number) {
    const target = deck.current?.querySelector<HTMLElement>(`[data-index="${next}"]`);
    if (target) deck.current?.scrollTo({ top: target.offsetTop, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  }
  async function markRead(id: string | null, read: boolean) {
    if (busy) return;
    setBusy(true); setError(null);
    try { const updated = await api<Briefing>(`/api/briefings/${briefing.id}/${id === null ? 'read-state' : 'read'}`, { method: 'POST', json: id === null ? {read} : {story_id: id, read} }); onChange(updated); }
    catch (e) { setError(e instanceof Error ? e.message : 'Could not save your reading progress.'); }
    finally { setBusy(false); }
  }
  return <div className="briefing-deck-wrap">
    <div ref={deck} className="briefing-deck" tabIndex={0} aria-label="Your finite briefing; use up and down arrow keys" onKeyDown={event => {
      if (event.target !== event.currentTarget) return;
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault(); go(Math.min(count, Math.max(0, index + (event.key === 'ArrowDown' ? 1 : -1))));
      }
    }}>
      {briefing.stories.map((story, i) => <div className="deck-story-slot" key={story.id} data-index={i} data-stack={Math.min(2, count - i - 1)}><section className="deck-story" aria-label={`Story ${i + 1} of ${count}`}>
        <div className="deck-story-top" style={{flexWrap: "wrap", flexShrink: 0}}><Link href="/briefing" aria-label="All saved briefings">← Briefings</Link><span>{fmtTime(briefing.created_at)} · {i + 1}/{count}</span><Link href={`/story/${story.id}?b=${briefing.id}`} aria-label="Open full story">↗</Link>
        <div style={{width: "100%"}} className="briefing-read-actions" aria-label="Whole briefing reading status"><span>{briefing.read_ids.length}/{count} read</span><button disabled={busy} onClick={() => markRead(null, !briefing.completed_at)}>{busy ? 'Saving…' : briefing.completed_at ? 'Mark briefing unread' : 'Mark briefing read'}</button></div>
        </div>
        {visited.has(i) ? <StoryReader key={story.id} id={story.id} embedded /> : <div className="deck-preview"><h2>{story.title}</h2><p>{story.teaser}</p></div>}
        <div className="deck-story-bottom"><div className="deck-step-buttons"><button disabled={i === 0} onClick={() => go(i - 1)} aria-label="Previous story">↑</button><button onClick={() => go(i + 1)} aria-label={i < count - 1 ? "Next story" : "Finish briefing"}>↓</button><span>{i < count - 1 ? "Swipe for next" : "Last story · swipe to finish"}</span></div><button disabled={busy} onClick={() => markRead(story.id, !briefing.read_ids.includes(story.id))}>{busy ? 'Saving…' : briefing.read_ids.includes(story.id) ? 'Mark unread' : 'Mark as read'}</button></div>
        {error && index === i && <ErrorNote message={error} />}
      </section></div>)}
      <section className="deck-ending" data-index={count}>
        <Link href="/briefing">← All saved briefings</Link><CompletionFlower /><h2>The end. Take a breath.</h2>
        <p>{count - briefing.read_ids.length > 0 ? `${count - briefing.read_ids.length} unread. You can return to them whenever you like.` : 'You’re done for today.'} Nothing more will load.</p>
        <Link href="/passport">Visit your Knowledge Passport →</Link>
        <button onClick={() => go(0)}>Back to the first story ↑</button>
      </section>
    </div>
  </div>;
}
