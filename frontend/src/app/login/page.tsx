"use client";

import { useRef, useState, type FormEvent } from "react";
import { api } from "@/lib/api";
import { Button, Wordmark } from "@/components/ui";

export default function Login() {
  const [register, setRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [busy, setBusy] = useState(false);
  const inFlight = useRef(false);
  const [error, setError] = useState<string | null>(null);
  async function submit(event: FormEvent) {
    event.preventDefault();
    if (inFlight.current) return;
    inFlight.current = true;
    setBusy(true);
    setError(null);
    try {
      await api(`/api/auth/${register ? "register" : "login"}`, { method: "POST", json: { username: username.trim(), password } });
      // A full navigation clears account-specific client state after authentication.
      // eslint-disable-next-line @next/next/no-location-assign-relative-destination
      window.location.assign("/");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not sign in. Try again.");
      setBusy(false);
      inFlight.current = false;
    }
  }
  return <main className="mx-auto flex min-h-dvh max-w-md flex-col justify-center px-6 py-12">
    <Wordmark />
    <h1 className="mt-8 font-serif text-3xl">{register ? "Make room for curiosity." : "Welcome back."}</h1>
    <p className="mt-3 text-sm leading-relaxed text-muted">{register ? "Create your account for a personal briefing and a place to keep what you learn." : "Sign in to your briefing and Knowledge Passport."}</p>
    <form onSubmit={submit} className="mt-8 space-y-5">
      <div><label htmlFor="username" className="block text-sm font-medium">Username</label>
        <input id="username" name="username" autoComplete="username" autoCapitalize="none" spellCheck={false} required minLength={3} maxLength={32} pattern="[a-zA-Z0-9_]{3,32}" value={username} onChange={(e) => setUsername(e.target.value)} disabled={busy} className="mt-2 w-full rounded-xl border border-line bg-card px-4 py-3" aria-describedby="username-help" />
        <p id="username-help" className="mt-2 text-xs text-muted">3–32 letters, numbers or underscores. Not case-sensitive.</p></div>
      <div><label htmlFor="password" className="block text-sm font-medium">Password</label>
        <input id="password" name="password" type={showPassword ? "text" : "password"} autoComplete={register ? "new-password" : "current-password"} required minLength={register ? 8 : 1} maxLength={128} value={password} onChange={(e) => setPassword(e.target.value)} disabled={busy} className="mt-2 w-full rounded-xl border border-line bg-card px-4 py-3" aria-describedby={register ? "password-help" : undefined} />
        <label className="mt-2 flex items-center gap-2 text-xs text-muted"><input type="checkbox" checked={showPassword} onChange={(e) => setShowPassword(e.target.checked)} />Show password</label>
        {register && <p id="password-help" className="mt-2 text-xs leading-relaxed text-muted">At least 8 characters. No special-character rules. Keep it somewhere safe; password recovery is not available.</p>}</div>
      {error && <p role="alert" className="rounded-xl bg-warm-soft p-3 text-sm">{error}</p>}
      <Button type="submit" disabled={busy} className="w-full">{busy ? "Please wait…" : register ? "Create account" : "Sign in"}</Button>
    </form>
    <button type="button" disabled={busy} className="mt-6 text-sm text-accent underline underline-offset-4" onClick={() => { setRegister(!register); setError(null); setPassword(""); }}>{register ? "Already have an account? Sign in" : "New to Finite? Create an account"}</button>
  </main>;
}
