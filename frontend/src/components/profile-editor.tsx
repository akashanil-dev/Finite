"use client";

import { useState } from "react";
import { PRIORITY_LABELS, type Meta, type Profile, type SourcesIndex } from "@/lib/api";
import { Eyebrow, TierBadge } from "./ui";

type Props = { meta: Meta; profile: Profile; onChange: (p: Profile) => void };

const PRIORITY_STYLE: Record<number, string> = {
  0: "border-line bg-card text-ink",
  1: "border-accent/30 bg-accent-soft/50 text-accent",
  2: "border-accent/60 bg-accent-soft text-accent",
  3: "border-accent bg-accent text-paper",
};

export function LanguagePicker({ meta, profile, onChange }: Props) {
  const ml = profile.languages.includes("ml");
  return (
    <div className="space-y-3">
      {meta.languages.map((l) => {
        const on = l.id === "en" ? true : ml;
        return (
          <button
            key={l.id}
            disabled={l.id === "en"}
            onClick={() =>
              onChange({ ...profile, languages: ml ? ["en"] : ["en", "ml"], ui_language: ml ? "en" : profile.ui_language })
            }
            className={`flex w-full items-center justify-between rounded-2xl border p-4 text-left transition ${on ? "border-accent bg-accent-soft" : "border-line bg-card"}`}
          >
            <span>
              <span className="block font-medium">
                {l.name} {l.native && <span className="ml-1 text-muted">{l.native}</span>}
              </span>
              <span className="text-xs text-muted">
                {l.id === "en" ? "National and international outlets (always on)" : "Adds Mathrubhumi, Asianet News, Twenty Four and more to your crawl"}
              </span>
            </span>
            <span className={`h-5 w-5 rounded-full border-2 ${on ? "border-accent bg-accent" : "border-line"}`} />
          </button>
        );
      })}
      {ml && (
        <label className="flex items-center justify-between rounded-2xl border border-line bg-card p-4 text-sm">
          <span>
            Show summaries and rabbit holes in Malayalam
            <span className="block text-xs text-muted">You can switch per story anytime</span>
          </span>
          <input
            type="checkbox"
            className="h-5 w-5 accent-[#1f5c50]"
            checked={profile.ui_language === "ml"}
            onChange={(e) => onChange({ ...profile, ui_language: e.target.checked ? "ml" : "en" })}
          />
        </label>
      )}
    </div>
  );
}

