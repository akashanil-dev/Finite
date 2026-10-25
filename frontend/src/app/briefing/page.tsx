"use client";

import { useState } from "react";
import { BriefingDeck } from "@/components/briefing-deck";
import { api, fmtTime, type Briefing } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { Button, ErrorNote, Shell, Skeleton, Wordmark } from "@/components/ui";

export default function BriefingPage() {
  const { data: b, setData, error, loading } = useApi<Briefing | null>("/api/briefings/latest");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  async function prepare() {
    setBusy(true); setErr(null);
    try { setData(await api<Briefing>("/api/briefings", { method: "POST" })); }
    catch (e) { setErr(e instanceof Error ? e.message : "Could not prepare a briefing"); }
    finally { setBusy(false); }
  }
  return <Shell immersive={!!b}>
    <header className="briefing-overview">
      <Wordmark small />
      {b && <div><h1>Your daily briefing</h1><p>{b.stories.length} stories · {fmtTime(b.created_at)} · A finite edition</p></div>}
      {b && <button onClick={prepare} disabled={busy}>{busy ? 'Preparing…' : 'New edition'}</button>}
    </header>
    {loading && <div className="mt-10"><Skeleton lines={6} /></div>}
    {error && <ErrorNote message={error} />}
    {err && <ErrorNote message={err} />}
    {!loading && !b && !error && <div className="mt-16 space-y-4 text-center"><h1 className="font-serif text-3xl">No briefing yet</h1><p className="text-sm text-muted">A finite collection of stories, chosen around your interests.</p><Button onClick={prepare} disabled={busy}>{busy ? 'Preparing…' : 'Prepare my briefing now'}</Button></div>}
    {b && <BriefingDeck key={b.id} briefing={b} onRead={id => setData({...b, read_ids:[...new Set([...b.read_ids,id])]})} />}
  </Shell>;
}
