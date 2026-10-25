"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { api, type Meta, type Profile, type SourcesIndex } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { Exclusions, InterestPicker, LanguagePicker, ScheduleForm } from "@/components/profile-editor";
import { Button, ErrorNote, Eyebrow, Shell, Spinner, Wordmark } from "@/components/ui";

const STEPS = [
  { title: "Choose your languages", sub: "Pick the languages you read news in." },
  { title: "Build your curiosity profile", sub: "Choose the fields and subfields you care about, and how much each one matters." },
  { title: "Anything to leave out?", sub: "Exclude subjects or sources. You can change this anytime." },
  { title: "Configure your daily briefing", sub: "One finite briefing a day. No endless scroll." },
];

export default function Onboarding() {
  const router = useRouter();
  const meta = useApi<Meta>("/api/meta");
  const prof = useApi<Profile>("/api/profile");
  const sources = useApi<SourcesIndex>("/api/sources");
  const [draft, setProfile] = useState<Profile | null>(null);
  const profile = draft ?? prof.data;
  const [step, setStep] = useState(-1);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (meta.error || prof.error) return <Shell nav={false}><ErrorNote message={meta.error || prof.error || ""} /></Shell>;
  if (!meta.data || !profile) return <Shell nav={false}><Spinner /></Shell>;

  const selected = Object.keys(profile.interests).length;

  const finish = async () => {
    setBusy(true);
    setError(null);
    try {
      await api("/api/profile", { method: "PUT", json: { ...profile, onboarded: true } });
      await api("/api/briefings", { method: "POST" });
      router.push("/briefing");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not prepare your briefing");
      setBusy(false);
    }
  };

  if (step === -1)
    return (
      <Shell nav={false}>
        <div className="flex min-h-[85dvh] flex-col justify-between">
          <div className="pt-6">
            <Wordmark />
          </div>
          <div className="rise space-y-6">
            <h1 className="font-serif text-[2.6rem] leading-[1.05] tracking-tight">
              News that ends.
              <br />
              <span className="italic text-accent">Understanding</span> that doesn&apos;t.
            </h1>
            <p className="text-muted">
              Most news tells you what happened. Finite also helps you understand why it happened, how we got here, and what it connects to. Then it stops.
            </p>
            <ol className="space-y-3 text-sm">
              {["Define your interests", "Set your daily briefing", "Read a finite, source-backed feed", "Open a rabbit hole when you're curious", "Reach an ending"].map(
                (t, i) => (
                  <li key={t} className="flex items-center gap-3">
                    <span className="font-serif text-lg text-warm">0{i + 1}</span>
                    {t}
                  </li>
                ),
              )}
            </ol>
          </div>
          <Button onClick={() => setStep(0)} className="w-full">
            Begin
          </Button>
        </div>
      </Shell>
    );

  const s = STEPS[step];
  return (
    <Shell nav={false}>
      <div className="mb-6 flex items-center justify-between">
        <button onClick={() => setStep(step - 1)} className="text-sm text-muted">
          ← Back
        </button>
        <div className="flex gap-1.5">
          {STEPS.map((_, i) => (
            <span key={i} className={`h-1.5 w-6 rounded-full ${i <= step ? "bg-accent" : "bg-line"}`} />
          ))}
        </div>
      </div>
      <div key={step} className="rise">
        <Eyebrow>Step {step + 1} of {STEPS.length}</Eyebrow>
        <h1 className="mt-2 font-serif text-3xl leading-tight">{s.title}</h1>
        <p className="mb-6 mt-2 text-sm text-muted">{s.sub}</p>
        {step === 0 && <LanguagePicker meta={meta.data} profile={profile} onChange={setProfile} />}
        {step === 1 && <InterestPicker meta={meta.data} profile={profile} onChange={setProfile} />}
        {step === 2 && <Exclusions meta={meta.data} profile={profile} onChange={setProfile} sources={sources.data} />}
        {step === 3 && <ScheduleForm meta={meta.data} profile={profile} onChange={setProfile} />}
      </div>
      {error && <div className="mt-4"><ErrorNote message={error} /></div>}
      <div className="sticky bottom-0 -mx-5 mt-8 bg-gradient-to-t from-paper via-paper to-transparent px-5 pb-6 pt-6">
        {step < STEPS.length - 1 ? (
          <Button onClick={() => setStep(step + 1)} disabled={step === 1 && selected === 0} className="w-full">
            {step === 1 ? `Continue with ${selected} interest${selected === 1 ? "" : "s"}` : "Continue"}
          </Button>
        ) : (
          <Button onClick={finish} disabled={busy} className="w-full">
            {busy ? "Gathering and ranking today's stories…" : "Prepare my first briefing"}
          </Button>
        )}
      </div>
    </Shell>
  );
}
