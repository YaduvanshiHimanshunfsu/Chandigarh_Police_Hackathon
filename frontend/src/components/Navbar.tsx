import Link from "next/link";
import { Shield, FileText, Search, PlusCircle, Activity } from "lucide-react";

export default function Navbar() {
  return (
    <header className="border-b border-police-accent/20 bg-police-dark/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-police-accent/10 border border-police-accent flex items-center justify-center text-police-accent">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <div className="font-bold text-lg tracking-wider text-white flex items-center gap-2">
              PRATIBIMB PRAMAN
              <span className="text-xs px-2 py-0.5 bg-police-accent/20 text-police-accent rounded border border-police-accent/40 font-mono">
                BSA §63 READY
              </span>
            </div>
            <div className="text-xs text-gray-400">
              Chandigarh Police • AI Media Provenance & Origin Intelligence
            </div>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="flex items-center gap-6">
          <Link
            href="/"
            className="text-sm font-medium text-gray-300 hover:text-police-accent flex items-center gap-1.5 transition-colors"
          >
            <Activity className="w-4 h-4" />
            Dashboard
          </Link>
          <Link
            href="/cases"
            className="text-sm font-medium text-gray-300 hover:text-police-accent flex items-center gap-1.5 transition-colors"
          >
            <FileText className="w-4 h-4" />
            Case Queue
          </Link>
          <Link
            href="/#intake"
            className="text-sm font-medium px-3.5 py-1.5 rounded-md bg-police-accent/20 border border-police-accent text-police-accent hover:bg-police-accent/30 flex items-center gap-1.5 transition-all shadow-sm"
          >
            <PlusCircle className="w-4 h-4" />
            New Forensic Intake
          </Link>
        </nav>
      </div>
    </header>
  );
}
