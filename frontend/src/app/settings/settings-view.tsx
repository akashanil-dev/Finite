"use client";

import { useState } from "react";
import { api, type Meta, type Profile, type SourcesIndex } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { Exclusions, InterestPicker, LanguagePicker, ScheduleForm } from "@/components/profile-editor";
import { Button, ErrorNote, Segmented, Shell, Spinner } from "@/components/ui";

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
  const [saving, setSaving] = useState(false);

  if (prof.error) return <Shell><ErrorNote message={prof.error} onRetry={prof.reload} /></Shell>;
  if (meta.error) return <Shell><ErrorNote message={meta.error} /></Shell>;
  if (!meta.data || !profile) return <Shell><Spinner /></Shell>;

  const update = (p: Profile) => {
    setProfile(p);
    setSaved(false);
  };
  const save = async () => {
    if (saving) return;
    setSaving(true);
    try {
      setProfile(await api<Profile>("/api/profile", { method: "PUT", json: profile }));
      setSaved(true);
      setAccountError(null);
    } catch (e) { setAccountError(e instanceof Error ? e.message : "Could not save changes"); }
    finally { setSaving(false); }
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
      <div className="mt-6"><Segmented value={tab} options={TABS} onChange={setTab} label="Settings section" /></div>
      <div key={tab} className="rise mt-6">
        {tab === "Interests" && <InterestPicker meta={meta.data} profile={profile} onChange={update} />}
        {tab === "Briefing" && <ScheduleForm meta={meta.data} profile={profile} onChange={update} />}
        {tab === "Languages" && <LanguagePicker meta={meta.data} profile={profile} onChange={update} />}
        {tab === "Exclusions" && <Exclusions meta={meta.data} profile={profile} onChange={update} sources={sources.data} />}
      </div>
      <div className="sticky bottom-28 mt-8">
        {draft && !saved && <p role="status" className="mb-2 rounded-xl bg-card p-3 text-center text-sm">Unsaved changes — save to apply these preferences to future briefings. Saved editions stay unchanged.</p>}
        <Button onClick={save} disabled={saving} className="w-full">
          {saving ? "Saving…" : saved ? "Saved. Applies to your next briefing" : "Save changes"}
        </Button>
      </div>
      <p className="mt-6 text-center text-xs text-muted">
        {meta.data.mock_mode ? "Running without an AI key: summaries and rabbit holes are extractive." : "AI mode is on."}
      </p>
    </Shell>
  );
}