export function InterestPicker({ meta, profile, onChange }: Props) {
  const [open, setOpen] = useState<string | null>(meta.taxonomy[0]?.id ?? null);
  const set = (id: string) => {
    const cur = profile.interests[id] ?? 0;
    const next = (cur + 1) % 4;
    const interests = { ...profile.interests };
    if (next) interests[id] = next;
    else delete interests[id];
    onChange({ ...profile, interests, excluded_subfields: profile.excluded_subfields.filter((x) => x !== id) });
  };
  return (
    <div className="space-y-3">
      <p className="text-xs text-muted">Tap once for occasional, twice for moderate, three times for high priority. A fourth tap removes it.</p>
      {meta.taxonomy.map((f) => {
        const count = f.subfields.filter((s) => profile.interests[s.id]).length;
        const isOpen = open === f.id;
        return (
          <div key={f.id} className="overflow-hidden rounded-2xl border border-line bg-card">
            <button onClick={() => setOpen(isOpen ? null : f.id)} className="flex w-full items-center justify-between p-4 text-left">
              <span className="font-medium">{f.name}</span>
              <span className="text-xs text-muted">
                {count}/{f.subfields.length} <span className="ml-1 inline-block transition" style={{ transform: isOpen ? "rotate(90deg)" : "" }}>›</span>
              </span>
            </button>
            {isOpen && (
              <div className="flex flex-wrap gap-2 px-4 pb-4">
                {f.subfields.map((s) => {
                  const p = profile.interests[s.id] ?? 0;
                  return (
                    <button key={s.id} onClick={() => set(s.id)} className={`rounded-full border px-3 py-1.5 text-sm transition ${PRIORITY_STYLE[p]}`}>
                      {s.name}
                      {p > 0 && <span className="ml-1.5 text-[10px] opacity-80">· {PRIORITY_LABELS[p]}</span>}
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export function Exclusions({ meta, profile, onChange, sources }: Props & { sources: SourcesIndex | null }) {
  const toggle = (key: "excluded_subfields" | "excluded_sources", id: string) => {
    const list = profile[key];
    onChange({ ...profile, [key]: list.includes(id) ? list.filter((x) => x !== id) : [...list, id] });
  };
  const unselected = meta.taxonomy.flatMap((f) => f.subfields).filter((s) => !profile.interests[s.id]);
  const langs = new Set(profile.languages);
  return (
    <div className="space-y-6">
      <div>
        <Eyebrow>Never show me</Eyebrow>
        <div className="mt-3 flex flex-wrap gap-2">
          {unselected.map((s) => {
            const on = profile.excluded_subfields.includes(s.id);
            return (
              <button
                key={s.id}
                onClick={() => toggle("excluded_subfields", s.id)}
                className={`rounded-full border px-3 py-1.5 text-sm ${on ? "border-warm bg-warm-soft text-warm line-through" : "border-line bg-card"}`}
              >
                {s.name}
              </button>
            );
          })}
        </div>
      </div>
      {sources && (
        <div>
          <Eyebrow>Exclude sources</Eyebrow>
          <p className="mt-2 text-xs text-muted">Check a source to leave it out of future briefings.</p>
          <div className="mt-3 divide-y divide-line rounded-2xl border border-line bg-card">
            {sources.sources
              .filter((s) => langs.has(s.lang))
              .map((s) => {
                const off = profile.excluded_sources.includes(s.id);
                return (
                  <label key={s.id} className="flex items-center justify-between gap-3 px-4 py-3 text-sm">
                    <span className={off ? "text-muted line-through" : ""}>
                      {s.name} <TierBadge tier={s.tier} label={sources.tiers[s.tier]?.label} />
                    </span>
                    <input type="checkbox" className="h-4 w-4 accent-[#1f5c50]" checked={off} onChange={() => toggle("excluded_sources", s.id)} />
                  </label>
                );
              })}
          </div>
        </div>
      )}
    </div>
  );
}

export function ScheduleForm({ meta, profile, onChange }: Props) {
  const period = meta.periods.find((p) => p.time === profile.delivery_time)?.id;
  return (
    <div className="space-y-7">
      <section>
        <Eyebrow>Delivery period</Eyebrow>
        <div className="mt-3 grid grid-cols-2 gap-2">
          {meta.periods.map((p) => (
            <button
              key={p.id}
              onClick={() => onChange({ ...profile, delivery_time: p.time })}
              className={`rounded-2xl border p-3 text-left ${period === p.id ? "border-accent bg-accent-soft" : "border-line bg-card"}`}
            >
              <span className="block font-medium">{p.label}</span>
              <span className="text-xs text-muted">{p.range}</span>
            </button>
          ))}
        </div>
        <label className="mt-3 flex items-center justify-between rounded-2xl border border-line bg-card px-4 py-3 text-sm">
          <span>
            Exact time <span className="text-xs text-muted">({profile.timezone})</span>
          </span>
          <input
            type="time"
            value={profile.delivery_time}
            onChange={(e) => onChange({ ...profile, delivery_time: e.target.value })}
            className="bg-transparent text-right font-medium"
          />
        </label>
        <p className="mt-2 text-xs text-muted">When scheduled delivery is enabled, your briefing is prepared 30 minutes before this time. Every prepared briefing is frozen so it doesn&apos;t change while you read.</p>
      </section>

      <section>
        <Eyebrow>News lookback window</Eyebrow>
        <div className="mt-3 grid grid-cols-3 gap-2">
          {[24, 30, 48].map((h) => (
            <button
              key={h}
              onClick={() => onChange({ ...profile, lookback_hours: h })}
              className={`rounded-full border py-2 text-sm ${profile.lookback_hours === h ? "border-accent bg-accent text-paper" : "border-line bg-card"}`}
            >
              {h} hours
            </button>
          ))}
        </div>
        <p className="mt-2 text-xs text-muted">30 hours overlaps your previous briefing by six hours so late stories aren&apos;t missed. Stories you already received are removed.</p>
      </section>

      <section>
        <div className="flex items-baseline justify-between">
          <Eyebrow>Stories per briefing</Eyebrow>
          <span className="font-serif text-2xl">{profile.stories_per_briefing}</span>
        </div>
        <input
          type="range"
          min={3}
          max={25}
          value={profile.stories_per_briefing}
          onChange={(e) => onChange({ ...profile, stories_per_briefing: Number(e.target.value) })}
          className="mt-3 w-full accent-[#1f5c50]"
        />
      </section>

      <section>
        <Eyebrow>Default reading depth</Eyebrow>
        <div className="mt-3 space-y-2">
          {meta.depths.map((d) => (
            <button
              key={d.id}
              onClick={() => onChange({ ...profile, depth: d.id })}
              className={`flex w-full items-center justify-between rounded-2xl border p-3 text-left ${profile.depth === d.id ? "border-accent bg-accent-soft" : "border-line bg-card"}`}
            >
              <span className="font-medium">{d.label}</span>
              <span className="text-xs text-muted">{d.desc}</span>
            </button>
          ))}
        </div>
      </section>

      <div className="rounded-2xl bg-ink p-4 text-sm text-paper">
        <div className="text-[11px] uppercase tracking-[0.14em] text-paper/60">Your briefing configuration</div>
        <div className="mt-1 font-serif text-lg">
          {profile.stories_per_briefing} stories · Past {profile.lookback_hours} hours · {profile.delivery_time} · {profile.depth} depth
        </div>
      </div>
    </div>
  );
}
