import type { Metadata } from "next";
import { Cairo } from "next/font/google";
import "./globals.css";
import PixelTracker from "@/components/PixelTracker";

const cairo = Cairo({
  variable: "--font-cairo",
  subsets: ["arabic", "latin"],
  weight: ["200", "300", "400", "500", "600", "700", "800", "900"],
});

export const metadata: Metadata = {
  title: "إطار الصوت الفني",
  description: "أنشئ إطارات فنية شخصية مع رموز QR التي ترتبط برسائلك الصوتية",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar" dir="rtl">
      <body className={`${cairo.variable} font-cairo antialiased`}>
        <PixelTracker />
        {children}
      </body>
    </html>
  );
}
