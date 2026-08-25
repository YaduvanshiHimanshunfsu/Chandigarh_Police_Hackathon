"""
Indian Social Media Recompression Dataset Generator.

Simulates the degradation chain observed in Indian social networks (WhatsApp, Telegram, Instagram):
- Hop 1: Mild JPEG compression (Q=85) + 0.9x downscaling
- Hop 2: Moderate compression (Q=65) + slight color gamut shift
- Hop 3: Severe WhatsApp recompression (Q=42) + noise injection + downscaling
- Hop 4: Screenshotting & re-saving (Q=30)
- Hop 5: Extreme multi-group forward degradation (Q=20)

Used to fine-tune and evaluate detectors for real-world robustness.
"""

import io
import os
from pathlib import Path
from PIL import Image, ImageEnhance
import numpy as np


# Progression of JPEG quality degradation per forwarding hop
QUALITY_SCHEDULE = {1: 85, 2: 65, 3: 42, 4: 30, 5: 20}


def apply_whatsapp_recompression_hop(img: Image.Image, hop_level: int) -> Image.Image:
    """Applies realistic social media forwarding degradation."""
    w, h = img.size

    quality = QUALITY_SCHEDULE.get(hop_level, 40)

    # Slight scaling down (mimicking WhatsApp resizing max 1600px -> 1280px -> 1024px)
    scale_factor = max(0.6, 1.0 - (hop_level * 0.08))
    new_w, new_h = int(w * scale_factor), int(h * scale_factor)
    resized = img.resize((new_w, new_h), Image.Resampling.BILINEAR)

    # Re-encode as JPEG
    buffer = io.BytesIO()
    resized.save(buffer, "JPEG", quality=quality)
    buffer.seek(0)
    recompressed = Image.open(buffer).convert("RGB")

    return recompressed


def generate_degradation_benchmark(input_dir: str, output_dir: str, max_hops: int = 5):
    """Processes a directory of real/AI images through 1-5 degradation hops."""
    in_path = Path(input_dir)
    out_path = Path(output_dir)

    for hop in range(1, max_hops + 1):
        hop_dir = out_path / f"hop_{hop}"
        hop_dir.mkdir(parents=True, exist_ok=True)

    image_files = list(in_path.glob("*.jpg")) + list(in_path.glob("*.png"))
    print(f"Generating {max_hops}-hop degradation for {len(image_files)} images...")

    for img_file in image_files:
        try:
            current_img = Image.open(img_file).convert("RGB")
            for hop in range(1, max_hops + 1):
                current_img = apply_whatsapp_recompression_hop(current_img, hop)
                target = out_path / f"hop_{hop}" / f"{img_file.stem}_hop{hop}.jpg"
                current_img.save(target, "JPEG", quality=QUALITY_SCHEDULE.get(hop, 40))
        except Exception as e:
            print(f"Error processing {img_file}: {e}")

    print("Recompression dataset generation complete.")


if __name__ == "__main__":
    print("Indian Recompression Dataset generator ready. Call generate_degradation_benchmark(input_dir, output_dir)")
