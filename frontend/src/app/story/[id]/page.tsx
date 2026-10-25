import { Suspense } from "react";
import { Spinner } from "@/components/ui";
import StoryView from "./story-view";

// AuthGate delays this protected segment until the session is checked.
export const instant = false;

export default function StoryPage() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-xl px-5"><Spinner /></div>}>
      <StoryView />
    </Suspense>
  );
}
