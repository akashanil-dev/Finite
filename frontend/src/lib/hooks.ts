"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "./api";

type Result<T> = { key: string; data: T | null; error: string | null };

export function useApi<T>(path: string | null) {
  const [tick, setTick] = useState(0);
  const [result, setResult] = useState<Result<T> | null>(null);
  const [override, setOverride] = useState<{ key: string; data: T | null } | null>(null);
  const key = `${path}#${tick}`;

  useEffect(() => {
    if (!path) return;
    let alive = true;
    api<T>(path)
      .then((data) => alive && setResult({ key, data, error: null }))
      .catch((e) => alive && setResult({ key, data: null, error: e instanceof Error ? e.message : "Something went wrong" }));
    return () => {
      alive = false;
    };
  }, [path, key]);

  const reload = useCallback(() => setTick((t) => t + 1), []);
  const setData = useCallback((data: T | null) => setOverride({ key, data }), [key]);

  const fresh = result?.key === key ? result : null;
  const data = override?.key === key ? override.data : (fresh?.data ?? null);
  return { data, setData, error: fresh?.error ?? null, loading: !!path && !fresh && override?.key !== key, reload };
}
