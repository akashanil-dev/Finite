"use client";

import { useState } from "react";
import { api, type Meta, type Profile, type SourcesIndex } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { Exclusions, InterestPicker, LanguagePicker, ScheduleForm } from "@/components/profile-editor";
import { Button, ErrorNote, Shell, Spinner } from "@/components/ui";

const TABS = ["Interests", "Briefing", "Languages", "Exclusions"] as const;

export default function Settings() {
  const meta = useApi<Meta>("/api/meta");
  const prof = useApi<Profile>("/api/profile");
  const sources = useApi<SourcesIndex>("/api/sources");
  const [draft, setProfile] = useState<Profile | null>(null);
  const profile = draft ?? prof.data;
  const [tab, setTab] = useState<(typeof TABS)[number]>("Interests");
  const [saved, setSaved] = useState(false);

  if (meta.error) return <Shell><ErrorNote message={meta.error} /></Shell>;
  if (!meta.data || !profile) return <Shell><Spinner /></Shell>;

  const update = (p: Profile) => {
    setProfile(p);
    setSaved(false);
  };
  const save = async () => {
    setProfile(await api<Profile>("/api/profile", { method: "PUT", json: profile }));
    setSaved(true);
  };

  return (
    <Shell>
      <h1 className="font-serif text-3xl">Settings</h1>
      <div className="mt-4 flex gap-2 overflow-x-auto pb-1">
        {TABS.map((t) => (
          <button key={t} onClick={() => setTab(t)} className={`shrink-0 rounded-full px-4 py-1.5 text-sm ${tab === t ? "bg-ink text-paper" : "border border-line"}`}>
            {t}
          </button>
        ))}
      </div>
      <div className="mt-6">
        {tab === "Interests" && <InterestPicker meta={meta.data} profile={profile} onChange={update} />}
        {tab === "Briefing" && <ScheduleForm meta={meta.data} profile={profile} onChange={update} />}
        {tab === "Languages" && <LanguagePicker meta={meta.data} profile={profile} onChange={update} />}
        {tab === "Exclusions" && <Exclusions meta={meta.data} profile={profile} onChange={update} sources={sources.data} />}
      </div>
      <div className="sticky bottom-20 mt-8">
        <Button onClick={save} className="w-full">
          {saved ? "Saved. Applies to your next briefing" : "Save changes"}
        </Button>
      </div>
      <p className="mt-6 text-center text-xs text-muted">
        {meta.data.mock_mode ? "Running without an AI key: summaries and rabbit holes are extractive." : "AI mode is on."}
      </p>
    </Shell>
  );
}
