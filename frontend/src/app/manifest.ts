import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Finite",
    short_name: "Finite",
    description: "A finite daily briefing that turns current events into journeys of understanding.",
    start_url: "/",
    display: "standalone",
    background_color: "#f5f1ea",
    theme_color: "#f5f1ea",
    icons: [{ src: "/icon.svg", sizes: "any", type: "image/svg+xml" }],
  };
}
