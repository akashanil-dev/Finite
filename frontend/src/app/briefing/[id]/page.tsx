import { Suspense } from "react";
import { Spinner } from "@/components/ui";
import EditionView from "./edition-view";
export default function EditionPage() {
  return <Suspense fallback={<Spinner />}><EditionView /></Suspense>;
}
