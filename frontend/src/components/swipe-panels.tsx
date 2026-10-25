"use client";

import { useRef, useState, useEffect, type ReactNode } from "react";

export function SwipePanels({ panels, initialIndex = 0, onChange }: { initialIndex?: number; onChange?: (index: number) => void; panels: { label: string; content: ReactNode }[] }) {
  const track = useRef<HTMLDivElement>(null);
  const [selected, setSelected] = useState(initialIndex);
  const initialPanel = useRef(initialIndex);
  const currentPanel = useRef(initialIndex);
  useEffect(() => {
    const element = track.current;
    if (!element) return;
    element.scrollLeft = initialPanel.current * element.clientWidth;
    // Keep the active panel aligned after rotation or a viewport resize.
    const observer = new ResizeObserver(() => {
      element.scrollTo({ left: currentPanel.current * element.clientWidth, behavior: 'instant' });
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);
  function go(index: number) {
    const element = track.current;
    if (!element) return;
    element.scrollTo({ left: index * element.clientWidth, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  }
  return <div className="swipe-panels">
    <div className="swipe-tabs" role="group" aria-label="Story panels">
      {panels.map((panel, i) => <button key={panel.label} type="button" aria-pressed={selected === i} onClick={() => go(i)}>{panel.label}<span aria-hidden="true">{i === selected ? ' ●' : ''}</span></button>)}
    </div>
    <p className="swipe-hint">Swipe sideways to explore · {selected + 1} / {panels.length}</p>
    <div ref={track} className="swipe-track" onScroll={(event) => {
      if (event.target !== event.currentTarget) return;
      const el = event.currentTarget;
      const index = Math.round(el.scrollLeft / el.clientWidth);
      currentPanel.current = index;
      setSelected(index); onChange?.(index);
    }} onKeyDown={(event) => {
      if (event.target !== event.currentTarget) return;
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault(); go(Math.max(0, Math.min(panels.length - 1, selected + (event.key === 'ArrowRight' ? 1 : -1))));
      }
    }} tabIndex={0} aria-label="Story panels; use left and right arrow keys">
      {panels.map((panel, i) => <section key={panel.label} className="swipe-panel" aria-label={panel.label} inert={selected !== i}>
        {panel.content}
      </section>)}
    </div>
  </div>;
}
