"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, type Profile } from "@/lib/api";
import { ErrorNote, Shell, Spinner, Wordmark } from "@/components/ui";

export default function Home() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    api<Profile>("/api/profile")
      .then((p) => router.replace(p.onboarded ? "/briefing" : "/onboarding"))
      .catch(() => setError("Can't reach the Finite API. Is the backend running on port 8000?"));
  }, [router]);
  return (
    <Shell nav={false}>
      <div className="flex min-h-[70dvh] flex-col items-center justify-center gap-4">
        <Wordmark />
        {error ? <ErrorNote message={error} /> : <Spinner />}
      </div>
    </Shell>
  );
}
