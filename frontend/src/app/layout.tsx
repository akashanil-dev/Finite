import type { Metadata, Viewport } from "next";
import { Inter, Newsreader, Noto_Sans_Malayalam } from "next/font/google";
import "./globals.css";
import { Suspense } from "react";
import { AuthGate } from "@/components/auth-gate";

const inter = Inter({ variable: "--font-inter", subsets: ["latin"] });
const newsreader = Newsreader({ variable: "--font-newsreader", subsets: ["latin"], style: ["normal", "italic"] });
const malayalam = Noto_Sans_Malayalam({ variable: "--font-malayalam", subsets: ["malayalam"] });

export const metadata: Metadata = {
  title: "Finite — news that ends, understanding that doesn't",
  description: "A finite daily briefing that turns current events into journeys of understanding.",
  manifest: "/manifest.webmanifest",
  appleWebApp: { capable: true, title: "Finite", statusBarStyle: "default" },
};

export const viewport: Viewport = {
  themeColor: "#f5f1ea",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${inter.variable} ${newsreader.variable} ${malayalam.variable} h-full antialiased`}>
      <body className="min-h-full"><Suspense fallback={<p className="p-8 text-center">Opening Finite…</p>}><AuthGate>{children}</AuthGate></Suspense></body>
    </html>
  );
}
