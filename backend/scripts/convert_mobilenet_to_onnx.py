"""
One-shot conversion: MobileNetV2 Keras .h5 → ONNX format.

Run on dev machine (needs tensorflow + tf2onnx), NOT in production Docker.
The output .onnx file is the only artifact that ships to production —
no TensorFlow dependency needed at inference time.

Model files (migrated from mobilenetV2/ project):
    backend/models/mobilenet_v2_finetuned.h5  ← USE THIS (best accuracy)
    backend/models/mobilenet_v2_base.h5        ← baseline model

IMPORTANT — Preprocessing:
    The model was trained with ImageDataGenerator(rescale=1./255) → inputs MUST be [0, 1].
    The mobilenet_triage.py inference code already uses arr / 255.0 (fixed).
    DO NOT use / 127.5 - 1.0 (that is MobileNetV2 standard but NOT how this model was trained).

Usage (run from Chandigarh_Police_Hackathon-main/):
    pip install tensorflow tf2onnx onnx
    python backend/scripts/convert_mobilenet_to_onnx.py \\
        --input backend/models/mobilenet_v2_finetuned.h5 \\
        --output backend/models/mobilenet_v2_triage.onnx

Verification:
    python -c "import onnxruntime; s=onnxruntime.InferenceSession('backend/models/mobilenet_v2_triage.onnx'); print(s.get_inputs()[0].shape)"
"""

import argparse
import sys
from pathlib import Path


def convert(input_path: str, output_path: str) -> None:
    """Convert Keras .h5 model to ONNX format."""
    try:
        import tensorflow as tf
        import tf2onnx
    except ImportError:
        print("ERROR: tensorflow and tf2onnx are required for conversion.")
        print("Install with: pip install tensorflow tf2onnx onnx")
        sys.exit(1)

    if not Path(input_path).exists():
        print(f"ERROR: Input model not found: {input_path}")
        sys.exit(1)

    print(f"Loading Keras model from {input_path}...")
    model = tf.keras.models.load_model(input_path)
    print(f"  Input shape: {model.input.shape}")
    print(f"  Output shape: {model.output.shape}")

    # Define input signature
    input_signature = [
        tf.TensorSpec(shape=model.input.shape, dtype=tf.float32, name="input")
    ]

    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting to ONNX (opset 13)...")
    tf2onnx.convert.from_keras(
        model,
        input_signature=input_signature,
        opset=13,
        output_path=output_path,
    )

    onnx_size = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"✓ Converted: {input_path} → {output_path} ({onnx_size:.1f} MB)")

    # Quick validation
    print("Validating ONNX model...")
    import onnxruntime as ort
    session = ort.InferenceSession(output_path)
    inp = session.get_inputs()[0]
    print(f"  Input name: {inp.name}, shape: {inp.shape}, type: {inp.type}")
    out = session.get_outputs()[0]
    print(f"  Output name: {out.name}, shape: {out.shape}")
    print("✓ ONNX validation passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert MobileNetV2 .h5 Keras model to ONNX"
    )
    parser.add_argument("--input", required=True, help="Path to .h5 Keras model file")
    parser.add_argument(
        "--output",
        default="models/mobilenet_v2_triage.onnx",
        help="Output ONNX model path (default: models/mobilenet_v2_triage.onnx)",
    )
    args = parser.parse_args()
    convert(args.input, args.output)
