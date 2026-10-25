"use client";
import Link from "next/link";
import { useParams } from "next/navigation";
import { BriefingDeck } from "@/components/briefing-deck";
import { type Briefing } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { ErrorNote, Shell, Skeleton } from "@/components/ui";
export default function EditionView() {
  const {id} = useParams<{id:string}>();
  const {data:b,setData,error,loading,reload} = useApi<Briefing>(`/api/briefings/${id}`);
  return <Shell immersive>
    {loading && <Skeleton lines={6} />}
    {error && <><Link href="/briefing">← All briefings</Link><ErrorNote message={error} onRetry={reload} /></>}
    {b && <BriefingDeck key={b.id} briefing={b} onRead={storyId => setData({...b,read_ids:[...new Set([...b.read_ids,storyId])]})} />}
  </Shell>;
}
