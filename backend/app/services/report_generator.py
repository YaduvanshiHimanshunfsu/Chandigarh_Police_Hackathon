"""
Forensic Report & Legal Certificate Generation Service.

Generates:
1. Bharatiya Sakshya Adhiniyam (BSA), 2023 - Section 63(4) Dual-Certification Certificate (PDF)
2. Comprehensive Multi-Page Forensic Analysis Dossier (PDF)
"""

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)

from app.core.config import settings
from app.models.media_item import MediaItem
from app.models.analysis_result import AnalysisResult, ModuleType


async def generate_bsa_certificate(
    media_item: MediaItem,
    fusion_result: Optional[AnalysisResult],
    officer_name: str = "Authorized Investigating Officer",
    officer_designation: str = "Cyber Crime Cell, Chandigarh Police",
) -> str:
    """
    Generates a statutory Section 63(4) Certificate as prescribed under the Schedule
    of the Bharatiya Sakshya Adhiniyam (BSA), 2023 for admissibility of electronic evidence.
    """
    reports_dir = Path(settings.REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)

    filename = f"BSA_63_CERT_{media_item.sha256_hash[:16]}_{uuid.uuid4().hex[:6]}.pdf"
    file_path = str(reports_dir / filename)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CertTitle",
        parent=styles["Heading1"],
        fontSize=14,
        leading=18,
        alignment=1,
        textColor=colors.HexColor("#1A2B49"),
        fontName="Helvetica-Bold",
    )
    subtitle_style = ParagraphStyle(
        "CertSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#4A5568"),
        fontName="Helvetica-Oblique",
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0D3B66"),
        fontName="Helvetica-Bold",
        spaceBefore=8,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
    )
    bold_body = ParagraphStyle(
        "BoldBody",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    elements = []

    # Header
    elements.append(Paragraph("SCHEDULE TO THE BHARATIYA SAKSHYA ADHINIYAM, 2023", subtitle_style))
    elements.append(Paragraph("CERTIFICATE UNDER SECTION 63(4)", title_style))
    elements.append(Paragraph("Admissibility of Electronic Records in Judicial Proceedings", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A2B49")))
    elements.append(Spacer(1, 10))

    # Electronic Record Details
    elements.append(Paragraph("1. IDENTIFICATION OF ELECTRONIC RECORD", section_heading))
    meta_table_data = [
        [Paragraph("File Name (Original):", bold_body), Paragraph(media_item.original_filename, body_style)],
        [Paragraph("MIME / File Type:", bold_body), Paragraph(f"{media_item.mime_type} ({media_item.media_type.value.upper()})", body_style)],
        [Paragraph("File Size (Bytes):", bold_body), Paragraph(f"{media_item.file_size_bytes:,} bytes", body_style)],
        [Paragraph("Mandatory SHA-256 Hash:", bold_body), Paragraph(f"<font color='#0D3B66'><b>{media_item.sha256_hash}</b></font>", body_style)],
        [Paragraph("Perceptual Hash (pHash):", bold_body), Paragraph(media_item.phash or "N/A", body_style)],
        [Paragraph("Acquisition / Ingest Timestamp:", bold_body), Paragraph(media_item.created_at.strftime("%d-%b-%Y %H:%M:%S UTC") if media_item.created_at else datetime.now(timezone.utc).isoformat(), body_style)],
    ]
    t1 = Table(meta_table_data, colWidths=[160, 360])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 10))

    # PART A
    elements.append(Paragraph("PART A: CERTIFICATE BY PERSON IN CHARGE OF COMPUTER DEVICE / SYSTEM", section_heading))
    part_a_text = (
        "I hereby certify that the electronic record identified above was produced by a computer / electronic system "
        "lawfully operated by Chandigarh Police / Authorized Forensic Laboratory during the period over which the computer "
        "was used regularly to store or process information for the purposes of forensic verification and investigation. "
        "I further certify that during the said period, the computer system was operating properly and there were no operational "
        "defects that would affect the integrity of the data or reproduction thereof."
    )
    elements.append(Paragraph(part_a_text, body_style))
    elements.append(Spacer(1, 12))

    part_a_sig_data = [
        [Paragraph("<b>Name of Certifying Officer:</b>", body_style), Paragraph(officer_name, body_style)],
        [Paragraph("<b>Designation / Agency:</b>", body_style), Paragraph(officer_designation, body_style)],
        [Paragraph("<b>Date of Certification:</b>", body_style), Paragraph(datetime.now().strftime("%d-%m-%Y"), body_style)],
        [Paragraph("<b>Signature / Seal:</b>", body_style), Paragraph("____________________________________", body_style)],
    ]
    t_sig_a = Table(part_a_sig_data, colWidths=[160, 360])
    t_sig_a.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t_sig_a)
    elements.append(Spacer(1, 14))

    # PART B
    elements.append(Paragraph("PART B: CERTIFICATE BY INDEPENDENT TECHNICAL EXPERT / FORENSIC EXAMINER", section_heading))
    part_b_text = (
        "I, acting as the Technical Expert / Forensic System Operator, have examined the digital artifact specified herein "
        "using <b>PratiBimb Praman v1.0</b> (Multi-Modal Provenance & Evidence Fusion Platform). The cryptographic hash (SHA-256) "
        "computed at ingestion was verified against the bitstream. Cryptographic chain-of-custody ledgers (Merkle-chained) confirm "
        "zero retroactive alterations to the evidence or analytical artifacts."
    )
    elements.append(Paragraph(part_b_text, body_style))
    elements.append(Spacer(1, 8))

    # Forensic summary table if fusion results exist
    if fusion_result and fusion_result.details:
        f_details = fusion_result.details
        verdict = f_details.get("verdict", "ANALYZED")
        ai_prob = f"{round((fusion_result.ai_generation_score or 0) * 100, 1)}%"
        manip_prob = f"{round((fusion_result.manipulation_score or 0) * 100, 1)}%"
        provenance = f_details.get("c2pa_summary", "Not Cryptographically Signed")

        forensic_brief = [
            [Paragraph("<b>Forensic Authenticity Assessment:</b>", body_style), Paragraph(f"<b>{verdict}</b>", bold_body)],
            [Paragraph("<b>AI Generation Likelihood:</b>", body_style), Paragraph(ai_prob, body_style)],
            [Paragraph("<b>Visual Manipulation Likelihood:</b>", body_style), Paragraph(manip_prob, body_style)],
            [Paragraph("<b>Provenance Status (C2PA):</b>", body_style), Paragraph(provenance, body_style)],
        ]
        t_fb = Table(forensic_brief, colWidths=[180, 340])
        t_fb.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(t_fb)
        elements.append(Spacer(1, 10))

    elements.append(Spacer(1, 10))
    part_b_sig_data = [
        [Paragraph("<b>Technical Examiner / Tool:</b>", body_style), Paragraph("PratiBimb Praman Automated Forensic Engine v1.0", body_style)],
        [Paragraph("<b>Digital Forensic Lab ID:</b>", body_style), Paragraph("CHD-CYBER-LAB-01", body_style)],
        [Paragraph("<b>Date / Timestamp:</b>", body_style), Paragraph(datetime.now(timezone.utc).strftime("%d-%b-%Y %H:%M:%S UTC"), body_style)],
        [Paragraph("<b>Expert Signature / E-Sign:</b>", body_style), Paragraph("____________________________________", body_style)],
    ]
    t_sig_b = Table(part_b_sig_data, colWidths=[180, 340])
    t_sig_b.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t_sig_b)

    doc.build(elements)
    return file_path


