"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { BriefingDeck } from "@/components/briefing-deck";
import { api, type Briefing } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { ErrorNote, Shell, Skeleton } from "@/components/ui";
export default function EditionView() {
  const {id} = useParams<{id:string}>();
  const {data:b,setData,error,loading,reload} = useApi<Briefing>(`/api/briefings/${id}`);
  const [openError, setOpenError] = useState<string | null>(null);
  const loadedId = b?.id;
  useEffect(() => {
    if (!loadedId) return;
    let active = true;
    api(`/api/briefings/${loadedId}/opened`, {method: "POST"}).catch(() => {
      if (active) setOpenError("Couldn't save your opened status. Your reading progress is still available.");
    });
    return () => { active = false; };
  }, [loadedId]);
  return <Shell immersive>
    {openError && <p role="status" className="text-sm text-muted">{openError}</p>}
    {loading && <Skeleton lines={6} />}
    {error && <><Link href="/briefing">← All briefings</Link><ErrorNote message={error} onRetry={reload} /></>}
    {b && <BriefingDeck key={b.id} briefing={b} onChange={setData} />}
  </Shell>;
}
