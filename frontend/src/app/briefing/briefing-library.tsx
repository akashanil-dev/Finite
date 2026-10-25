"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useRef, useState } from "react";
import { api, fmtTime, type Briefing } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { Button, ErrorNote, Shell, Skeleton } from "@/components/ui";

type Edition = { completed_at: number | null; number: number; opened_at: number | null; id: number; created_at: number; story_count: number; requested_count?: number; read_count: number; headline: string; can_refresh: boolean; edition_of: number | null };
type History = { items: Edition[]; next_cursor: number | null };

export default function BriefingPage() {
  const history = useApi<History>("/api/briefings");
  const router = useRouter();
  const lock = useRef(false);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [older, setOlder] = useState<History | null>(null);
  const [used, setUsed] = useState<number[]>([]);
  const editions = [...new Map([...(history.data?.items ?? []), ...(older?.items ?? [])].map(b => [b.id,b])).values()];
  const cursor = older ? older.next_cursor : history.data?.next_cursor;
  async function prepare(id?: number) {
    if (lock.current) return;
    lock.current = true; setBusy(true); setErr(null);
    if (id !== undefined) setUsed(previous => [...previous,id]);
    try {
      const b = await api<Briefing>(id === undefined ? '/api/briefings' : `/api/briefings/${id}/edition`, {method:'POST'});
      history.reload(); router.push(`/briefing/${b.id}`);
    } catch (e) { setErr(e instanceof Error ? e.message : 'Could not prepare an edition.'); history.reload(); }
    finally { lock.current = false; setBusy(false); }
  }
  async function more() {
    if (!cursor || lock.current) return;
    lock.current = true; setBusy(true); setErr(null);
    try {
      const page = await api<History>(`/api/briefings?before=${cursor}`);
      setOlder(previous => ({items:[...(previous?.items ?? []),...page.items],next_cursor:page.next_cursor}));
    } catch (e) { setErr(e instanceof Error ? e.message : 'Could not load older briefs.'); }
    finally { lock.current = false; setBusy(false); }
  }
  return <Shell>
    <header className="briefing-library-heading"><h1>Your briefings</h1><p>Each card is a saved edition. Open one to read its stories. Earlier editions stay here.</p></header>
    {history.loading && <Skeleton lines={5} />}
    {history.error && <ErrorNote message={history.error} onRetry={history.reload} />}
    {err && <ErrorNote message={err} />}
    <div className="briefing-library">
      {editions.map(b => <article className="edition-card" data-opened={Boolean(b.opened_at || b.read_count)} key={b.id}>
        <div className="edition-surface">
        <Link href={`/briefing/${b.id}`} className="edition-open" prefetch={false}>
          <div className="edition-identity"><span>Brief #{b.number}</span><span>{b.completed_at ? "Finished" : b.opened_at || b.read_count ? "Opened" : "Unopened"}</span></div>
          <span className="edition-date">{fmtTime(b.created_at)} · {b.edition_of ? 'Extra edition' : 'Briefing'}</span>
          <h2>{b.headline}</h2>
          <p>{b.story_count} stories · {b.read_count} read <span aria-hidden="true">↗</span></p>
          {b.requested_count !== undefined && b.story_count < b.requested_count && <p className="mt-2 text-muted">Saved with {b.story_count} of {b.requested_count} requested stories.</p>}
          <p className="mt-3 underline">{b.completed_at ? "Read again →" : b.opened_at || b.read_count ? "Continue reading →" : "Open briefing →"}</p>
        </Link>
        {b.can_refresh && !used.includes(b.id) && <div className="edition-refresh"><span>One extra edition available</span><button onClick={() => prepare(b.id)} disabled={busy}>New edition</button></div>}
        </div>
      </article>)}
    </div>
    {!history.loading && !history.error && editions.length === 0 && <div className="mt-10 space-y-4"><p>No saved briefs yet. Prepare your first edition to begin.</p><Button disabled={busy} onClick={() => prepare()}>{busy ? 'Preparing…' : 'Prepare my first briefing'}</Button></div>}
    {cursor && <Button className="mt-6" disabled={busy} onClick={more}>{busy ? 'Loading…' : 'Older briefings'}</Button>}
    {busy && <p role="status" className="mt-4 text-sm text-muted">Working on your request…</p>}
  </Shell>;
}
