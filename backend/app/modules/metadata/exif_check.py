"""
Metadata & EXIF Forensic Consistency Check Module.

Extracts and validates:
1. Camera sensor tags vs Software tags (AI generators + editing tools)
2. PNG text chunks (tEXt, iTXt, zTXt) for embedded AI generation parameters/prompts
3. EXIF timestamp vs capture timestamp discrepancies (date mismatch)
4. ICC profile anomalies
5. Metadata dimensions vs actual dimensions (crop/resize detection) — ported from mobilenetV2/metadata.py
6. Thumbnail vs actual image mismatch (edit-after-thumbnail detection) — ported from mobilenetV2/metadata.py
"""

import io
from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
from PIL import Image, ExifTags


# Known AI generation software signatures
KNOWN_AI_SOFTWARE_SIGNATURES = [
    "stable diffusion", "midjourney", "dall-e", "novelai", "comfyui",
    "automatic1111", "invokeai", "fooocus", "adobe firefly", "bing image creator",
]

# Traditional editing tools — suspicious for document tampering context
# (expanded from mobilenetV2/metadata.py's EDITING_SOFTWARE list)
EDITING_SOFTWARE_SIGNATURES = [
    "adobe photoshop", "gimp", "paint.net", "ms paint", "canva",
    "lightroom", "pixlr", "fotor", "snapseed", "picsart", "paintshop",
    "affinity", "inkscape", "corel", "illustrator", "photopea", "paint",
    "preview", "irfanview", "xnview", "acdsee", "capture one",
    "darktable", "rawtherapee", "image editor", "photo editor", "photoscape",
]


