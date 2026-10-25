import BriefingLibrary from "./briefing-library";

// AuthGate deliberately withholds this account-specific UI until its client
// session check finishes. It cannot promise an instant render during validation.
// This config must live in a Server Component, not the client library below.
export const instant = false;

export default function BriefingPage() {
  return <BriefingLibrary />;
}
