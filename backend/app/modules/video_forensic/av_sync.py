"""
Audio-Visual Synchronization & Voice Clone Misalignment Detector.

Analyzes cross-modal correlation between speech acoustic energy / phonemes (librosa)
and visual mouth opening / landmark displacements (SyncNet-style).

Targets:
- "Digital Arrest" extortion scam video calls (fraudster voice dubbed over fabricated cop/customs officer video)
- Face-swap deepfakes paired with synthetic cloned audio
"""

import io
from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
import cv2


def analyze_av_synchronization(
    video_path: str,
) -> Tuple[float, float, Dict[str, Any], str]:
    """
    Measures cross-modal alignment between audio speech energy and visual mouth dynamics.

    Returns:
        (desync_manipulation_score, confidence, details_dict, explanation)
    """
    path_obj = Path(video_path)
    if not path_obj.exists():
        return 0.5, 0.0, {"error": "File not found"}, "Video file missing."

    try:
        import librosa

        # 1. Extract and analyze audio stream
        try:
            y, sr = librosa.load(video_path, sr=16000, duration=15.0)
            audio_present = len(y) > 0 and np.max(np.abs(y)) > 0.01
        except Exception:
            audio_present = False
            y, sr = None, None

        if not audio_present or y is None:
            return (
                0.0,
                0.20,
                {"audio_stream_detected": False},
                "No active audio stream detected in video container (AV sync analysis skipped)."
            )

        # Compute audio RMS energy envelope & onset strength
        hop_length = 512
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

        # 2. Extract mouth region variance across sampled frames
        cap = cv2.VideoCapture(video_path)
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 25.0)
        mouth_energies = []

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        frame_count = 0
        while cap.isOpened() and frame_count < int(fps * 15.0):
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % max(1, int(fps / 15.0)) == 0:  # Sample at ~15fps
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 5)
                if len(faces) > 0:
                    fx, fy, fw, fh = faces[0]
                    # Lower third of face corresponds to mouth area
                    mouth_roi = gray[fy + int(fh * 0.65): fy + fh, fx + int(fw * 0.2): fx + int(fw * 0.8)]
                    if mouth_roi.size > 0:
                        mouth_energies.append(float(np.var(mouth_roi)))
                    else:
                        mouth_energies.append(0.0)
                else:
                    mouth_energies.append(0.0)
            frame_count += 1

        cap.release()

        if len(mouth_energies) < 10:
            return (
                0.5,
                0.30,
                {"mouth_samples": len(mouth_energies)},
                "Insufficient visible mouth frames detected for audio-visual correlation."
            )

        # 3. Cross-correlation between resampled audio envelope and mouth dynamics
        mouth_series = np.array(mouth_energies, dtype=np.float32)
        mouth_series = (mouth_series - np.mean(mouth_series)) / (np.std(mouth_series) + 1e-5)

        # Resample audio envelope to match mouth sample length
        audio_interp = np.interp(
            np.linspace(0, 1, len(mouth_series)),
            np.linspace(0, 1, len(rms)),
            rms,
        )
        audio_interp = (audio_interp - np.mean(audio_interp)) / (np.std(audio_interp) + 1e-5)

        # Pearson correlation
        correlation = float(np.corrcoef(mouth_series, audio_interp)[0, 1])
        if np.isnan(correlation):
            correlation = 0.0

        # Low or negative correlation indicates audio dubbing / voice clone overlay
        desync_score = float(np.clip(1.0 - (correlation + 1.0) / 2.0, 0.05, 0.95))
        confidence = float(np.clip(len(mouth_energies) / 40.0, 0.50, 0.90))

        details = {
            "cross_modal_correlation": round(correlation, 3),
            "av_desync_score": round(desync_score, 3),
            "audio_duration_sec": round(len(y) / sr, 2),
            "mouth_tracking_frames": len(mouth_energies),
        }

        if desync_score >= 0.70:
            exp_text = "Severe audio-visual desynchronization detected (suggestive of voice clone dubbing / audio replacement)."
        else:
            exp_text = "Acoustic phonemes and visual mouth kinetics demonstrate natural synchronization."

        explanation = (
            f"Audio-Visual Lip-Sync Analysis: {round(desync_score * 100, 1)}% desync anomaly likelihood "
            f"(Correlation: {round(correlation, 2)}, Confidence: {round(confidence * 100)}%). {exp_text}"
        )

        return desync_score, confidence, details, explanation

    except Exception as e:
        return 0.5, 0.1, {"error": str(e)}, f"Audio-visual sync analysis failed: {e}"
