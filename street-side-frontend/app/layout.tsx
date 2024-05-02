import type { Metadata } from "next";
import { Radio_Canada } from "next/font/google";
import "./globals.css";
import NavigationHeader from "./components/NavigationHeader";

const inter = Radio_Canada({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Street Side",
  description: "Financial clearing companies public information.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-background-black`}>
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
          <NavigationHeader />
          {children}
        </main>
      </body>
    </html>
  );
}
