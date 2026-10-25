import View from "./start-view";

// AuthGate withholds protected pages during its client-side session check.
// Keep the validation opt-out in a Server Component; authentication is unchanged.
export const instant = false;

export default function Page() {
  return <View />;
}
