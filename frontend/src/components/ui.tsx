"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";

const NAV = [
  { href: "/briefing", label: "Briefing", icon: "M4 5h16M4 10h16M4 15h10" },
  { href: "/passport", label: "Passport", icon: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm0 4a5 5 0 1 0 0 10 5 5 0 0 0 0-10z" },
  { href: "/sources", label: "Sources", icon: "M5 4h10l4 4v12H5zM9 12h6M9 16h6" },
  { href: "/settings", label: "Settings", icon: "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM3 12h2m14 0h2M12 3v2m0 14v2" },
];

export function Shell({ children, nav = true, immersive = false }: { children: ReactNode; nav?: boolean; immersive?: boolean }) {
  const path = usePathname();
  const [hiddenAt, setHiddenAt] = useState<string | null>(null);
  useEffect(() => {
    let touchY: number | null = null;
    const wheel = (event: WheelEvent) => {
      if (Math.abs(event.deltaY) > Math.abs(event.deltaX) && Math.abs(event.deltaY) > 2)
        setHiddenAt(event.deltaY > 0 ? path : null);
    };
    const start = (event: TouchEvent) => { touchY = event.touches[0]?.clientY ?? null; };
    const move = (event: TouchEvent) => {
      const y = event.touches[0]?.clientY;
      if (touchY === null || y === undefined || Math.abs(y - touchY) < 16) return;
      setHiddenAt(y < touchY ? path : null);
      touchY = y;
    };
    document.addEventListener("wheel", wheel, { passive: true });
    document.addEventListener("touchstart", start, { passive: true });
    document.addEventListener("touchmove", move, { passive: true });
    return () => {
      document.removeEventListener("wheel", wheel);
      document.removeEventListener("touchstart", start);
      document.removeEventListener("touchmove", move);
    };
  }, [path]);
  return (
    <div className="app-shell" data-nav={nav} data-immersive={immersive}>
      <main className="app-main">{children}</main>
      {nav && (
        <nav className="app-nav" data-hidden={hiddenAt === path} aria-label="Main navigation">
          <div className="nav-brand" aria-hidden="true">Finite.</div>
          <div className="nav-items">
            {NAV.map((n) => {
              const active = path.startsWith(n.href) || (n.href === "/briefing" && path.startsWith("/story"));
              return (
                <Link key={n.href} href={n.href} className="nav-link" aria-current={active ? "page" : undefined}>
                  <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={1.6} strokeLinecap="round" strokeLinejoin="round">
                    <path d={n.icon} />
                  </svg>
                  {n.label}
                </Link>
              );
            })}
          </div>
        </nav>
      )}
    </div>
  );
}

export function Wordmark({ small }: { small?: boolean }) {
  return (
    <span className={`wordmark ${small ? "text-lg" : "text-2xl"}`}>
      Finite<span className="wordmark-dot">.</span>
    </span>
  );
}

export function Button({
  children,
  onClick,
  variant = "primary",
  disabled,
  className = "",
  type = "button",
}: {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "ghost" | "soft";
  disabled?: boolean;
  className?: string;
  type?: "button" | "submit";
}) {
  const styles = {
    primary: "bg-ink text-paper hover:bg-ink/90",
    soft: "bg-accent-soft text-accent hover:bg-accent-soft/70",
    ghost: "border border-line text-ink hover:bg-card",
  }[variant];
  return (
    <button type={type} onClick={onClick} disabled={disabled} className={`rounded-full px-5 py-3 text-sm font-medium transition disabled:opacity-40 ${styles} ${className}`}>
      {children}
    </button>
  );
}

export function Eyebrow({ children }: { children: ReactNode }) {
  return <div className="text-[11px] font-semibold uppercase tracking-[0.14em] text-muted">{children}</div>;
}

const TIER_STYLE: Record<string, string> = {
  primary: "bg-accent text-paper",
  factcheck: "bg-accent-soft text-accent",
  established: "bg-[#ece7dd] text-ink",
  specialist: "bg-[#e7e3f1] text-[#3d3570]",
  regional: "bg-warm-soft text-warm",
  aggregator: "bg-transparent border border-line text-muted",
};

export function TierBadge({ tier, label }: { tier: string; label?: string }) {
  return <span className={`inline-block rounded-full px-2 py-0.5 text-[10px] font-medium ${TIER_STYLE[tier] ?? TIER_STYLE.established}`}>{label ?? tier}</span>;
}

export function WeightBar({ weight }: { weight: number }) {
  return (
    <span className="inline-flex items-center gap-1.5 text-[11px] text-muted" title={`Confidence weight ${weight.toFixed(2)}`}>
      <span className="relative h-1.5 w-12 overflow-hidden rounded-full bg-line">
        <span className="absolute inset-y-0 left-0 rounded-full bg-accent" style={{ width: `${weight * 100}%` }} />
      </span>
      {weight.toFixed(2)}
    </span>
  );
}

export function Spinner({ label }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 py-6 text-sm text-muted">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-line border-t-accent" />
      {label}
    </div>
  );
}

export function Skeleton({ lines = 3 }: { lines?: number }) {
  return (
    <div className="space-y-2.5 py-2">
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="skeleton h-3.5" style={{ width: `${92 - i * 13}%` }} />
      ))}
    </div>
  );
}

export function ErrorNote({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="rounded-2xl border border-warm/30 bg-warm-soft p-4 text-sm text-warm">
      {message}
      {onRetry && (
        <button onClick={onRetry} className="ml-2 underline">
          Try again
        </button>
      )}
    </div>
  );
}

export function Fold({ open, children, id }: { open: boolean; children: ReactNode; id?: string }) {
  return <div id={id} className="fold" data-open={open} inert={!open} aria-hidden={!open}>
    <div className="fold-inner"><div className="fold-body">{children}</div></div>
  </div>;
}

export function CompletionFlower() {
  return <svg className="completion-flower" aria-hidden="true" viewBox="0 0 80 80">
    {Array.from({ length: 8 }, (_, i) => <ellipse key={i} cx="40" cy="23" rx="10" ry="19" fill="currentColor" transform={`rotate(${i * 45} 40 40)`} />)}
    <circle cx="40" cy="40" r="12" fill="#20211f" /><path d="m34 40 4 4 8-8" fill="none" stroke="#d3ed80" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
  </svg>;
}

export function Segmented<T extends string>({ value, options, onChange, label }: { value: T; options: readonly T[]; onChange: (value: T) => void; label: string }) {
  return <div className="segmented" role="group" aria-label={label}>
    <span className="segmented-glider" aria-hidden="true" style={{ width: `calc((100% - 8px) / ${options.length})`, transform: `translateX(${Math.max(0, options.indexOf(value)) * 100}%)` }} />
    {options.map((option) => <button key={option} type="button" aria-pressed={option === value} onClick={() => onChange(option)}>{option}</button>)}
  </div>;
}
