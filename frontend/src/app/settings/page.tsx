"use client";

import { useState } from "react";
import { api, type Meta, type Profile, type SourcesIndex } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { Exclusions, InterestPicker, LanguagePicker, ScheduleForm } from "@/components/profile-editor";
import { Button, ErrorNote, Shell, Spinner } from "@/components/ui";

const TABS = ["Interests", "Briefing", "Languages", "Exclusions"] as const;

export default function Settings() {
  const account = useApi<{ username: string }>("/api/auth/me");
  const [accountError, setAccountError] = useState<string | null>(null);
  const [signingOut, setSigningOut] = useState(false);
  const meta = useApi<Meta>("/api/meta");
  const prof = useApi<Profile>("/api/profile");
  const sources = useApi<SourcesIndex>("/api/sources");
  const [draft, setProfile] = useState<Profile | null>(null);
  const profile = draft ?? prof.data;
  const [tab, setTab] = useState<(typeof TABS)[number]>("Interests");
  const [saved, setSaved] = useState(false);

  if (prof.error) return <Shell><ErrorNote message={prof.error} onRetry={prof.reload} /></Shell>;
  if (meta.error) return <Shell><ErrorNote message={meta.error} /></Shell>;
  if (!meta.data || !profile) return <Shell><Spinner /></Shell>;

  const update = (p: Profile) => {
    setProfile(p);
    setSaved(false);
  };
  const save = async () => {
    try {
      setProfile(await api<Profile>("/api/profile", { method: "PUT", json: profile }));
      setSaved(true);
      setAccountError(null);
    } catch (e) { setAccountError(e instanceof Error ? e.message : "Could not save changes"); }
  };

  return (
    <Shell>
      <h1 className="font-serif text-3xl">Settings</h1>
      <div className="mt-4 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-line p-4">
        <p className="text-sm">Signed in as <strong>{account.data?.username ?? "…"}</strong></p>
        <Button variant="ghost" disabled={signingOut} onClick={async () => {
          setSigningOut(true);
          try {
            await api("/api/auth/logout", { method: "POST" });
            // Clear all account-specific React state on sign-out.
            // eslint-disable-next-line @next/next/no-location-assign-relative-destination
            window.location.assign("/login");
          }
          catch (e) { setAccountError(e instanceof Error ? e.message : "Could not sign out"); setSigningOut(false); }
        }}>{signingOut ? "Signing out…" : "Sign out"}</Button>
      </div>
      {accountError && <ErrorNote message={accountError} /> }
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
