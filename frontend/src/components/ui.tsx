"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

const NAV = [
  { href: "/briefing", label: "Briefing", icon: "M4 5h16M4 10h16M4 15h10" },
  { href: "/passport", label: "Passport", icon: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm0 4a5 5 0 1 0 0 10 5 5 0 0 0 0-10z" },
  { href: "/sources", label: "Sources", icon: "M5 4h10l4 4v12H5zM9 12h6M9 16h6" },
  { href: "/settings", label: "Settings", icon: "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM3 12h2m14 0h2M12 3v2m0 14v2" },
];

export function Shell({ children, nav = true }: { children: ReactNode; nav?: boolean }) {
  const path = usePathname();
  return (
    <div className="mx-auto flex min-h-dvh w-full max-w-xl flex-col">
      <main className={`flex-1 px-5 pt-6 ${nav ? "pb-28" : "pb-10"}`}>{children}</main>
      {nav && (
        <nav className="fixed inset-x-0 bottom-0 z-20 border-t border-line bg-paper/95 backdrop-blur">
          <div className="mx-auto grid max-w-xl grid-cols-4">
            {NAV.map((n) => {
              const active = path.startsWith(n.href) || (n.href === "/briefing" && path.startsWith("/story"));
              return (
                <Link key={n.href} href={n.href} className={`flex flex-col items-center gap-1 py-3 text-[11px] ${active ? "text-accent" : "text-muted"}`}>
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
    <span className={`font-serif tracking-tight ${small ? "text-lg" : "text-2xl"}`}>
      Finite<span className="text-warm">.</span>
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
