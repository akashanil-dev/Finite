import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Finite",
    short_name: "Finite",
    description: "A finite daily briefing that turns current events into journeys of understanding.",
    start_url: "/",
    display: "standalone",
    background_color: "#f4f1e8",
    theme_color: "#f4f1e8",
    icons: [{ src: "/icon.svg", sizes: "any", type: "image/svg+xml" }],
  };
}
