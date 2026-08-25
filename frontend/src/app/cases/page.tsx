"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { FileText, Search, Filter, Plus, ArrowLeft } from "lucide-react";
import { fetchCases, CaseData } from "@/lib/api";

export default function CasesQueuePage() {
  const [cases, setCases] = useState<CaseData[]>([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    fetchCases().then(setCases).catch(console.error);
  }, []);

  const filteredCases = cases.filter((c) => {
    const matchesSearch =
      c.case_number.toLowerCase().includes(search.toLowerCase()) ||
      c.title.toLowerCase().includes(search.toLowerCase()) ||
      c.officer_name.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = statusFilter === "all" || c.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-police-accent/20 pb-4">
        <div>
          <Link
            href="/"
            className="text-xs text-police-accent hover:underline flex items-center gap-1 mb-1"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Dashboard
          </Link>
          <h1 className="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
            <FileText className="w-6 h-6 text-police-accent" />
            <span>Forensic Case Queue & Investigation Docket</span>
          </h1>
          <div className="text-xs text-slate-400 mt-0.5">
            Manage, triage, and inspect deepfake / cyber fraud cases
          </div>
        </div>

        <Link
          href="/#intake"
          className="px-4 py-2 bg-police-accent text-police-dark font-bold rounded text-xs flex items-center gap-1.5 hover:bg-cyan-300 transition-colors shadow-md self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" /> New Case Intake
        </Link>
      </div>

      {/* Filter / Search Bar */}
      <div className="card-cyber p-4 flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by Case ID, Title, Officer..."
            className="w-full bg-slate-900 border border-slate-700 rounded-md pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:border-police-accent"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-md px-3 py-2 text-xs text-white focus:outline-none focus:border-police-accent"
          >
            <option value="all">All Statuses</option>
            <option value="draft">Draft</option>
            <option value="analyzing">Analyzing</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="card-cyber p-4 overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-900/80 text-slate-400 uppercase font-mono text-[10px]">
            <tr>
              <th className="py-2.5 px-3">Case ID</th>
              <th className="py-2.5 px-3">Case Title</th>
              <th className="py-2.5 px-3">Category</th>
              <th className="py-2.5 px-3">Officer</th>
              <th className="py-2.5 px-3">Priority</th>
              <th className="py-2.5 px-3">Status</th>
              <th className="py-2.5 px-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-slate-200">
            {filteredCases.map((c) => (
              <tr key={c.id} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3 px-3 font-mono text-police-accent font-semibold">
                  {c.case_number}
                </td>
                <td className="py-3 px-3 max-w-[200px] truncate font-medium text-white">
                  {c.title}
                </td>
                <td className="py-3 px-3 capitalize text-slate-300">
                  {c.category.replace("_", " ")}
                </td>
                <td className="py-3 px-3 text-slate-300">{c.officer_name}</td>
                <td className="py-3 px-3">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-mono uppercase ${
                      c.priority === "critical"
                        ? "bg-rose-950 text-rose-300 border border-rose-800"
                        : "bg-amber-950 text-amber-300 border border-amber-800"
                    }`}
                  >
                    {c.priority}
                  </span>
                </td>
                <td className="py-3 px-3">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-950/80 text-cyan-300 border border-cyan-800/60">
                    {c.status.toUpperCase()}
                  </span>
                </td>
                <td className="py-3 px-3 text-right">
                  <Link
                    href={`/cases/${c.id}`}
                    className="px-3 py-1 bg-police-accent/20 border border-police-accent text-police-accent hover:bg-police-accent/30 rounded text-xs font-semibold"
                  >
                    Inspect Dossier
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
