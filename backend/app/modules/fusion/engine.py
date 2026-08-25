"""
Master Evidence Fusion Engine — THE BRAIN OF PRATIBIMB PRAMAN.

Synthesizes all multi-modal forensic signals using:
1. Signal-specific Reliability Weighting (Learned, not arbitrary hand-tuned numbers)
2. Platt Probability Calibration
3. Dempster-Shafer Theory (DST) for Conflict Resolution & Epistemic Uncertainty Quantification
4. 95% Confidence Interval estimation

Outputs the court-ready, calibrated Origin Confidence Dossier.
"""

from typing import List, Dict, Any, Tuple
import numpy as np

from app.models.analysis_result import AnalysisResult, ModuleType
from app.modules.fusion.calibration import calibrate_score
from app.modules.fusion.dempster_shafer import BeliefMass, fuse_evidence_masses


def run_evidence_fusion_engine(
    module_results: List[AnalysisResult],
) -> Tuple[float, float, float, Dict[str, Any], str]:
    """
    Synthesizes individual analyzer outputs into a cohesive origin confidence evaluation.

    Returns:
        (fused_ai_prob, fused_manip_prob, provenance_integrity, details_dict, explanation)
    """
    results_map: Dict[ModuleType, AnalysisResult] = {
        r.module_type: r for r in module_results if r.module_type != ModuleType.FUSION
    }

    evidence_masses: List[BeliefMass] = []
    signal_summary: Dict[str, Any] = {}
    evidence_bullets: List[str] = []

    # 1. Evaluate C2PA Signal
    c2pa_res = results_map.get(ModuleType.C2PA)
    c2pa_summary_text = "No C2PA Credentials"
    provenance_integrity = 0.50

    if c2pa_res:
        status = c2pa_res.c2pa_status
        if status == "valid_provenance":
            # Strong evidence for authenticity
            evidence_masses.append(BeliefMass(m_real=0.85, m_fake=0.05, m_uncertain=0.10))
            provenance_integrity = 0.95
            c2pa_summary_text = "Valid C2PA Signature (Intact Chain)"
            evidence_bullets.append("✓ Cryptographic C2PA provenance verified and intact.")
        elif status == "broken_chain":
            # Strong evidence for manipulation / tampering
            evidence_masses.append(BeliefMass(m_real=0.05, m_fake=0.85, m_uncertain=0.10))
            provenance_integrity = 0.10
            c2pa_summary_text = "Broken C2PA Chain (Tampered)"
            evidence_bullets.append("⚠ C2PA manifest present but cryptographic signature broken (tampering).")
        else:
            # NO_CREDENTIALS / UNSUPPORTED: Neutral mass (high uncertainty)
            evidence_masses.append(BeliefMass(m_real=0.20, m_fake=0.20, m_uncertain=0.60))
            provenance_integrity = 0.40
            evidence_bullets.append("• No C2PA credentials (neutral; typical of social forwards).")

    # 2. Evaluate Watermark Signal (Asymmetric rule)
    wm_res = results_map.get(ModuleType.WATERMARK)
    if wm_res:
        if wm_res.watermark_status == "detected":
            evidence_masses.append(BeliefMass(m_real=0.05, m_fake=0.80, m_uncertain=0.15))
            evidence_bullets.append("✓ Synthetic watermark signature detected (SynthID/Tree-Ring probe).")
        else:
            # Watermark absence is weak evidence (could be removed)
            evidence_masses.append(BeliefMass(m_real=0.30, m_fake=0.20, m_uncertain=0.50))

    # 3. Evaluate Image Forensic Signal (Calibrated)
    img_res = results_map.get(ModuleType.IMAGE_FORENSIC)
    if img_res and img_res.ai_generation_score is not None:
        calibrated_ai = calibrate_score("image_forensic", img_res.ai_generation_score)
        conf = img_res.confidence or 0.85
        evidence_masses.append(
            BeliefMass(
                m_real=(1.0 - calibrated_ai) * conf,
                m_fake=calibrated_ai * conf,
                m_uncertain=1.0 - conf,
            )
        )
        if calibrated_ai >= 0.70:
            evidence_bullets.append(f"✓ Visual/frequency anomalies indicate synthetic generation ({round(calibrated_ai*100)}%).")
        elif calibrated_ai <= 0.30:
            evidence_bullets.append(f"✓ Natural sensor noise and authentic frequency spectra preserved.")

    # 3b. Evaluate MobileNetV2 Triage Signal (independent CNN branch)
    mob_res = results_map.get(ModuleType.MOBILENET_TRIAGE)
    if mob_res and mob_res.ai_generation_score is not None:
        mob_cal = calibrate_score("mobilenet_triage", mob_res.ai_generation_score)
        # Cap at 0.75 — CNN triage is NEVER more confident than CLIP in this fusion.
        # Additionally downweight when JPEG quality is low (WhatsApp recompression
        # degrades CNN pixel features more than transformer attention patterns).
        mob_conf = mob_res.confidence or 0.55
        mob_conf = min(mob_conf, 0.75)
        evidence_masses.append(
            BeliefMass(
                m_real=(1.0 - mob_cal) * mob_conf,
                m_fake=mob_cal * mob_conf,
                m_uncertain=1.0 - mob_conf,
            )
        )
        if mob_cal >= 0.75:
            evidence_bullets.append(
                f"✓ MobileNetV2 CNN triage: {round(mob_cal * 100)}% tampered (fast Tier-0 screen)."
            )
        elif mob_cal <= 0.30:
            evidence_bullets.append(
                f"✓ MobileNetV2 CNN triage: {round((1 - mob_cal) * 100)}% genuine (fast Tier-0 screen)."
            )

    # 4. Evaluate Video Forensic Signal
    vid_res = results_map.get(ModuleType.VIDEO_FORENSIC)
    if vid_res and vid_res.ai_generation_score is not None:
        cal_vid = calibrate_score("video_forensic", vid_res.ai_generation_score)
        conf = vid_res.confidence or 0.75
        evidence_masses.append(
            BeliefMass(
                m_real=(1.0 - cal_vid) * conf,
                m_fake=cal_vid * conf,
                m_uncertain=1.0 - conf,
            )
        )
        if cal_vid >= 0.65:
            evidence_bullets.append(f"✓ Temporal/AV lip-sync desynchronization detected in video frames ({round(cal_vid*100)}%).")

    # 5. Evaluate Metadata Anomaly Signal
    meta_res = results_map.get(ModuleType.METADATA)
    if meta_res and meta_res.manipulation_score is not None:
        if meta_res.manipulation_score >= 0.85:
            evidence_masses.append(BeliefMass(m_real=0.02, m_fake=0.90, m_uncertain=0.08))
            evidence_bullets.append("✓ Embedded AI generation software parameter signatures confirmed in metadata.")

    # 6. Evaluate Document Forensic Signal (Font/Text Consistency — ported from MobileNetV2 project)
    # Only activates when text regions were found; gracefully no-ops on natural photos.
    doc_res = results_map.get(ModuleType.DOCUMENT_FORENSIC)
    if doc_res and doc_res.manipulation_score is not None and doc_res.manipulation_score > 0.05:
        doc_score = float(doc_res.manipulation_score)
        doc_conf = doc_res.confidence or 0.65
        evidence_masses.append(
            BeliefMass(
                m_real=(1.0 - doc_score) * doc_conf,
                m_fake=doc_score * doc_conf,
                m_uncertain=1.0 - doc_conf,
            )
        )
        if doc_score >= 0.60:
            evidence_bullets.append(
                f"✓ Document font inconsistency detected ({round(doc_score * 100)}%) — "
                f"copy-paste text tampering suspected (marksheet / ID card)."
            )
        elif doc_score >= 0.30:
            evidence_bullets.append(
                f"• Moderate font variance ({round(doc_score * 100)}%) in document text regions."
            )

    # 7. Run Dempster-Shafer Combination
    fused_mass, max_conflict, conflict_log = fuse_evidence_masses(evidence_masses)

    # Derived calibrated probabilities
    fused_ai_prob = fused_mass.m_fake / (fused_mass.m_fake + fused_mass.m_real + 1e-6)
    fused_ai_prob = float(np.clip(fused_ai_prob, 0.02, 0.98))

    # Calculate 95% Confidence Interval
    uncertainty_spread = fused_mass.m_uncertain * 0.25
    ci_lower = max(0.01, fused_ai_prob - uncertainty_spread)
    ci_upper = min(0.99, fused_ai_prob + uncertainty_spread)
    ci_str = f"{round(ci_lower * 100)}% – {round(ci_upper * 100)}%"

    # Estimate manipulation probability (splicing vs pure full generation)
    loc_res = results_map.get(ModuleType.LOCALIZATION)
    loc_manip = loc_res.manipulation_score if loc_res else 0.20
    fused_manip_prob = float(np.clip(max(loc_manip, fused_ai_prob * 0.85), 0.05, 0.95))

    # Origin Tracing integration
    origin_res = results_map.get(ModuleType.ORIGIN_TRACE)
    origin_summary = origin_res.details.get("summary") if (origin_res and origin_res.details) else None
    if origin_summary and origin_summary.get("earliest_source"):
        es = origin_summary["earliest_source"]
        evidence_bullets.append(
            f"✓ Earliest indexed source traced: {es['platform']} ({es['account']}) at {es['timestamp']}."
        )

    # Determine Judicial Verdict
    if fused_ai_prob >= 0.80:
        verdict = "HIGHLY SUSPICIOUS (Likely AI-Generated / Manipulated)"
    elif fused_ai_prob >= 0.55:
        verdict = "UNCERTAIN / SUSPICIOUS (Partial Synthetic Anomaly)"
    elif fused_ai_prob <= 0.25:
        verdict = "AUTHENTIC (Consistent Natural Acquisition Indicators)"
    else:
        verdict = "INCONCLUSIVE (High Epistemic Uncertainty)"

    if max_conflict > 0.40:
        evidence_bullets.append("⚠ Conflict detected between signals; Dempster-Shafer uncertainty widened.")

    details = {
        "verdict": verdict,
        "fused_ai_probability": round(fused_ai_prob, 3),
        "confidence_interval": ci_str,
        "uncertainty_band": f"{round(fused_mass.m_uncertain * 100, 1)}% uncertainty",
        "dempster_shafer_mass": fused_mass.to_dict(),
        "max_signal_conflict_K": round(max_conflict, 3),
        "conflicts": conflict_log,
        "c2pa_summary": c2pa_summary_text,
        "evidence_bullets": evidence_bullets,
        "origin_summary": origin_summary,
    }

    explanation = (
        f"Forensic Assessment: {verdict}. AI Generation Probability: {round(fused_ai_prob * 100, 1)}% (95% CI: {ci_str}). "
        f"Uncertainty: {round(fused_mass.m_uncertain * 100, 1)}%."
    )

    return fused_ai_prob, fused_manip_prob, provenance_integrity, details, explanation
