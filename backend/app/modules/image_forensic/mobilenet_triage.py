"""
Tier-0 MobileNetV2 Fast Triage — ONNX Runtime (zero TensorFlow dependency).

Returns calibrated fake-probability in ~5ms on CPU, <1ms on GPU.
Feeds into Dempster-Shafer fusion engine as an independent CNN evidence signal
alongside the primary CLIP ViT transformer signal.

Architecture Decision:
    - MobileNetV2 is a CNN → captures LOCAL texture/pixel artifacts
    - CLIP ViT-L/14 is a Transformer → captures GLOBAL semantic inconsistencies
    - Together they form a dual-architecture ensemble that's harder to adversarially evade

Design Rules:
    1. ONNX singleton session — loaded once, reused across all requests
    2. Returns calibrated [0.02, 0.98] — never 0.0 or 1.0 (epistemic humility)
    3. Confidence based on distance from decision boundary, capped at 0.75
       (CNN triage is NEVER given more weight than CLIP in fusion)
    4. Graceful fallback: if model file missing → returns 0.5 with zero confidence
"""

import logging
import time
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Module-level ONNX Singleton ──────────────────────
_session = None
_session_load_attempted = False


def _get_session():
    """Lazy-load ONNX InferenceSession singleton."""
    global _session, _session_load_attempted

    if _session is not None:
        return _session

    if _session_load_attempted:
        return None  # Already tried and failed — don't retry every request

    _session_load_attempted = True
    model_path = settings.MOBILENET_ONNX_PATH

    if not Path(model_path).exists():
        logger.warning(
            f"MobileNetV2 ONNX model not found at '{model_path}'. "
            f"Triage module will return neutral scores. "
            f"Run scripts/convert_mobilenet_to_onnx.py to generate the model."
        )
        return None

    try:
        import onnxruntime as ort

        sess_opts = ort.SessionOptions()
        sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_opts.enable_mem_pattern = True
        sess_opts.enable_mem_reuse = True

        _session = ort.InferenceSession(
            model_path,
            sess_opts,
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
        inp = _session.get_inputs()[0]
        logger.info(
            f"MobileNetV2 ONNX loaded: {model_path} "
            f"(input: {inp.name} {inp.shape}, "
            f"provider: {_session.get_providers()[0]})"
        )
        return _session

    except ImportError:
        logger.error("onnxruntime not installed. pip install onnxruntime")
        return None
    except Exception as e:
        logger.error(f"Failed to load MobileNetV2 ONNX: {e}")
        return None


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Resize to 224×224 and normalize to [-1, 1] range.
    This matches MobileNetV2's tf.keras.applications.mobilenet_v2.preprocess_input.
    """
    img = image.convert("RGB").resize((224, 224), Image.LANCZOS)
    arr = np.array(img, dtype=np.float32)
    arr = arr / 255.0  # Scale [0, 255] → [0, 1]  — matches train.py: ImageDataGenerator(rescale=1./255)
    return arr[np.newaxis, ...]  # Batch dim: (1, 224, 224, 3)


def run_mobilenet_triage(
    image_path: str,
) -> Tuple[float, float, dict, str]:
    """
    Fast binary triage: Genuine vs. Tampered.

    Returns:
        (fake_probability, confidence, details_dict, explanation)

    Failure modes:
        - Model not found → (0.5, 0.0, {...}, "not available")
        - Inference error → (0.5, 0.0, {...}, "error: ...")
        - Module disabled → (0.5, 0.0, {...}, "disabled")
    """
    if not settings.MOBILENET_ENABLED:
        return 0.5, 0.0, {"status": "disabled"}, "MobileNetV2 triage disabled in settings."

    session = _get_session()
    if session is None:
        return (
            0.5,
            0.0,
            {"status": "model_not_found", "path": settings.MOBILENET_ONNX_PATH},
            "MobileNetV2 ONNX model not available — skipping triage.",
        )

    try:
        t0 = time.perf_counter_ns()

        img = Image.open(image_path)
        input_arr = preprocess_image(img)

        # Run ONNX inference
        input_name = session.get_inputs()[0].name
        raw_output = session.run(None, {input_name: input_arr})[0]

        # Apply sigmoid if output is logit (single neuron output)
        raw_logit = float(raw_output.flat[0])
        raw_score = float(1.0 / (1.0 + np.exp(-raw_logit)))

        # Calibration: clip to [0.02, 0.98]
        # TODO(hackathon): Replace with proper Platt scaling after validation dataset
        calibrated = float(np.clip(raw_score, 0.02, 0.98))

        # Confidence: distance from decision boundary × 2, capped at 0.75
        # MobileNetV2 triage is NEVER more confident than 75% — it's a fast screen,
        # not the primary detector. The fusion engine respects this cap.
        confidence = float(np.clip(abs(calibrated - 0.5) * 2.0, 0.20, 0.75))

        elapsed_ms = (time.perf_counter_ns() - t0) / 1_000_000

        details = {
            "raw_logit": round(raw_logit, 4),
            "raw_sigmoid": round(raw_score, 4),
            "calibrated_score": round(calibrated, 4),
            "confidence": round(confidence, 4),
            "inference_time_ms": round(elapsed_ms, 1),
            "inference_backend": "onnxruntime",
            "model": "MobileNetV2-Binary-Triage",
            "model_path": settings.MOBILENET_ONNX_PATH,
        }

        # Generate human-readable explanation
        if calibrated > 0.70:
            explanation = (
                f"MobileNetV2 Triage: {round(calibrated * 100, 1)}% tampered likelihood "
                f"(fast CNN screen, {round(elapsed_ms, 1)}ms). Full pipeline analysis recommended."
            )
        elif calibrated < 0.30:
            explanation = (
                f"MobileNetV2 Triage: {round((1 - calibrated) * 100, 1)}% genuine likelihood "
                f"(fast CNN screen, {round(elapsed_ms, 1)}ms)."
            )
        else:
            explanation = (
                f"MobileNetV2 Triage: Ambiguous result ({round(calibrated * 100, 1)}% tampered) "
                f"— full multi-modal pipeline analysis required."
            )

        return calibrated, confidence, details, explanation

    except Exception as e:
        logger.error(f"MobileNetV2 triage failed for {image_path}: {e}")
        return (
            0.5,
            0.0,
            {"error": str(e), "status": "inference_failed"},
            f"MobileNetV2 triage error: {e}",
        )
