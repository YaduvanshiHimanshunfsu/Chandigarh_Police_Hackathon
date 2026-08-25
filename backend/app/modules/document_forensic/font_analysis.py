"""
Document Forensic Module — Font Stroke Width & Text Brightness Consistency Detector.

Detects copy-paste text tampering in documents (marksheets, ID cards, certificates,
affidavits) by measuring stroke width variance and brightness inconsistency across
identified text regions.

Ported and adapted from mobilenetV2/font_check.py — all three sub-functions preserved:
  1. has_sufficient_text()   — gate: skip if no text found (prevents false positives on photos)
  2. get_stroke_widths()     — distance-transform based stroke thickness measurement
  3. get_region_brightness() — background luminance consistency across text regions

Returns PratiBimb-style (score, confidence, details, explanation) tuple.
"""

from typing import Tuple, Dict, Any, List
import numpy as np
import cv2
from PIL import Image


# ── Gate: Does image contain enough text to analyze? ─────────────────────────
def _has_sufficient_text(gray: np.ndarray) -> Tuple[bool, str]:
    """
    Returns (bool, reason). Prevents false positives on natural photos.
    Only runs font analysis on documents with ≥25 text-like contour regions.
    """
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    dark_pixel_ratio = np.sum(binary > 0) / binary.size

    if dark_pixel_ratio < 0.01:
        return False, "Too few dark pixels — no text detected"

    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    text_sized = 0
    widths: List[float] = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect = w / h if h > 0 else 0
        if 5 < w < 200 and 5 < h < 80 and 0.1 < aspect < 10:
            text_sized += 1
            widths.append(float(w))

    if text_sized < 25:
        return False, f"Only {text_sized} text-like regions — not a text document"

    if widths and np.std(widths) > 40:
        return False, f"Edge widths too irregular (std={np.std(widths):.0f}) — natural image"

    return True, f"Found {text_sized} text-like regions"


# ── Stroke width via distance transform ──────────────────────────────────────
def _get_stroke_widths(gray: np.ndarray, text_regions: List[tuple]) -> List[float]:
    """
    Measures average stroke width per text region using distance transform.
    Consistent fonts → small variance. Mixed fonts (tampering) → high variance.
    """
    stroke_widths: List[float] = []
    for (x, y, w, h) in text_regions:
        region = gray[y:y + h, x:x + w]
        if region.size == 0:
            continue
        _, binary = cv2.threshold(region, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        dist = cv2.distanceTransform(binary, cv2.DIST_L2, 3)
        nonzero = dist[dist > 0]
        if len(nonzero) > 5:
            stroke_widths.append(float(np.mean(nonzero)))
    return stroke_widths


# ── Region brightness consistency ─────────────────────────────────────────────
def _get_region_brightness(gray: np.ndarray, text_regions: List[tuple]) -> List[float]:
    """
    Mean pixel brightness per text region.
    Pasted text from a different document has noticeably different brightness.
    """
    return [
        float(np.mean(gray[y:y + h, x:x + w]))
        for (x, y, w, h) in text_regions
        if gray[y:y + h, x:x + w].size > 0
    ]


# ── Main public function ──────────────────────────────────────────────────────
def analyze_document_font_consistency(
    file_path: str,
) -> Tuple[float, float, Dict[str, Any], str]:
    """
    Analyzes font/text inconsistencies for document tampering detection.

    Returns:
        (manipulation_score [0-1], confidence [0-1], details_dict, explanation)

    Graceful no-op on natural images (returns 0.0, 0.50 with skip reason).
    """
    # ── Load image ────────────────────────────────────────────────────────────
    try:
        image = cv2.imread(file_path)
        if image is None:
            pil_img = Image.open(file_path).convert("RGB")
            image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        return 0.0, 0.0, {"error": str(e)}, f"Image load failed: {e}"

    # ── Gate check: does the image have text? ─────────────────────────────────
    has_text, gate_reason = _has_sufficient_text(gray)
    if not has_text:
        return (
            0.0, 0.50,
            {"skipped": True, "reason": gate_reason},
            f"Document font check skipped: {gate_reason}."
        )

    # ── Find text regions via Canny + dilated contours ────────────────────────
    sharpened = cv2.filter2D(gray, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
    edges = cv2.Canny(sharpened, 30, 100)
    dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    text_regions = [
        cv2.boundingRect(c) for c in contours
        if 8 < cv2.boundingRect(c)[2] < 400
        and 8 < cv2.boundingRect(c)[3] < 120
        and 0.2 < (cv2.boundingRect(c)[2] / max(cv2.boundingRect(c)[3], 1)) < 15
    ]

    if len(text_regions) < 5:
        return (
            0.0, 0.50,
            {"skipped": True, "reason": f"Too few text regions ({len(text_regions)}) for comparison"},
            "Too few text regions — font analysis inconclusive."
        )

    # ── Measure stroke widths ─────────────────────────────────────────────────
    stroke_widths = _get_stroke_widths(gray, text_regions)
    if len(stroke_widths) < 5:
        return (
            0.0, 0.50,
            {"skipped": True, "reason": "Could not measure stroke widths"},
            "Stroke width measurement failed — font analysis inconclusive."
        )

    avg_stroke = float(np.mean(stroke_widths))
    std_stroke = float(np.std(stroke_widths))
    inconsistent_count = sum(1 for s in stroke_widths if abs(s - avg_stroke) > std_stroke * 2)

    # ── Measure brightness consistency ────────────────────────────────────────
    brightness_vals = _get_region_brightness(gray, text_regions)
    brightness_std = float(np.std(brightness_vals)) if brightness_vals else 0.0

    # ── Score accumulation (mirrors font_check.py calibrated thresholds) ─────
    score = 0.0

    # Stroke variance component (0–0.50)
    if std_stroke > 3.0:
        score += 0.50
    elif std_stroke > 1.5:
        score += 0.25
    elif std_stroke > 0.5:
        score += 0.10

    # Inconsistent region count (0–0.30)
    if inconsistent_count > 8:
        score += 0.30
    elif inconsistent_count > 3:
        score += 0.15

    # Brightness inconsistency (0–0.20)
    if brightness_std > 25:
        score += 0.20
    elif brightness_std > 10:
        score += 0.10

    manipulation_score = float(np.clip(score, 0.0, 1.0))

    # Confidence scales with how many text regions we found
    confidence = 0.85 if len(text_regions) > 50 else (0.75 if len(text_regions) > 20 else 0.60)

    details = {
        "has_text": True,
        "text_regions_found": len(text_regions),
        "average_stroke_width": round(avg_stroke, 2),
        "stroke_std": round(std_stroke, 2),
        "inconsistent_regions": inconsistent_count,
        "brightness_std": round(brightness_std, 2),
        "gate_reason": gate_reason,
    }

    if manipulation_score >= 0.60:
        explanation = (
            f"High document font inconsistency: stroke std={std_stroke:.2f}, "
            f"{inconsistent_count} outlier region(s), brightness std={brightness_std:.1f}. "
            f"Likely copy-paste text tampering (e.g. grade/mark alteration)."
        )
    elif manipulation_score >= 0.30:
        explanation = (
            f"Moderate font variance: stroke std={std_stroke:.2f} across "
            f"{len(text_regions)} text regions. Possible partial text alteration."
        )
    else:
        explanation = (
            f"Font strokes consistent across {len(text_regions)} text regions "
            f"(stroke std={std_stroke:.2f}, brightness std={brightness_std:.1f}). "
            f"Document appears unmodified."
        )

    return manipulation_score, confidence, details, explanation