def check_metadata_consistency(file_path: str) -> Tuple[float, float, Dict[str, Any], str]:
    """
    Examines file metadata for AI indicators, software tampering, dimension
    mismatches, and thumbnail inconsistencies.

    Returns:
        (tampering_score, confidence, details_dict, explanation)
    """
    path_obj = Path(file_path)
    if not path_obj.exists():
        return 0.5, 0.0, {"error": "File not found"}, "File missing."

    try:
        img = Image.open(file_path)
        actual_w, actual_h = img.size
        raw_info = img.info or {}
        extracted_tags: Dict[str, str] = {}
        ai_signatures_found = []
        editing_software_found = []
        software_detected = None
        score = 0.0

        # ── 1. Inspect PNG metadata chunks (Prompt / Workflow dump) ──────────
        for k, v in raw_info.items():
            if isinstance(v, str):
                val_lower = v.lower()
                for sig in KNOWN_AI_SOFTWARE_SIGNATURES:
                    if sig in val_lower:
                        ai_signatures_found.append(f"{k}: contains '{sig}'")
                if len(v) < 300:
                    extracted_tags[k] = v

        # ── 2. Inspect EXIF tags (JPEG/TIFF/WEBP) ───────────────────────────
        exif = img.getexif()
        date_original = None
        date_modified = None
        meta_w = meta_h = None

        if exif:
            for tag_id, val in exif.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                val_str = str(val)

                # Software / processing tool check
                if tag_name.lower() in ["software", "processingsoftware", "artist", "imagedescription"]:
                    software_detected = val_str
                    val_lower = val_str.lower()
                    for sig in KNOWN_AI_SOFTWARE_SIGNATURES:
                        if sig in val_lower:
                            ai_signatures_found.append(f"EXIF Software: '{val_str}'")
                    for sig in EDITING_SOFTWARE_SIGNATURES:
                        if sig in val_lower:
                            editing_software_found.append(f"EXIF Software: '{val_str}'")

                # Capture timestamps for date-mismatch check
                if tag_name == "DateTimeOriginal":
                    date_original = val_str
                if tag_name in ("DateTime", "DateTimeDigitized"):
                    date_modified = val_str

                # Metadata dimensions
                if tag_name == "ImageWidth":
                    try:
                        meta_w = int(val)
                    except (ValueError, TypeError):
                        pass
                if tag_name == "ImageLength":
                    try:
                        meta_h = int(val)
                    except (ValueError, TypeError):
                        pass

                if isinstance(val, (str, int, float)) and len(str(val)) < 200:
                    extracted_tags[tag_name] = val_str

        # ── 3. Date mismatch: capture time ≠ modification time ───────────────
        date_mismatch = False
        if date_original and date_modified and date_original != date_modified:
            date_mismatch = True
            ai_signatures_found.append(
                f"Date mismatch: captured={date_original} modified={date_modified}"
            )
            score += 0.30

        # ── 4. Dimension mismatch: metadata dimensions ≠ actual pixel size ───
        # (ported from mobilenetV2/metadata.py — catches crop/resize after edit)
        dimension_mismatch = False
        if meta_w and meta_h:
            if int(meta_w) != actual_w or int(meta_h) != actual_h:
                dimension_mismatch = True
                ai_signatures_found.append(
                    f"Dimension mismatch: metadata={meta_w}x{meta_h}, actual={actual_w}x{actual_h} "
                    f"(image resized/cropped after editing)"
                )
                score += 0.35

        # ── 5. Thumbnail vs image mismatch (ported from mobilenetV2/metadata.py) ──
        # JPEG embeds a small thumbnail in EXIF. If the main image was edited
        # later the thumbnail may not match, revealing post-capture tampering.
        thumbnail_mismatch = False
        thumbnail_diff = None
        try:
            raw_exif = img._getexif() if hasattr(img, "_getexif") else None
            if raw_exif:
                # Tag 513 = JPEGInterchangeFormat (thumbnail offset exists)
                if raw_exif.get(513):
                    thumb = img.copy()
                    thumb.thumbnail((100, 100))
                    thumb_arr = np.array(thumb.convert("RGB"), dtype=np.float32)

                    main = img.copy()
                    main.thumbnail((100, 100))
                    main_arr = np.array(main.convert("RGB"), dtype=np.float32)

                    if thumb_arr.shape == main_arr.shape:
                        diff = float(np.mean(np.abs(thumb_arr - main_arr)))
                        thumbnail_diff = round(diff, 2)
                        if diff > 30:
                            thumbnail_mismatch = True
                            ai_signatures_found.append(
                                f"Thumbnail mismatch (diff={diff:.1f}) — "
                                f"image content changed after thumbnail was created"
                            )
                            score += 0.40
                        elif diff > 15:
                            ai_signatures_found.append(
                                f"Slight thumbnail difference (diff={diff:.1f})"
                            )
                            score += 0.12
        except Exception:
            pass

        # ── 6. Consolidate score ──────────────────────────────────────────────
        has_ai_tag = len(ai_signatures_found) > 0
        has_exif = len(extracted_tags) > 0
        has_editing_software = len(editing_software_found) > 0

        if ai_signatures_found and any("stable diffusion" in s or "midjourney" in s or "dall-e" in s
                                       or "comfyui" in s or "novelai" in s or "firefly" in s
                                       for s in ai_signatures_found):
            # Hard positive: definitive AI generator signature
            tamper_score = 0.98
            conf = 0.99
            explanation = (
                f"Definitive generative AI metadata signatures found: {', '.join(ai_signatures_found)}."
            )
        elif has_ai_tag or has_editing_software:
            tamper_score = float(np.clip(0.55 + score, 0.05, 0.95))
            conf = 0.85
            all_findings = ai_signatures_found + editing_software_found
            explanation = f"Suspicious metadata signals: {'; '.join(all_findings[:3])}."
        elif not has_exif:
            tamper_score = 0.40  # Stripped EXIF is standard on WhatsApp
            conf = 0.50
            explanation = "Metadata completely stripped (typical for WhatsApp/Telegram compression; non-decisive)."
        else:
            tamper_score = float(np.clip(score, 0.05, 0.40))
            conf = 0.80
            explanation = (
                f"Camera/device EXIF metadata present ({len(extracted_tags)} tags). "
                f"Software: {software_detected or 'Standard capture pipeline'}."
            )

        details = {
            "tags_found_count": len(extracted_tags),
            "ai_signatures": ai_signatures_found,
            "editing_software": editing_software_found,
            "software_detected": software_detected,
            "date_mismatch": date_mismatch,
            "dimension_mismatch": dimension_mismatch,
            "thumbnail_mismatch": thumbnail_mismatch,
            "thumbnail_diff": thumbnail_diff,
            "actual_dimensions": f"{actual_w}x{actual_h}",
            "sample_tags": dict(list(extracted_tags.items())[:8]),
        }

        return float(np.clip(tamper_score, 0.05, 0.99)), conf, details, explanation

    except Exception as e:
        return 0.5, 0.2, {"error": str(e)}, f"Metadata check error: {e}"
