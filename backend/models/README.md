# models/

This directory stores production ML models. Git-ignored for binary size reasons.

## Current Model Files

| File | Size | Description | Status |
|---|---|---|---|
| `mobilenet_v2_finetuned.h5` | 23.6 MB | Fine-tuned MobileNetV2 (best accuracy, use this) | ✅ Present |
| `mobilenet_v2_base.h5` | 13.9 MB | Baseline MobileNetV2 (pre-fine-tuning) | ✅ Present |
| `mobilenet_v2_triage.onnx` | ~14 MB | Runtime ONNX model (generate from .h5 below) | ⚠ Generate |

## Generating the ONNX Model (Required for Runtime)

The production backend uses ONNX (no TensorFlow at inference time).
Run **once** on the dev machine, then copy `mobilenet_v2_triage.onnx` to this directory.

```bash
# From project root: Chandigarh_Police_Hackathon-main/
pip install tensorflow tf2onnx onnx

python backend/scripts/convert_mobilenet_to_onnx.py \
  --input backend/models/mobilenet_v2_finetuned.h5 \
  --output backend/models/mobilenet_v2_triage.onnx
```

⚠️ **CRITICAL — Preprocessing:**
The model was trained with `ImageDataGenerator(rescale=1./255)`.
Inputs MUST be in range **[0, 1]**, NOT [-1, 1].
The inference code in `mobilenet_triage.py` already uses `arr / 255.0` (correct).

## Verify the ONNX Model

```bash
python -c "
import onnxruntime as ort, numpy as np
s = ort.InferenceSession('backend/models/mobilenet_v2_triage.onnx')
print('Input :', s.get_inputs()[0].name, s.get_inputs()[0].shape)
# Test with dummy image — expect score between 0 and 1
inp = np.random.rand(1, 224, 224, 3).astype(np.float32)
out = s.run(None, {s.get_inputs()[0].name: inp})[0]
score = 1 / (1 + np.exp(-float(out.flat[0])))
print(f'Test score: {score:.4f}  (should be 0 < score < 1)')
assert 0.0 < score < 1.0, 'Score out of range!'
print('OK')
"
```

## Training Artifacts (Reference)

Training graphs are in `ml/training_artifacts/`:
- `mobilenet_training_graphs.png` — baseline training loss/accuracy curves
- `mobilenet_finetuning_graphs.png` — fine-tuning curves

Training scripts in `ml/`:
- `train_mobilenet_v2.py` — initial training (do not re-run, model already trained)
- `finetune_mobilenet_v2.py` — fine-tuning script (do not re-run)

## Notes

- `.onnx` and `.h5` files are `.gitignore`d (too large for Git)
- For demo: the `mobilenet_v2_triage.onnx` must exist in this directory before starting backend
- If ONNX file is missing: the system gracefully returns confidence=0 (neutral) for MobileNet triage
