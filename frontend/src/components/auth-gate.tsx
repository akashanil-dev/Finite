"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";
import { api, ApiError } from "@/lib/api";

export function AuthGate({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const publicPage = ["/", "/login", "/signup"].includes(pathname);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    if (publicPage) return;
    let alive = true;
    api("/api/auth/me").then(() => { if (alive) setReady(true); }).catch((e) => {
      if (!alive) return;
      if (e instanceof ApiError && e.status === 401) window.location.replace("/login");
      else setError("Cannot reach Finite. Check your connection and try again.");
    });
    return () => { alive = false; };
  }, [publicPage, attempt]);
  // Recheck after browser back/forward cache restoration, including after logout.
  useEffect(() => {
    const restore = (event: PageTransitionEvent) => { if (event.persisted) window.location.reload(); };
    window.addEventListener("pageshow", restore);
    return () => window.removeEventListener("pageshow", restore);
  }, []);
  if (publicPage || ready) return children;
  return <main className="mx-auto max-w-xl px-5 py-20 text-center">
    <p role="status" className="text-sm text-muted">{error ?? "Opening your Finite account…"}</p>
    {error && <button className="mt-4 rounded-full border border-line px-5 py-2" onClick={() => { setError(null); setAttempt(attempt + 1); }}>Try again</button>}
  </main>;
}
