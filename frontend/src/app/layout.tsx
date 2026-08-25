import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "PratiBimb Praman — AI Media Forensic & Origin Intelligence",
  description:
    "Evidence-fusion forensic platform engineered for Indian Law Enforcement & Chandigarh Police Hackathon 2026.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-police-dark text-slate-100 antialiased flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
        <footer className="border-t border-slate-800/80 bg-police-dark/50 py-4 text-center text-xs text-slate-500">
          PratiBimb Praman v1.0 • Built for Chandigarh Police National Hackathon 2026 • Bharatiya Sakshya Adhiniyam §63 Admissible
        </footer>
      </body>
    </html>
  );
}
