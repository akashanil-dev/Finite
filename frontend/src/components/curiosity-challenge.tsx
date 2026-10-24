"use client";

import { useState } from "react";
import { Button, Eyebrow } from "./ui";

const predictions = [
  { id: "history", label: "A shared history", detail: "Earlier events or ideas helped shape both." },
  { id: "mechanism", label: "A similar mechanism", detail: "The same process or principle connects them." },
  { id: "impact", label: "A wider impact", detail: "The connection changes things for people or institutions." },
];

export function CuriosityChallenge({ question, onReveal, onCancel }: {
  question: string;
  onReveal: (prediction?: string) => void;
  onCancel: () => void;
}) {
  const [selected, setSelected] = useState<string | null>(null);
  return (
    <section className="mt-8 rounded-3xl border border-accent/30 bg-accent-soft/50 p-5" aria-label="Curiosity challenge">
      <Eyebrow>Curiosity challenge · optional</Eyebrow>
      <h3 className="mt-2 font-serif text-2xl">Predict the connection</h3>
      <p className="mt-2 text-sm leading-relaxed">{question}</p>
      <fieldset className="mt-5">
        <legend className="text-sm font-medium">What kind of connection do you expect?</legend>
        <div className="mt-3 space-y-2">
          {predictions.map((p) => <label key={p.id} className={`flex cursor-pointer items-start gap-3 rounded-2xl border p-4 ${selected === p.id ? "border-accent bg-card" : "border-line bg-paper"}`}>
            <input type="radio" name="connection-prediction" value={p.id} checked={selected === p.id} onChange={() => setSelected(p.id)} className="mt-1 accent-[#1f5c50]" />
            <span><span className="block text-sm font-medium">{p.label}</span><span className="mt-1 block text-xs text-muted">{p.detail}</span></span>
          </label>)}
        </div>
      </fieldset>
      <p className="mt-3 text-xs leading-relaxed text-muted">A prediction, not a quiz. More than one connection may fit. Read the sources and decide whether your idea holds up.</p>
      <div className="mt-5 flex flex-col gap-2">
        <Button disabled={!selected} onClick={() => onReveal(predictions.find((p) => p.id === selected)?.label)}>Reveal the exploration</Button>
        <Button variant="ghost" onClick={() => onReveal()}>Skip and explore</Button>
        <button onClick={onCancel} className="py-2 text-sm text-muted underline">Back to connections</button>
      </div>
    </section>
  );
}
