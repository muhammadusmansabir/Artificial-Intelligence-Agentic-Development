import "@/app/globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "Health AI Chatbot",
  description: "AI-powered nutrition assistant",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
