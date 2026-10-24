"use client";

import { useState } from "react";
import { WeightBar } from "./ui";

export type CiteInfo = { name: string; title: string; url: string; weight?: number; kind?: string };

export function CitationChips({ refs, lookup }: { refs: string[]; lookup: (ref: string) => CiteInfo | undefined }) {
  const [open, setOpen] = useState<string | null>(null);
  const info = open ? lookup(open) : undefined;
  return (
    <span className="inline">
      {refs.map((r) => {
        const i = lookup(r);
        return (
          <button
            key={r}
            onClick={() => setOpen(open === r ? null : r)}
            aria-expanded={open === r}
            aria-label={`Citation: ${i?.name ?? r}`}
            className={`ml-1 inline-flex translate-y-[-1px] items-center rounded-md px-1.5 py-0.5 align-middle text-[10px] font-semibold ${
              i?.kind === "background" ? "bg-[#e7e3f1] text-[#3d3570]" : "bg-accent-soft text-accent"
            }`}
          >
            {i?.name ? i.name : r}
          </button>
        );
      })}
      {info && (
        <span className="mt-2 block rounded-xl border border-line bg-paper p-3 text-xs">
          <span className="flex items-center justify-between gap-2">
            <span className="font-semibold">{info.name}</span>
            {info.weight !== undefined && <WeightBar weight={info.weight} />}
          </span>
          <span className="mt-1 block text-muted">{info.title}</span>
          <a href={info.url} target="_blank" rel="noreferrer" className="mt-1.5 inline-block text-accent underline">
            Read the original →
          </a>
        </span>
      )}
    </span>
  );
}

const CONF: Record<string, { label: string; cls: string }> = {
  verified: { label: "Established", cls: "bg-accent-soft text-accent" },
  reported: { label: "Reported", cls: "bg-[#ece7dd] text-ink" },
  disputed: { label: "Disputed", cls: "bg-warm-soft text-warm" },
};

export function ConfidenceBadge({ level }: { level: string }) {
  const c = CONF[level] ?? CONF.reported;
  return <span className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${c.cls}`}>{c.label}</span>;
}
