import { Suspense } from "react";
import { Spinner } from "@/components/ui";
import StoryView from "./story-view";

export default function StoryPage() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-xl px-5"><Spinner /></div>}>
      <StoryView />
    </Suspense>
  );
}
