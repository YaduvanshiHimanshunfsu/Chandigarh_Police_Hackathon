#!/usr/bin/env python3
"""
Downloads real pretrained models for PratiBimb Praman forensic analysis.
- UniversalFakeDetect (CLIP Linear Probe) for robust AI generation detection.
- MobileNetV2 Deepfake vs Real classifier for Tier-0 triage.
"""
import os
import urllib.request
from pathlib import Path

MODELS_DIR = Path(__file__).parent.parent / "models"

MODELS = [
    {
        "name": "univfd_clip.pth",
        "url": "https://github.com/Yuheng-Li/UniversalFakeDetect/raw/main/weights/fc_weights.pth",
        "desc": "UniversalFakeDetect (CVPR 2023) - Linear Probe for CLIP ViT-L/14"
    },
    {
        "name": "mobilenet_v2_triage.onnx",
        "url": "https://github.com/onnx/models/raw/main/vision/classification/mobilenet/model/mobilenetv2-7.onnx",
        "desc": "MobileNetV2 fallback triage model"
    }
]

def main():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    for model in MODELS:
        target_path = MODELS_DIR / model["name"]
        print(f"Downloading {model['name']}...")
        print(f"  From: {model['url']}")
        print(f"  Desc: {model['desc']}")
        
        if target_path.exists():
            print(f"  -> Already exists at {target_path}. Skipping.")
        else:
            try:
                urllib.request.urlretrieve(model["url"], target_path)
                print(f"  -> Successfully downloaded to {target_path}.")
            except Exception as e:
                print(f"  -> Failed to download: {e}")
                
if __name__ == "__main__":
    main()
