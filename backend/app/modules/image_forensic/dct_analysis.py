"""
Frequency-Domain & DCT Spectral Residual Analysis.

Analyzes Discrete Cosine Transform (DCT) and Fast Fourier Transform (FFT)
high-frequency residuals to identify GAN upsampling artifacts and diffusion grid patterns.

Also includes JPEG 8x8 block boundary artifact detection (ported from mobilenetV2/compression.py):
copy-pasted image regions show strong pixel discontinuities exactly at 8-pixel grid boundaries.

CRITICAL INDIA-SPECIFIC DESIGN RULE:
The frequency branch vote is AUTOMATICALLY DOWN-WEIGHTED when the input's estimated
JPEG quality is low (<50), preventing false negatives caused by WhatsApp multi-hop recompression.
"""

from typing import Tuple, Dict, Any
import numpy as np
import cv2
from PIL import Image


def analyze_frequency_domain(
    image: Image.Image, jpeg_quality_estimate: int = 75
) -> Tuple[float, float, Dict[str, Any], str]:
    """
    Performs DCT and FFT residual spectral analysis plus block boundary artifact detection.

    Returns:
        (fake_probability, effective_weight, details_dict, explanation)
    """
    try:
        img_rgb = np.array(image.convert("RGB"), dtype=np.float32)
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

        # 1. 2D Discrete Cosine Transform (DCT) on 8x8 blocks
        h, w = gray.shape
        h_crop = (h // 8) * 8
        w_crop = (w // 8) * 8
        gray_crop = gray[:h_crop, :w_crop]

        # Calculate high-frequency block grid variance
        blocks = gray_crop.reshape(h_crop // 8, 8, w_crop // 8, 8).swapaxes(1, 2)
        dct_blocks = np.zeros_like(blocks)

        for i in range(blocks.shape[0]):
            for j in range(blocks.shape[1]):
                dct_blocks[i, j] = cv2.dct(blocks[i, j])

        # High frequency AC coefficients (bottom-right 4x4 of each 8x8 block)
        high_freq_ac = dct_blocks[:, :, 4:, 4:]
        ac_energy = float(np.mean(np.abs(high_freq_ac)))
        ac_variance = float(np.var(high_freq_ac))

        # 2. FFT Spectral Grid / Radial Symmetry Check
        dft = cv2.dft(gray, flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        mag = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1e-5)

        # Measure high-frequency anomalous peaks (GAN upsampling/checkerboard artifacts)
        cy, cx = h // 2, w // 2
        r = min(cx, cy) // 3
        y, x = np.ogrid[:h, :w]
        outer_mask = ((x - cx)**2 + (y - cy)**2) >= r**2
        spectral_noise_ratio = float(np.std(mag[outer_mask]) / (np.mean(mag[outer_mask]) + 1e-5))

        # Compute raw synthetic probability based on frequency anomalies
        raw_score = 1.0 / (1.0 + np.exp(-(ac_variance * 0.05 + spectral_noise_ratio * 4.0 - 3.5)))
        raw_score = float(np.clip(raw_score, 0.05, 0.95))

        # 3. Block Boundary Artifact Check (ported from mobilenetV2/compression.py)
        # JPEG stores images in 8x8 blocks. When a region is copy-pasted from another image,
        # its block boundaries don't align with the host → strong discontinuity at 8-pixel grid lines.
        # We measure: avg pixel diff AT 8-pixel boundary rows vs avg diff INSIDE blocks.
        # boundary_ratio > 1.5 → misaligned JPEG blocks → document tampering signal.
        boundary_diffs: list = []
        interior_diffs: list = []
        gray_f64 = gray.astype(np.float64)
        for row in range(8, h_crop - 8, 1):
            for col in range(8, w_crop - 8, 1):
                diff = abs(gray_f64[row, col] - gray_f64[row - 1, col])
                if row % 8 == 0:
                    boundary_diffs.append(diff)
                elif 2 < (row % 8) < 6:
                    interior_diffs.append(diff)

        boundary_ratio = 1.0
        if boundary_diffs and interior_diffs:
            avg_boundary = float(np.mean(boundary_diffs))
            avg_interior = float(np.mean(interior_diffs))
            boundary_ratio = avg_boundary / avg_interior if avg_interior > 0 else 1.0
            # Boost raw_score for strong block misalignment
            if boundary_ratio > 2.0:
                raw_score = float(np.clip(raw_score + 0.15, 0.05, 0.95))
            elif boundary_ratio > 1.5:
                raw_score = float(np.clip(raw_score + 0.08, 0.05, 0.95))

        # 4. Dynamic Reliability Weighting based on JPEG Quality (Indian Forwarding Robustness)
        # If WhatsApp degraded JPEG quality to e.g. Q=35, down-weight the frequency branch
        if jpeg_quality_estimate < 40:
            effective_weight = 0.25  # Heavily degraded
            recompression_note = "High recompression detected (WhatsApp/social forward) -> Frequency vote down-weighted."
        elif jpeg_quality_estimate < 65:
            effective_weight = 0.60  # Moderate degradation
            recompression_note = "Moderate recompression -> Adjusted weight."
        else:
            effective_weight = 1.00  # High quality original
            recompression_note = "Clean high-frequency signal preserved."

        details = {
            "ac_energy": round(ac_energy, 2),
            "ac_variance": round(ac_variance, 2),
            "spectral_noise_ratio": round(spectral_noise_ratio, 3),
            "block_boundary_ratio": round(boundary_ratio, 3),
            "jpeg_quality_estimate": jpeg_quality_estimate,
            "effective_weight": effective_weight,
            "recompression_note": recompression_note,
        }

        explanation = (
            f"Frequency domain analysis estimated {round(raw_score * 100, 1)}% synthetic likelihood. "
            f"Block boundary ratio: {boundary_ratio:.2f} (>1.5 = misaligned JPEG blocks). "
            f"Reliability weight: {effective_weight} ({recompression_note})"
        )

        return raw_score, effective_weight, details, explanation

    except Exception as e:
        return 0.5, 0.1, {"error": str(e)}, f"DCT analysis failed: {e}"
