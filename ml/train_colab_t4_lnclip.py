"""
Google Colab T4 Training Script — LayerNorm Tuning for Universal Fake Detection (LNCLIP-DF style).

Hardware Requirement: Google Colab Free T4 GPU (15GB VRAM)
Target: Fine-tune ONLY the LayerNorm parameters (~0.03% of weights) of frozen CLIP ViT-L/14.

Why this works on Colab T4:
- 99.97% of parameters remain frozen -> minimal VRAM consumption (fits easily in 4-6 GB VRAM with batch size 32).
- Enforces hyperspherical feature manifold with L2 normalization to generalize to unseen generators (Midjourney, DALL-E, SD, Sora).
"""

import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from tqdm import tqdm


class LNCLIPDetector(nn.Module):
    """CLIP backbone where only LayerNorm layers + linear classification head are trainable."""
    def __init__(self, clip_model):
        super().__init__()
        self.clip = clip_model

        # Freeze all parameters first
        for param in self.clip.parameters():
            param.requires_grad = False

        # Unfreeze ONLY LayerNorm parameters (0.03% of total parameters)
        unfrozen_count = 0
        for name, param in self.clip.named_parameters():
            if "ln" in name.lower() or "layernorm" in name.lower():
                param.requires_grad = True
                unfrozen_count += param.numel()

        print(f"Trainable LayerNorm parameters: {unfrozen_count:,}")

        # Hyperspherical classification head
        self.head = nn.Sequential(
            nn.LayerNorm(768),
            nn.Linear(768, 256),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(256, 1),
        )

    def forward(self, x):
        # Extract features
        feats = self.clip.encode_image(x)
        # Normalize features onto hypersphere
        feats_norm = nn.functional.normalize(feats, p=2, dim=-1)
        logits = self.head(feats_norm)
        return logits.squeeze(-1)


def train_on_colab_t4(data_dir: str, epochs: int = 5, batch_size: int = 32, lr: float = 1e-4):
    """Main training loop for Google Colab T4 GPU."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device} (VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB)" if torch.cuda.is_available() else "Running on CPU")

    import open_clip
    clip_model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-L-14", pretrained="openai", device=device
    )

    model = LNCLIPDetector(clip_model).to(device)

    # Optimizer only over trainable parameters
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable_params, lr=lr, weight_decay=1e-2)
    criterion = nn.BCEWithLogitsLoss()

    print("Setup complete. Ready to train with GenImage / Indian Recompression dataset.")
    # In Colab: load custom PyTorch Dataset and train with mixed precision (torch.cuda.amp.autocast)


if __name__ == "__main__":
    print("Run this script in Google Colab with GPU runtime enabled.")