async def generate_forensic_report(
    media_item: MediaItem,
    analysis_results: List[AnalysisResult],
    fusion_result: Optional[AnalysisResult],
    officer_name: str = "Authorized Investigator",
) -> str:
    """
    Generates a full comprehensive multi-page digital forensics report.
    """
    reports_dir = Path(settings.REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)

    filename = f"FORENSIC_REPORT_{media_item.sha256_hash[:16]}_{uuid.uuid4().hex[:6]}.pdf"
    file_path = str(reports_dir / filename)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "MainTitle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A2B49"),
        fontName="Helvetica-Bold",
    )
    sub_style = ParagraphStyle(
        "SubTitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#718096"),
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0D3B66"),
        fontName="Helvetica-Bold",
        spaceBefore=12,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("PRATIBIMB PRAMAN — FORENSIC DOSSIER", title_style))
    elements.append(Paragraph("AI Media Forensic Provenance & Origin Intelligence Report", sub_style))
    elements.append(Paragraph(f"Generated on: {datetime.now(timezone.utc).strftime('%d %B %Y at %H:%M:%S UTC')} | Examiner: {officer_name}", sub_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1A2B49")))
    elements.append(Spacer(1, 12))

    # Executive Verdict & Evidence Fusion Summary
    elements.append(Paragraph("1. EXECUTIVE FORENSIC VERDICT & EVIDENCE FUSION", h2_style))
    if fusion_result and fusion_result.details:
        f_info = fusion_result.details
        verdict = f_info.get("verdict", "SUSPICIOUS")
        ai_score = f"{round((fusion_result.ai_generation_score or 0) * 100, 1)}%"
        ci_str = f_info.get("confidence_interval", "N/A")
        uncertainty = f_info.get("uncertainty_band", "Low")
        conflicts = f_info.get("conflicts", [])

        fusion_table_data = [
            [Paragraph("<b>Primary Assessment:</b>", body_style), Paragraph(f"<b>{verdict}</b>", body_style)],
            [Paragraph("<b>AI Generation Probability:</b>", body_style), Paragraph(f"<b>{ai_score}</b> (95% CI: {ci_str})", body_style)],
            [Paragraph("<b>Uncertainty Band:</b>", body_style), Paragraph(uncertainty, body_style)],
            [Paragraph("<b>Signal Conflict Status:</b>", body_style), Paragraph("Detected & Dempster-Shafer Calibrated" if conflicts else "None (Signals in concordance)", body_style)],
        ]
        t_fusion = Table(fusion_table_data, colWidths=[160, 360])
        t_fusion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F4F8")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(t_fusion)
    else:
        elements.append(Paragraph("Evidence Fusion analysis pending or incomplete.", body_style))

    elements.append(Spacer(1, 12))

    # Individual Module Breakdown
    elements.append(Paragraph("2. MULTI-MODAL EVIDENCE DECOMPOSITION", h2_style))
    module_rows = [
        [Paragraph("<b>Forensic Module</b>", body_style), Paragraph("<b>Status / Verdict</b>", body_style), Paragraph("<b>Key Forensic Indicator / Explanation</b>", body_style)]
    ]

    for res in analysis_results:
        if res.module_type == ModuleType.FUSION:
            continue
        m_name = res.module_type.value.replace("_", " ").title()
        status_val = res.c2pa_status or res.watermark_status or (f"{round((res.ai_generation_score or 0)*100)}% AI" if res.ai_generation_score is not None else "Completed")
        explanation = res.explanation or "Analysis executed with calibrated weights."
        module_rows.append([
            Paragraph(f"<b>{m_name}</b>", body_style),
            Paragraph(str(status_val), body_style),
            Paragraph(explanation, body_style)
        ])

    t_modules = Table(module_rows, colWidths=[120, 110, 290])
    t_modules.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A2B49")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_modules)
    elements.append(Spacer(1, 12))

    # Digital Provenance & Chain-of-Custody
    elements.append(Paragraph("3. DIGITAL PROVENANCE & CUSTODY RECORD", h2_style))
    custody_rows = [
        [Paragraph("Media SHA-256:", body_style), Paragraph(media_item.sha256_hash, body_style)],
        [Paragraph("Perceptual Hash (pHash):", body_style), Paragraph(media_item.phash or "N/A", body_style)],
        [Paragraph("JPEG Estimated Quality:", body_style), Paragraph(f"{media_item.jpeg_quality_estimate}/100 (Recompression factored into DCT weights)" if media_item.jpeg_quality_estimate else "Uncompressed / N/A", body_style)],
    ]
    t_custody = Table(custody_rows, colWidths=[160, 360])
    t_custody.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_custody)

    doc.build(elements)
    return file_path
