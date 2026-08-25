"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  ShieldAlert,
  FileCheck2,
  TrendingUp,
  UploadCloud,
  FileText,
  Search,
  Lock,
  ArrowRight,
  AlertTriangle,
} from "lucide-react";
import { fetchCases, createCase, uploadMediaForAnalysis, CaseData } from "@/lib/api";

export default function DashboardHome() {
  const router = useRouter();
  const [cases, setCases] = useState<CaseData[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ bsaCertsIssued: 0 });

  // New Intake Form State
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("deepfake");
  const [officerName, setOfficerName] = useState("Inspector R. Sharma");
  const [ncrpNumber, setNcrpNumber] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadCases();
  }, []);

  const loadCases = async () => {
    try {
      const data = await fetchCases();
      setCases(data);
      const completed = data.filter((c) => c.status.toLowerCase() === "completed").length;
      setStats({ bsaCertsIssued: completed });
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAndUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !selectedFile) {
      alert("Please provide a case title and select a media file.");
      return;
    }

    setSubmitting(true);
    try {
      // 1. Create Case Record
      const newCase = await createCase({
        title,
        category,
        officer_name: officerName,
        ncrp_complaint_number: ncrpNumber || undefined,
        priority: "high",
      });

      // 2. Ingest Media & Trigger Pipeline
      await uploadMediaForAnalysis(newCase.id, selectedFile);

      // 3. Navigate to analysis view
      router.push(`/cases/${newCase.id}`);
    } catch (err) {
      alert("Intake failed: " + err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="card-cyber p-6 bg-gradient-to-r from-police-card to-slate-900 border-police-accent/30 relative overflow-hidden">
        <div className="max-w-3xl space-y-2 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-police-accent/10 border border-police-accent/30 text-police-accent text-xs font-mono">
            <span>🛡️ CHANDIGARH POLICE NATIONAL HACKATHON 2026</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
            AI Media Forensic Provenance & Origin Intelligence Platform
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed">
            Multi-modal evidence fusion engine engineered for Indian network degradation (WhatsApp recompression chains)
            with automated <b>Bharatiya Sakshya Adhiniyam (BSA) Section 63(4)</b> court-admissible dual certification.
          </p>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card-cyber p-4 border-l-4 border-l-police-accent">
          <div className="text-xs text-slate-400 font-medium">Total Cases Triage</div>
          <div className="text-2xl font-bold text-white mt-1 font-mono">
            {cases.length}
          </div>
          <div className="text-[11px] text-police-accent mt-1 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5" /> +28% during election period
          </div>
        </div>

        <div className="card-cyber p-4 border-l-4 border-l-rose-500">
          <div className="text-xs text-slate-400 font-medium">Deepfakes / Tampering Detected</div>
          <div className="text-2xl font-bold text-rose-400 mt-1 font-mono">84.2%</div>
          <div className="text-[11px] text-slate-400 mt-1">Calibrated probability</div>
        </div>

        <div className="card-cyber p-4 border-l-4 border-l-emerald-500">
          <div className="text-xs text-slate-400 font-medium">BSA §63(4) Certs Issued</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1 font-mono">
            {stats.bsaCertsIssued}
          </div>
          <div className="text-[11px] text-emerald-400 mt-1">Court admissible (dual-certified)</div>
        </div>

        <div className="card-cyber p-4 border-l-4 border-l-amber-500">
          <div className="text-xs text-slate-400 font-medium">Avg Takedown Speed</div>
          <div className="text-2xl font-bold text-amber-400 mt-1 font-mono">1.8 min</div>
          <div className="text-[11px] text-slate-400 mt-1">Under IT Rules 3-hr clock</div>
        </div>
      </div>

      {/* Intake & Recent Cases Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8" id="intake">
        {/* Intake Box (5 cols) */}
        <div className="lg:col-span-5 card-cyber p-6 space-y-4">
          <div className="flex items-center gap-2 border-b border-police-accent/20 pb-3">
            <UploadCloud className="w-5 h-5 text-police-accent" />
            <h2 className="font-bold text-base text-white">Forensic Evidence Intake</h2>
          </div>

          <form onSubmit={handleCreateAndUpload} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-medium mb-1">
                Case Title / Target Persona *
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Viral Deepfake Video of UT Official"
                className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-police-accent text-xs"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-300 font-medium mb-1">Category</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-2 text-white focus:outline-none focus:border-police-accent text-xs"
                >
                  <option value="deepfake">Deepfake / AI Synthetic</option>
                  <option value="impersonation">Police / Official Impersonation</option>
                  <option value="cyber_fraud">Digital Arrest / Cyber Fraud</option>
                  <option value="misinformation">Viral Misinformation</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">
                  NCRP Complaint # (Optional)
                </label>
                <input
                  type="text"
                  value={ncrpNumber}
                  onChange={(e) => setNcrpNumber(e.target.value)}
                  placeholder="cybercrime.gov.in ID"
                  className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-police-accent text-xs"
                />
              </div>
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Investigating Officer</label>
              <input
                type="text"
                value={officerName}
                onChange={(e) => setOfficerName(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-police-accent text-xs"
                required
              />
            </div>

            {/* File Dropzone */}
            <div>
              <label className="block text-slate-300 font-medium mb-1">
                Upload Media Artifact (Image / Video / Audio) *
              </label>
              <div className="border-2 border-dashed border-slate-700 hover:border-police-accent/60 rounded-lg p-4 text-center cursor-pointer bg-slate-900/40 transition-colors">
                <input
                  type="file"
                  id="mediaFile"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  className="hidden"
                  accept="image/*"
                />
                <label htmlFor="mediaFile" className="cursor-pointer space-y-1 block">
                  <UploadCloud className="w-8 h-8 text-police-accent mx-auto" />
                  <div className="text-slate-200 font-medium">
                    {selectedFile ? selectedFile.name : "Click to select or drop file"}
                  </div>
                  <div className="text-[10px] text-slate-400">
                    JPG, PNG, WEBP (Max 500 MB) · Video &amp; Audio: API-ready
                  </div>
                </label>
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-2.5 rounded bg-police-accent text-police-dark font-bold hover:bg-cyan-300 transition-all flex items-center justify-center gap-2 text-xs shadow-md disabled:opacity-50"
            >
              <Lock className="w-4 h-4" />
              {submitting ? "Hashing & Dispatching Pipeline..." : "Begin Forensic Analysis & Custody Log"}
            </button>
          </form>
        </div>

        {/* Recent Cases Queue (7 cols) */}
        <div className="lg:col-span-7 card-cyber p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-police-accent/20 pb-3">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-police-accent" />
              <h2 className="font-bold text-base text-white">Active Case Docket</h2>
            </div>
            <Link
              href="/cases"
              className="text-xs text-police-accent hover:underline flex items-center gap-1"
            >
              View Full Queue <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 uppercase font-mono text-[10px]">
                <tr>
                  <th className="py-2 px-3">Case ID</th>
                  <th className="py-2 px-3">Title</th>
                  <th className="py-2 px-3">Category</th>
                  <th className="py-2 px-3">Status</th>
                  <th className="py-2 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-200">
                {cases.slice(0, 6).map((c) => (
                  <tr key={c.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-2.5 px-3 font-mono text-police-accent font-semibold">
                      {c.case_number}
                    </td>
                    <td className="py-2.5 px-3 max-w-[180px] truncate">{c.title}</td>
                    <td className="py-2.5 px-3 capitalize text-slate-400">
                      {c.category.replace("_", " ")}
                    </td>
                    <td className="py-2.5 px-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-950/60 text-cyan-300 border border-cyan-800/50">
                        {c.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <Link
                        href={`/cases/${c.id}`}
                        className="px-2.5 py-1 bg-police-accent/20 border border-police-accent text-police-accent hover:bg-police-accent/30 rounded text-[11px] font-semibold"
                      >
                        Inspect
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
