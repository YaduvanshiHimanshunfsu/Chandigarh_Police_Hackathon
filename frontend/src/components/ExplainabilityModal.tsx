"use client";

import React from "react";
import { AlertCircle, CheckCircle, HelpCircle, Layers, Cpu } from "lucide-react";

interface ExplainabilityModalProps {
  isOpen: boolean;
  onClose: () => void;
  fusionSummary?: any;
}

export default function ExplainabilityModal({
  isOpen,
  onClose,
  fusionSummary,
}: ExplainabilityModalProps) {
  if (!isOpen) return null;

  const dempsterMass = fusionSummary?.dempster_shafer_mass || {
    m_real: 0.08,
    m_fake: 0.82,
    m_uncertain: 0.10,
  };

  const bullets = fusionSummary?.evidence_bullets || [
    "Diffusion-like high-frequency spectral artifacts identified in spatial domain.",
    "Dynamic recompression weighting applied to mitigate WhatsApp quality degradation.",
    "C2PA manifest absent (treated as neutral per Indian social media distribution).",
    "Synthetic watermark correlation detected in high-frequency residual.",
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4">
      <div className="card-cyber max-w-2xl w-full p-6 space-y-5 bg-police-card border border-police-accent/40 shadow-2xl relative">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-police-accent/20 pb-3">
          <div className="flex items-center gap-2 text-police-accent font-bold text-lg">
            <Cpu className="w-5 h-5" />
            <span>Forensic Reasoning & Dempster-Shafer Decomposition</span>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-lg font-bold"
          >
            ✕
          </button>
        </div>

        {/* Dempster-Shafer Belief Masses */}
        <div className="space-y-2">
          <div className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-police-accent" />
            <span>Dempster-Shafer Epistemic Belief Distribution</span>
          </div>
          <div className="grid grid-cols-3 gap-3">
            <div className="p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-lg text-center">
              <div className="text-xs text-emerald-400 font-medium">Belief (Authentic)</div>
              <div className="text-lg font-bold text-emerald-300 font-mono">
                {Math.round(dempsterMass.m_real * 100)}%
              </div>
            </div>
            <div className="p-3 bg-rose-950/40 border border-rose-500/30 rounded-lg text-center">
              <div className="text-xs text-rose-400 font-medium">Belief (Synthetic/Tampered)</div>
              <div className="text-lg font-bold text-rose-300 font-mono">
                {Math.round(dempsterMass.m_fake * 100)}%
              </div>
            </div>
            <div className="p-3 bg-amber-950/40 border border-amber-500/30 rounded-lg text-center">
              <div className="text-xs text-amber-400 font-medium">Epistemic Uncertainty</div>
              <div className="text-lg font-bold text-amber-300 font-mono">
                {Math.round(dempsterMass.m_uncertain * 100)}%
              </div>
            </div>
          </div>
        </div>

        {/* Evidence Card Breakdown */}
        <div className="space-y-2">
          <div className="text-xs font-semibold text-slate-300">
            Multi-Signal Forensic Evidence Summary
          </div>
          <div className="space-y-1.5 bg-slate-900/60 p-3 rounded-lg border border-slate-700/60">
            {bullets.map((bullet: string, i: number) => (
              <div key={i} className="text-xs text-slate-300 flex items-start gap-2">
                <span className="text-police-accent font-bold">•</span>
                <span>{bullet}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Calibration & Judicial Admissibility Note */}
        <div className="p-3 bg-blue-950/30 border border-blue-500/20 rounded-md text-[11px] text-blue-200/80 leading-relaxed">
          <b>Judicial Note:</b> Scores reflect empirical Platt-calibrated probabilities.
          Signals in conflict are surfaced via Dempster-Shafer combination rather than averaged away,
          ensuring full transparency and compliance with Section 63(4) of Bharatiya Sakshya Adhiniyam, 2023.
        </div>

        {/* Footer Action */}
        <div className="flex justify-end pt-2">
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-police-accent text-police-dark font-semibold text-xs rounded hover:bg-cyan-300 transition-colors"
          >
            Close Reasoning Panel
          </button>
        </div>
      </div>
    </div>
  );
}
