import type { Metadata } from "next";
import { Radio_Canada } from "next/font/google";
import "./globals.css";
import Link from "next/link";

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
      <body className={`${inter.className} background-black`}>
        <Link href="/" className="absolute mt-6 ml-6 text-3xl text-title-red">
          {"StreetSide"}
        </Link>
        {children}
      </body>
    </html>
  );
}
