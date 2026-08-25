"""
C2PA (Coalition for Content Provenance and Authenticity) Verification Module.

Extracts and validates Content Credentials manifests (JUMBF metadata).
Returns one of four explicit states:
- VALID_PROVENANCE (Signed manifest with intact cryptographic chain)
- BROKEN_CHAIN (Manifest present but validation failed / signatures invalid -> strong manipulation signal)
- NO_CREDENTIALS (No C2PA metadata found -> NEUTRAL in India, where 95%+ of social forwards lack C2PA)
- UNSUPPORTED_FORMAT

CRITICAL DESIGN RULE:
NO_CREDENTIALS must NEVER penalize the media or push the score toward 'Fake'.
"""

import json
import subprocess
from pathlib import Path
from typing import Tuple

from app.models.analysis_result import C2PAStatus


def verify_c2pa_manifest(file_path: str) -> Tuple[C2PAStatus, float, dict, str]:
    """
    Attempts to read and verify C2PA Content Credentials.
    Uses c2patool CLI wrapper or Python bindings if available, with robust fallback.
    
    Returns:
        (status, provenance_score, details_dict, explanation)
    """
    path_obj = Path(file_path)
    if not path_obj.exists():
        return C2PAStatus.UNSUPPORTED_FORMAT, 0.0, {}, "File not found."

    # Try c2patool if installed in container/system
    try:
        cmd = ["c2patool", str(file_path), "--detailed"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if proc.returncode == 0 and proc.stdout:
            data = json.loads(proc.stdout)
            active_manifest = data.get("active_manifest")
            validation_status = data.get("validation_status", [])

            # Check if there are any validation errors
            has_errors = any(
                item.get("code") != "claimSignature.validated" 
                for item in validation_status if "error" in item.get("status", "").lower()
            )

            if active_manifest and not has_errors:
                return (
                    C2PAStatus.VALID_PROVENANCE,
                    0.95,
                    data,
                    "Valid C2PA Content Credentials found with unbroken cryptographic signature chain."
                )
            elif active_manifest and has_errors:
                return (
                    C2PAStatus.BROKEN_CHAIN,
                    0.10,
                    data,
                    "C2PA manifest found, but cryptographic signature chain validation failed (tampering detected)."
                )
    except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
        pass

    # Inspect file headers directly for C2PA JUMBF boxes (JPEG/PNG/MP4)
    try:
        with open(file_path, "rb") as f:
            header_bytes = f.read(65536)  # Read initial 64KB

        if b"c2pa" in header_bytes or b"jumd" in header_bytes or b"c2ma" in header_bytes:
            return (
                C2PAStatus.BROKEN_CHAIN,
                0.20,
                {"header_match": "JUMBF/C2PA signature box detected but unvalidated"},
                "Potential C2PA metadata box detected in bitstream, but manifest signature could not be verified."
            )
    except Exception:
        pass

    # Default neutral state for Indian social media forwards
    return (
        C2PAStatus.NO_CREDENTIALS,
        0.50,
        {"status": "No C2PA manifest found (typical for social media re-shares)"},
        "No C2PA Content Credentials detected. (Neutral: typical for social forwards with stripped EXIF)."
    )
