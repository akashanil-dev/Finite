import { Suspense } from "react";
import { Spinner } from "@/components/ui";
import EditionView from "./edition-view";
// AuthGate delays this protected segment until the session is checked.
export const instant = false;

export default function EditionPage() {
  return <Suspense fallback={<Spinner />}><EditionView /></Suspense>;
}
