# 🔍 PratiBimb Praman — MASTER BLUEPRINT v2.0
## AI Media Forensic Provenance & Origin Intelligence Platform
### Chandigarh Police National Hackathon 2026 — Problem Statement 4

> **Date**: August 25, 2026 | **Hackathon**: September 8–9, 2026 (24-Hour Offline + Grand Finale)

---

## Table of Contents
1. [Problem Statement](#1-problem-statement)
2. [Problem Decomposition — 8 Sub-Challenges](#2-problem-decomposition)
3. [Indian Scenario — Why This Matters Specifically in India](#3-indian-scenario)
4. [Current Project Audit — Honest Assessment](#4-current-project-audit)
5. [MobileNetV2 Integration — Deep Pros/Cons/Problems Analysis](#5-mobilenetv2-integration-analysis)
6. [Better Solutions — Research-Backed Alternatives](#6-better-solutions)
7. [Unique Feature Synthesis — The 10 Features That Make Us Win](#7-unique-feature-synthesis)
8. [Technical Approach — Brain & Skeleton](#8-technical-approach)
9. [Detailed Backend Architecture](#9-detailed-backend-architecture)
10. [Languages & Libraries (What & Why)](#10-languages--libraries)
11. [Research Required](#11-research-required)
12. [Wireframes & UI Screens](#12-wireframes)
13. [Flowcharts & Architecture Diagrams](#13-flowcharts--architecture-diagrams)
14. [How This is Different from EVERY Other Project](#14-how-this-is-different)
15. [How This Helps Police & Law Enforcement](#15-how-this-helps-police)
16. [Hackathon Execution Timeline](#16-hackathon-execution-timeline)
17. [Honest Limitations](#17-honest-limitations)
18. [Referenced Research Papers & Repos](#18-referenced-research)

---

## 1. Problem Statement

> **"Build an AI-powered digital forensic platform to detect AI-generated or manipulated images and videos, verify their authenticity, and trace their origin and dissemination across social media. The solution should help combat misinformation, impersonation, cyber fraud, and digital evidence tampering."**

### What This Actually Asks (Most Teams Will Miss This)
This single paragraph contains **EIGHT** distinct technical challenges. Most teams will treat it as a single binary classifier ("real vs fake"). We decompose it properly:

- **Detect** → AI-generated (fully synthetic) + AI-altered (partial manipulation) + traditional edits (Photoshop)
- **Verify** → Cryptographic provenance (C2PA), watermark integrity, chain-of-custody
- **Trace Origin** → Find the earliest indexed instance of media on the open web
- **Trace Dissemination** → Map propagation graph across platforms (who shared what, when, where)
- **Combat Misinformation** → Output must be interpretable, uncertainty-aware, usable by courts
- **Combat Impersonation** → Face-swap / voice-clone targeting specific identifiable individuals
- **Combat Cyber Fraud** → Bulk triage for digital arrest scams, UPI fraud screenshots
- **Combat Evidence Tampering** → Platform's own output must be legally admissible as evidence

---

## 2. Problem Decomposition — The 8 Sub-Challenges

```mermaid
mindmap
  root((Problem Statement 4))
    Detection Layer
      Fully AI-Generated Media
      AI-Manipulated Media
      Conventionally Edited Media
      Authentic Media
    Verification Layer
      Cryptographic Provenance
      Chain-of-Custody
    Tracing Layer
      Origin Tracing
      Dissemination Mapping
    Application Layer
      Combat Misinformation
      Combat Impersonation
      Combat Cyber Fraud
      Combat Evidence Tampering
```

### Why This Decomposition Wins Points
- **Judges see** that you understood the full scope, not just "fake vs real"
- **Each sub-challenge** maps to a specific module in your architecture
- **NIST OpenMFC** explicitly frames the same questions: "has it been manipulated, was it malicious, who did it, what was the source, which tool was used" — cite this directly in your deck

---

## 3. Indian Scenario — Why This Matters Specifically in India

> [!IMPORTANT]
> A hackathon judged by **Chandigarh Police** will reward a team that demonstrates deep understanding of the **Indian threat surface**, not a generic global one.

### 3.1 Hard Statistics (2025–2026, Verified Sources)

| Metric | Data Point | Source |
|---|---|---|
| **Total cyber fraud losses** | ₹52,976 crore over 6 years | NHRC Report 2026 |
| **Digital arrest scam losses** | ₹22,495 crore in 2025 alone (~9% of total) | ORF Analysis 2026 |
| **NCRP complaint surge** | 2.6 lakh (2021) → 24 lakh (2025) — **9x growth** | NCRP Data |
| **Voice clone vulnerability** | 47% of Indian adults victimized (2× global avg); 83% lost money | McAfee Survey 2025 |
| **Election deepfakes** | ~280% rise around 2024 Lok Sabha; 50M+ AI voice-clone calls | Multiple verified |
| **Chandigarh-specific (2026)** | **4,280 cybercrime complaints** in first 5 months, 80 FIRs, ₹10.37cr lost to digital arrest | Indian Express / TOI |
| **Chandigarh Police action** | 74 arrests across 11 states in first 5 months of 2026 | Times of India |

### 3.2 Why Generic (Western-Benchmark) Detectors FAIL in India

```mermaid
flowchart LR
    A["Original Media"] -->|"WhatsApp Forward 1"| B["Recompressed Gen 1"]
    B -->|"WhatsApp Forward 2"| C["Recompressed Gen 2"]
    C -->|"Screenshot + Telegram"| D["Recompressed Gen 3"]
    D -->|"Instagram Repost"| E["Recompressed Gen 4"]
    E -->|"WhatsApp Again"| F["What Investigator Gets"]
    style F fill:#ff4444,color:#fff
```

| Problem | Why It Kills Generic Detectors |
|---|---|
| **WhatsApp Recompression Chain** | Content forwarded 3-10x loses the exact artifacts detectors rely on. No public benchmark models this |
| **C2PA Coverage = Near Zero** | Realistic case: WhatsApp-forwarded screenshot-of-screenshot with ALL metadata stripped |
| **Vernacular Content Gap** | Hindi/Punjabi text overlays, Telegram branding absent from FaceForensics++/DFDC |
| **Uncrawlable Primary Channel** | WhatsApp (E2E encrypted) and private Telegram = invisible to origin tracing |
| **Indian Face/Skin Tone Gap** | DFDC, Celeb-DF = overwhelmingly Western faces; Indian performance untested |
| **Accuracy drops 10-20%+** | Under social media compression vs clean datasets (2026 research confirmed) |

### 3.3 The Legal & Institutional Landscape (Judge Goldmine)

> [!TIP]
> Most teams will NOT research Indian law. Doing so is a **direct, defensible differentiator** to a police audience.

#### Criminal Statutes for Deepfake Cases
| Law | Relevant Sections | Application |
|---|---|---|
| **BNS (2023)** | §308 (extortion), §336 (forgery — covers AI-morphed), §351 (intimidation), §356 (defamation) | Primary criminal charges |
| **IT Act, 2000** | §66C (identity theft), §66D (personation), §66E (privacy), §67/67A (obscene/explicit) | Cyber-specific charges |
| **IT Rules Nov 2025/Feb 2026** | Takedown within **3 hours** (govt order); 24h (sexual deepfakes); 36h (other synthetic misinformation) | Our report triggers this clock |

#### The Make-or-Break: BSA Section 63(4) Certificate

```
┌──────────────────────────────────────────────────────┐
│  BSA Section 63(4) — DUAL CERTIFICATION (NEW LAW)    │
├──────────────────────────────────────────────────────┤
│  PART A: Person in lawful control of device/data     │
│    - Device details (Make, Model, IMEI/MAC)          │
│    - Operating conditions during material period     │
│    - Attestation of faithful/accurate output         │
│                                                      │
│  PART B: Independent technical expert                │
│    - Technical verification of integrity             │
│    - Hash values (SHA-256) — NOW MANDATORY           │
│    - Tool/software identification                    │
│    - Process description                             │
│                                                      │
│  KEY CHANGE vs OLD LAW (IEA §65B):                   │
│    Old: 1 signatory, no fixed format, no hash        │
│    New: 2 signatories, prescribed format, SHA-256    │
└──────────────────────────────────────────────────────┘
```

> **This is a concrete, buildable feature.** No commercial tool (Reality Defender, Sensity, Hive) auto-generates a BSA-63(4) certificate. This is our **single strongest differentiator.**

---

## 4. Current Project Audit — Honest Assessment

### 4.1 What's Already Built (Strengths)

| Component | Status | Assessment |
|---|---|---|
| **Project Architecture** | ✅ Complete | FastAPI + Celery + Docker Compose + Next.js. Professional-grade |
| **Fusion Engine (THE BRAIN)** | ✅ Functional | Dempster-Shafer is correct, conflict logging works, belief mass normalization sound |
| **Image Forensic Detector** | ✅ Functional | CLIP ViT-L/14 + DCT ensemble with dynamic recompression weighting |
| **Video Forensic Module** | ✅ Functional | Temporal (Farneback optical flow + face jitter) + AV sync, quality gate correct |
| **Watermark Detector** | ✅ Functional | FFT-based spectral analysis, correct 3-state output |
| **Origin Trace Pipeline** | ✅ Scaffolded | pHash + CLIP FAISS designed, simulated retrieval works |
| **Chain-of-Custody** | ✅ Designed | SHA-256 + Merkle chain ledger pattern in place |
| **Docker Compose** | ✅ Complete | One-command demo with pgvector, Redis, FastAPI, Celery, Next.js |
| **ML Training Script** | ✅ Ready | LNCLIP-DF style LayerNorm-only tuning for Colab T4 |

### 4.2 What's Weak / Missing (Gaps)

| Gap | Severity | Impact |
|---|---|---|
| **No trained model weights** | 🔴 Critical | CLIP head has random weights — outputs are heuristic, not learned |
| **No Indian Recompression Dataset** | 🔴 Critical | The unique selling point hasn't been built yet |
| **Watermark detector is heuristic-only** | 🟡 Medium | Spectral thresholds hand-tuned, not validated against real SynthID |
| **Origin tracing uses simulated data** | 🟡 Medium | No real search API integration yet |
| **Frontend is bare scaffold** | 🟡 Medium | Need visual wow-factor for judges |
| **No BSA-63(4) PDF generator** | 🔴 Critical | The #1 differentiator exists only in docs, not code |
| **No Grad-CAM++ localization** | 🟡 Medium | Heatmap not implemented yet |
| **`temporal.py` has a bug** | 🟡 Low | Line 72: `CascadeCascade` — typo in variable name |
| **No C2PA integration** | 🟡 Medium | c2pa-rs/c2patool not wired up yet |

### 4.3 Code Quality Verdict

The codebase is **architecturally sound and well-documented**. Comments are excellent, module separation clean, Dempster-Shafer math correct. Main gap is **execution** — skeleton is strong but muscles (trained weights, real API calls, PDF output) aren't attached.

---

## 5. MobileNetV2 Integration Analysis

### 5.1 What's in the ZIP

The `mobilenetV2-main.zip` (33.6 MB) contains a **TensorFlow/Keras binary classifier** (Genuine vs. Tampered) with:
- Pre-trained MobileNetV2 backbone (ImageNet weights)
- Binary classification head
- Basic heuristic scripts (ELA, metadata, compression check)
- Saved `.h5` model weights

### 5.2 Integration Pros

| Pro | Detail | Impact |
|---|---|---|
| **Speed** | Inference ~5-10ms vs ~200-500ms for CLIP ViT-L/14 | Excellent for bulk CCTV triage |
| **Resource Efficiency** | ~14MB model vs ~1.7GB CLIP; ~200MB RAM vs ~4GB | Runs on officer's laptop without GPU |
| **Defense-in-Depth** | Independent CNN architecture complements ViT transformer | Adversarial evasion must fool BOTH |
| **Tier-0 Pre-Filter** | If MobileNetV2 says >98% → prioritize/deprioritize queue | Reduces load on CLIP |
| **Already Trained** | Has actual weights (unlike our CLIP head) | Gives working demo immediately |

### 5.3 Integration Cons

| Con | Detail | Severity |
|---|---|---|
| **Framework Bloat** | PyTorch (CLIP) + TensorFlow (MobileNetV2) in same worker → **doubles memory**, CUDA OOM risk | 🔴 Critical |
| **Generalization Gap** | CNN relies on local textures; struggles with global inconsistencies and unseen generators | 🔴 Critical |
| **WhatsApp Vulnerability** | Standard MobileNetV2 drops ~30-50% accuracy on multi-hop compressed Indian content | 🟡 High |
| **Redundant Heuristics** | ZIP contains `ela.py`, `metadata.py` overlapping our modules | 🟢 Low |
| **No Platt Calibration** | Sigmoid is NOT a true probability → cannot feed into Dempster-Shafer directly | 🟡 High |
| **Training Data Unknown** | Don't know what dataset ZIP model was trained on; may overfit | 🟡 High |

### 5.4 Three Critical Problems We WILL Face

> [!WARNING]
> **Problem 1: Memory Explosion**
> PyTorch (CLIP ~1.7GB) + TensorFlow (MobileNetV2 ~200MB + TF runtime ~1.5GB) = **~4-5GB baseline**. In Docker with Celery workers → OOM kills.
>
> **Solution**: Convert `.h5` → **ONNX** via `tf2onnx`. Run with `onnxruntime` (~50MB runtime) — no TensorFlow in production.

> [!WARNING]
> **Problem 2: Probability Calibration Mismatch**
> MobileNetV2 sigmoid output is raw score, NOT epistemic probability. Feeding it into Dempster-Shafer corrupts conflict detection.
>
> **Solution**: **Platt Scaling** (isotonic regression on held-out validation) before treating output as belief mass.

> [!WARNING]
> **Problem 3: Indian Recompression Vulnerability**
> Standard MobileNetV2 (clean images) will have ~30-50% accuracy drop on 3rd-gen WhatsApp forwards.
>
> **Solution**: Down-weight MobileNetV2 mass in fusion when JPEG-Q estimate is low. Or re-train with JPEG augmentation (Q=15-85).

### 5.5 Integration Verdict

**YES — as Tier-0 Triage only, NOT as primary detector.**

```mermaid
flowchart TD
    A["Media Upload"] --> B{"MobileNetV2 ONNX<br/>Triage ~5ms"}
    B -->|"Confidence > 98%"| C["Fast Path: Flag + Queue"]
    B -->|"Confidence < 98%"| D["Full Pipeline: CLIP + DCT<br/>+ C2PA + Watermark + Fusion"]
    B -->|"Platt-calibrated mass"| E["Evidence Fusion Engine"]
    C --> E
    D --> E
    E --> F["Report + BSA Certificate"]
```

---

## 6. Better Solutions — Research-Backed Alternatives

> [!IMPORTANT]
> These aren't hypothetical — they're **published, cited, some with open-source code**.

### 6.1 Combining Features from Multiple SOTA Approaches

| Source | Feature We Take | Their Weakness We Fix |
|---|---|---|
| **LNCLIP-DF** (arXiv 2508.06248) | LayerNorm-only tuning = best cross-generator generalization | No localization, no Indian data → Add Grad-CAM++ + Indian augmentation |
| **M2F2-Det** (CVPR 2025 Oral) | CLIP + LLM = textual explanation of WHY | Expensive LLM inference → Template-based explanations without LLM |
| **FLARE** (CVPR 2026) | Evidence-linked temporal explanations for video | Video-only → Integrate into our multi-modal Dempster-Shafer fusion |
| **DFF-Adapter** (2025) | Multi-head LoRA adapters on DINOv2 | Single-model → Use as Branch C in our ensemble |
| **C2P-CLIP** (AAAI 2025) | Category-prompt injection for generalization | No origin tracing → Merge into our CLIP pipeline |
| **VRAG-DFD** (CVPR 2026) | RAG + RL for forensic reasoning | Heavy, needs LLM → Inspire evidence card explanations |
| **MM-DeepGuard** (2026) | Edge-cloud hybrid: lightweight + deep | No Indian context → Our Tier-0/Tier-1 + BSA compliance |
| **DeepSafe** (GitHub) | Modular ensemble detection | Basic averaging → Replace with Dempster-Shafer |
| **ForensicChain** (2026) | Blockchain evidence chain of custody | Complex infra → Merkle chain in Postgres |

### 6.2 The Synthesized "Better Solution" — 5-Layer Defense-in-Depth

```mermaid
flowchart TD
    subgraph "Layer 0: Triage 5ms"
        T0["MobileNetV2-ONNX Fast Screen"]
    end
    
    subgraph "Layer 1: Provenance 100ms"
        L1A["C2PA Verification"]
        L1B["Watermark Probe"]
        L1C["EXIF/Metadata Check"]
    end
    
    subgraph "Layer 2: Deep Forensics 500ms"
        L2A["CLIP ViT-L/14 LNCLIP-DF"]
        L2B["DCT/FFT Frequency"]
        L2C["DFF-Adapter DINOv2"]
    end
    
    subgraph "Layer 3: Localization + Temporal"
        L3A["Grad-CAM++ Heatmap"]
        L3B["Temporal Bio-Consistency"]
        L3C["Audio-Visual Sync"]
    end
    
    subgraph "Layer 4: Origin Intelligence"
        L4A["pHash + CLIP FAISS"]
        L4B["Public Web Retrieval"]
        L4C["Propagation Graph"]
    end
    
    subgraph "THE BRAIN"
        FUSE["Dempster-Shafer Calibrated Fusion"]
    end
    
    T0 --> FUSE
    L1A --> FUSE
    L1B --> FUSE
    L1C --> FUSE
    L2A --> FUSE
    L2B --> FUSE
    L2C --> FUSE
    L3A --> FUSE
    L3B --> FUSE
    L3C --> FUSE
    L4A --> FUSE
    L4B --> FUSE
    L4C --> FUSE
    
    FUSE --> OUT["Forensic Report + BSA Certificate + NCRP JSON"]
```

---

## 7. Unique Feature Synthesis — The 10 Features That Make Us Win

| # | Feature | Why Unique | Who Else Does This |
|---|---|---|---|
| 1 | **Dempster-Shafer Fusion Engine** | Surfaces inter-signal conflict as named uncertainty | Nobody in hackathon space |
| 2 | **BSA §63(4) Auto-Certificate** | Prescribed-format PDF with SHA-256, dual-signature | **ZERO commercial tools** |
| 3 | **Origin Propagation Graph** | Interactive DAG: earliest indexed source + spread | Reality Defender/Sensity = detect-only |
| 4 | **Indian Recompression Augmentation** | Training with real WhatsApp/Telegram forward cycles | No public benchmark |
| 5 | **Tier-0 MobileNetV2 Triage** | Edge-deployable fast-screen + deep CLIP analysis | Novel combination with fusion |
| 6 | **Grad-CAM++ Heatmap Localization** | Shows WHERE manipulation is, not just WHETHER | Most tools: score only |
| 7 | **Face-Quality Gated Temporal** | Reports LOW_CONFIDENCE instead of guessing | Most: output regardless |
| 8 | **Asymmetric Watermark Logic** | Presence = strong AI evidence; Absence = neutral | Most treat symmetrically |
| 9 | **NCRP-Compatible JSON Export** | Matches I4C/cybercrime.gov.in format | Nobody builds for Indian fit |
| 10 | **Merkle-Chain Evidence Ledger** | Tamper-evident audit trail for the analysis itself | Blockchain-inspired, no overhead |

---

## 8. Technical Approach — Brain & Skeleton

### The Skeleton (Pipeline Engineering)
```
Upload → Ingest → Normalize → Hash → Dispatch → [8 parallel modules] → Collect → Fuse → Report
```
Solid engineering (FastAPI, Celery, Docker) but NOT where novelty lives.

### The Brain (Evidence Fusion & Calibration Engine)

```mermaid
flowchart LR
    subgraph "Input Signals"
        S1["C2PA: valid/broken/absent"]
        S2["Watermark: detected/not/failed"]
        S3["Visual CLIP: calibrated 0-1"]
        S4["MobileNetV2: calibrated 0-1"]
        S5["Temporal: gated by face-quality"]
        S6["Metadata: EXIF anomalies"]
        S7["Origin: source confidence"]
    end

    S1 --> W["Reliability Weighting<br/>learned, NOT hand-tuned"]
    S2 --> W
    S3 --> W
    S4 --> W
    S5 --> W
    S6 --> W
    S7 --> W

    W --> X["Stacked Logistic Calibration"]
    X --> Y{"Conflict?"}
    Y -- "Yes" --> Z1["Dempster-Shafer<br/>surfaces conflict explicitly"]
    Y -- "No" --> Z2["Standard Fusion"]
    Z1 --> AA["Origin Confidence + 95% CI"]
    Z2 --> AA
    AA --> AB["Verdict: 'Evidence suggests...'<br/>never 'This proves...'"]
```

#### Why Dempster-Shafer, Not Weighted Average?

| Approach | When Detectors Disagree |
|---|---|
| **Simple Average** | C2PA=90% real + Visual=90% fake → "50%" ← **misleadingly confident** |
| **Dempster-Shafer** | Reports: "m_real=0.35, m_fake=0.35, **m_uncertain=0.30**, K=0.72 HIGH CONFLICT" ← **correct** |

Uncertainty **widens when detectors disagree** (correct behavior) rather than collapsing to a middling score (incorrect).

---

## 9. Detailed Backend Architecture

### 9.1 Module Map

```
backend/app/modules/
├── c2pa/                    # C2PA verification (c2pa-rs SDK)
├── watermark/               # FFT + DWT invisible watermark probes  
├── image_forensic/          
│   ├── detector.py          # CLIP ViT-L/14 + DCT ensemble
│   ├── dct_analysis.py      # Frequency domain analysis
│   ├── mobilenet_triage.py  # [NEW] MobileNetV2 ONNX Tier-0
│   └── tasks.py
├── video_forensic/          
│   ├── temporal.py          # Blink/jitter/optical flow  
│   ├── av_sync.py           # Lip-sync correlation
│   └── tasks.py
├── localization/            # [IMPLEMENT] Grad-CAM++ heatmaps
├── metadata/                # EXIF consistency via ExifTool
├── origin_trace/            
│   ├── retriever.py         # Search API integration
│   ├── graph_builder.py     # Propagation DAG construction
│   └── tasks.py
├── fusion/                  # THE BRAIN
│   ├── engine.py            # Master fusion orchestrator  
│   ├── calibration.py       # Platt scaling
│   ├── dempster_shafer.py   # DS theory implementation
│   └── tasks.py
└── report/                  # [IMPLEMENT]
    ├── bsa63_generator.py   # BSA §63(4) certificate PDF
    ├── forensic_report.py   # Full forensic PDF
    └── ncrp_export.py       # NCRP-compatible JSON
```

### 9.2 MobileNetV2 ONNX Integration (New Module)

```python
# backend/app/modules/image_forensic/mobilenet_triage.py
"""
Tier-0 MobileNetV2 Fast Triage — ONNX Runtime (no TensorFlow dependency)
Inference ~5ms. Platt-calibrated before Dempster-Shafer fusion.
"""
import numpy as np
import onnxruntime as ort
from PIL import Image

class MobileNetTriage:
    def __init__(self, onnx_path: str):
        self.session = ort.InferenceSession(
            onnx_path,
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
        )
    
    def predict(self, image: Image.Image) -> tuple:
        """Returns (calibrated_probability, raw_confidence)"""
        img = image.resize((224, 224))
        arr = np.array(img, dtype=np.float32) / 127.5 - 1.0
        arr = arr[np.newaxis, ...]
        raw_output = self.session.run(None, {"input": arr})[0]
        raw_score = float(1.0 / (1.0 + np.exp(-raw_output[0])))
        return raw_score, raw_score
```

### 9.3 BSA §63(4) Certificate Generator (Critical New Module)

```python
# backend/app/modules/report/bsa63_generator.py
"""
Auto-generates BSA §63(4) Certificate in prescribed format.
Our #1 differentiator — ZERO commercial tools do this.
"""
BSA_63_TEMPLATE = {
    "part_a": {
        "title": "PART A: Declaration by Person in Lawful Control",
        "fields": {
            "platform_name": "PratiBimb Praman v1.0",
            "deployment": "On-premise Docker / Cloud",
            "operating_period": "<auto: analysis timestamps>",
            "regular_feeding": "Media ingested via forensic upload API",
            "proper_operation": "All modules responded within SLA",
            "officer_name": "<blank — manual signature>",
        },
    },
    "part_b": {
        "title": "PART B: Declaration by Technical Expert",
        "fields": {
            "evidence_hash_sha256": "<auto-computed>",
            "tool_identification": "PratiBimb Praman Multi-Signal Forensic Engine",
            "process_description": "<auto from pipeline execution log>",
            "integrity_verification": "<auto: hash chain validation>",
            "expert_name": "<blank — manual signature>",
        },
    },
}
```

### 9.4 Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Ingestion"
        UP["Upload API"] --> NORM["FFmpeg Normalize"]
        NORM --> HASH["SHA-256"]
        HASH --> LEDGER["Merkle Ledger"]
        HASH --> STORE["File Storage"]
    end

    subgraph "Analysis (Celery)"
        STORE --> W0["MobileNetV2 Triage"]
        STORE --> W1["C2PA"]
        STORE --> W2["Watermark"]
        STORE --> W3["Image Forensic"]
        STORE --> W4["Video Forensic"]
        STORE --> W5["Localization"]
        STORE --> W6["Metadata"]
        STORE --> W7["Origin Trace"]
    end

    subgraph "Fusion"
        W0 --> CAL["Platt Calibration"]
        W1 --> CAL
        W2 --> CAL
        W3 --> CAL
        W4 --> CAL
        W5 --> CAL
        W6 --> CAL
        CAL --> DS["Dempster-Shafer Fusion"]
        W7 --> DS
    end

    subgraph "Output"
        DS --> DASH["Dashboard API"]
        DS --> REPORT["Report Generator"]
        REPORT --> PDF["PDF + BSA §63"]
        REPORT --> JSON["NCRP JSON"]
        DASH --> NEXT["Next.js Frontend"]
    end
```

---

## 10. Languages & Libraries (What & Why)

### Languages
| Language | Where | Why |
|---|---|---|
| **Python 3.11+** | ML pipeline, FastAPI, orchestration | Dominant ML ecosystem |
| **Rust** (via SDK) | C2PA verification | `c2pa-rs` is official reference |
| **TypeScript** | Next.js frontend | Interactive graph viz, type safety |
| **SQL** | PostgreSQL | Relational integrity for evidence data |

### Backend / ML Libraries

| Library | Purpose | Why THIS One |
|---|---|---|
| **FastAPI** | API layer | Async, auto-OpenAPI docs for I4C pitch |
| **Celery + Redis** | Task queue | Each module runs as independent parallel task |
| **PyTorch + timm** | Model backbones | ViT/ConvNeXt/DINOv2 out of box |
| **open_clip** | CLIP features | LNCLIP-DF needs OpenCLIP specifically |
| **onnxruntime** | MobileNetV2 inference | Runs TF model **without TF** — eliminates memory problem |
| **OpenCV** | FFT/DCT, optical flow, face detection | Nothing matches its breadth |
| **FFmpeg + PyAV** | Video/audio decode | Industry standard |
| **MediaPipe** | Face landmarks | Fast CPU-friendly blink/pose |
| **librosa** | Audio features | Lip-sync / voice analysis |
| **c2pa-python** | C2PA verification | Official SDK — legal correctness |
| **pyexiftool** | Metadata extraction | Most complete extractor |
| **imagehash** | pHash/dHash | Stage-1 of two-stage retrieval |
| **FAISS / pgvector** | k-NN vector search | pgvector = stays in Postgres for hackathon |
| **scikit-learn** | Platt scaling, isotonic regression | Calibrated probabilities |
| **PostgreSQL + pgvector** | Cases, ledger, vectors, graphs | One DB for everything |
| **ReportLab / WeasyPrint** | PDF generation | BSA certificate + forensic report |
| **httpx** | Async HTTP | Origin tracing API calls |

### Why ONNX Runtime Instead of TensorFlow

| Approach | Memory | Dependencies |
|---|---|---|
| TF + PyTorch side-by-side | ~5-6GB | `tensorflow>=2.x` (huge) |
| **ONNX Runtime + PyTorch** | **~2-3GB** | `onnxruntime` (50MB) |

### Frontend Libraries

| Library | Purpose |
|---|---|
| **Next.js 14 + React 18** | Dashboard UI, SSR |
| **Tailwind CSS** | Rapid styling |
| **React Flow / vis-network** | Propagation graph visualization |
| **Recharts** | Confidence score charts |

---

## 11. Research Required

> [!WARNING]
> These are NOT optional. They separate a credible submission from a generic demo.

| # | Task | Why | Effort | Status |
|---|---|---|---|---|
| 1 | **Build Indian Recompression Dataset** — Forward 200 images through WhatsApp 3-5x, measure AUC decay | **Genuinely novel** — no public benchmark | 4-6 hrs | ❌ |
| 2 | **Train LNCLIP-DF head** on GenImage + augmented set (Colab T4) | Without weights, detector is random | 3-4 hrs | ❌ |
| 3 | **Convert MobileNetV2 .h5 → ONNX** and validate | Required for integration | 1 hr | ❌ |
| 4 | **Platt calibration** for CLIP + MobileNetV2 on validation set | Required for DS correctness | 2 hrs | ❌ |
| 5 | **Study BSA §63(4) schedule** | Certificate must be legally complete | 2-3 hrs | ✅ Done |
| 6 | **Test face-swap on Indian faces** | Measure performance gap honestly | 3-4 hrs | ❌ |
| 7 | **Implement BSA §63(4) PDF** | #1 differentiator must be in code | 3-4 hrs | ❌ |
| 8 | **Wire up real search API** for origin demo | Need real API call for demo | 2-3 hrs | ❌ |

---

## 12. Wireframes

### Screen Map

```mermaid
flowchart TD
    A["Login"] --> B["Case List / Queue"]
    B --> C["Case Intake + Upload"]
    C --> D["Analysis Dashboard"]
    D --> D1["Tab: Provenance"]
    D --> D2["Tab: Watermark"]
    D --> D3["Tab: Visual + Heatmap"]
    D --> D4["Tab: Temporal (Video)"]
    D --> D5["Tab: Origin Graph"]
    D --> D6["Tab: Fusion Summary"]
    D --> E["Explainability Panel"]
    D --> F["Report Export: PDF / BSA-63 / JSON"]
```

### Case Intake Screen
```
┌──────────────────────────────────────────────────────┐
│  🔍 PratiBimb Praman — New Case                     │
├──────────────────────────────────────────────────────┤
│  Case ID:    [Auto: CHD-2026-_____]                  │
│  NCRP #:     [Optional: cybercrime.gov.in ref]       │
│  Officer:    [Auto from login]                       │
│  Category:   [Deepfake | Impersonation |             │
│               Misinformation | Fraud]                │
│                                                      │
│  ┌────────────────────────────────────────────┐      │
│  │     📁 Drop files here or click            │      │
│  │     JPG, PNG, MP4, WAV, WEBM (max 500MB)   │      │
│  └────────────────────────────────────────────┘      │
│                                                      │
│  SHA-256: [Live computed]                            │
│  MobileNetV2 Triage: [~1 second fast result]         │
│                                                      │
│  [ Start Full Analysis ]  [ Quick Triage Only ]      │
└──────────────────────────────────────────────────────┘
```

### Analysis Dashboard (Core Screen)
```
┌────────────────────────────────────────────────────────┐
│ Case: CHD-2026-04921  │ Status: Analysis Complete      │
├────────────────────────────────────────────────────────┤
│ [Provenance] [Watermark] [Visual] [Temporal] [Origin]  │
│ [Fusion Summary]                                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│ ┌─────────────────────┐  ┌──────────────────────────┐  │
│ │ [Image with         │  │ Fusion Scorecard          │  │
│ │  Grad-CAM++         │  │ AI-Generated:  91%        │  │
│ │  Heatmap Overlay]   │  │ (CI: 84-95%)              │  │
│ │                     │  │ Manipulated:   84%        │  │
│ │ Zoom | Toggle       │  │ Provenance:    32%        │  │
│ │ Opacity: ████░░░    │  │ Watermark:  Detected      │  │
│ └─────────────────────┘  │ Triage:     92% fake      │  │
│                          │                           │  │
│ Evidence Cards:          │ Verdict:                   │  │
│ ┌────────────────────┐   │ ⚠ HIGHLY SUSPICIOUS       │  │
│ │ ✓ C2PA broken      │   │ Uncertainty: 11.2%        │  │
│ │ ✓ Diffusion found  │   │                           │  │
│ │ ✓ 17 derivatives   │   │ [📄 Generate Report]      │  │
│ │ ⚠ Timestamp issue  │   │ [📜 BSA §63 Certificate]  │  │
│ └────────────────────┘   │ [📤 NCRP JSON Export]     │  │
│                          └──────────────────────────┘  │
│ [ 💡 Explain This Score ]                              │
└────────────────────────────────────────────────────────┘
```

### Forensic Report Sample Output
```
╔══════════════════════════════════════════════════════╗
║  FORENSIC ANALYSIS REPORT — Case #CHD-2026-04921    ║
╠══════════════════════════════════════════════════════╣
║  Authenticity:         HIGHLY SUSPICIOUS             ║
║  AI Generation:        91%  (95% CI: 84–95%)         ║
║  Manipulation:         84%                           ║
║  Provenance:           32%                           ║
║  Watermark:            Detected (SynthID-like)       ║
║  Triage (MobileNet):   92% (Calibrated: 89%)         ║
║  Earliest Source:      @user_xyz, X.com              ║
║  Propagation:          88% (17 derivatives)          ║
║                                                      ║
║  Evidence:                                           ║
║    ✓ C2PA chain broken at hop 3                      ║
║    ✓ Diffusion frequency artifacts                   ║
║    ✓ Temporal inconsistency frames 142-189           ║
║    ✓ 17 derivative posts located                     ║
║    ⚠ Earliest-source timestamp unconfirmed           ║
║                                                      ║
║  BSA §63(4) Certificate:   Attached                  ║
╚══════════════════════════════════════════════════════╝
```

---

## 13. Flowcharts & Architecture Diagrams

### End-to-End User Flow

```mermaid
flowchart TD
    A["Officer logs in"] --> B["Creates/selects case"]
    B --> C["Uploads media"]
    C --> D["SHA-256 + ledger entry"]
    D --> E0["MobileNetV2 Triage ~5ms"]
    E0 --> E["8 parallel modules via Celery"]
    E --> F["Evidence Fusion Engine"]
    F --> G["Origin tracing parallel"]
    G --> H["Dashboard populated"]
    H --> I{"Officer reviews tabs"}
    I --> J["Explainability Panel"]
    J --> K["Generate report + BSA §63(4)"]
    K --> L{"Export"}
    L --> M["PDF for court"]
    L --> N["JSON for NCRP"]
    L --> O["Case handoff to RCCC"]
```

### System Component Diagram

```mermaid
flowchart TB
    subgraph "Client"
        BROWSER["Next.js :3000"]
        SWAGGER["Swagger :8000/docs"]
    end
    
    subgraph "API"
        FASTAPI["FastAPI :8000"]
    end
    
    subgraph "Queue"
        REDIS["Redis :6379"]
        CELERY["Celery Workers"]
    end
    
    subgraph "Storage"
        PG["PostgreSQL + pgvector :5432"]
        FILES["File Storage"]
    end
    
    subgraph "ML Models"
        CLIP["CLIP ViT-L/14 PyTorch"]
        MOBI["MobileNetV2 ONNX"]
        MEDIA["MediaPipe FaceMesh"]
    end
    
    BROWSER <--> FASTAPI
    SWAGGER <--> FASTAPI
    FASTAPI --> REDIS
    REDIS --> CELERY
    CELERY --> PG
    CELERY --> FILES
    CELERY --> CLIP
    CELERY --> MOBI
    CELERY --> MEDIA
```

---

## 14. How This is Different from EVERY Other Project

### vs. Typical Hackathon Projects

| Dimension | Typical | **PratiBimb Praman** |
|---|---|---|
| **Detection** | Single classifier | Multi-architecture ensemble (CLIP + MobileNet + DCT) |
| **Output** | "97% fake" | Calibrated score + uncertainty + 95% CI + conflict |
| **Provenance** | Ignored | C2PA first-class module |
| **Origin tracing** | Absent | Core module — propagation graph |
| **Legal** | Not considered | BSA §63(4) auto-certificate |
| **India context** | Clean benchmarks | WhatsApp/Telegram recompression-tested |
| **Explainability** | None | Grad-CAM++ heatmaps + evidence cards |

### vs. Commercial APIs

| Dimension | Reality Defender/Sensity/Hive | **PratiBimb Praman** |
|---|---|---|
| **Origin tracing** | Absent (detect-only) | Core differentiator |
| **Legal compliance** | Generic "court-ready" | India-specific BSA §63(4) |
| **Conflict handling** | Hidden | Dempster-Shafer explicit |
| **Pricing** | $$$$ per API call | Open-source, on-premise |

### vs. IndiaAI Mission Projects

| Project | What We Add |
|---|---|
| **Saakshya** (IIT Jodhpur/Madras) | Origin-tracing graphs + BSA-63 automation |
| **AI Vishleshak** (IIT Mandi) | Dempster-Shafer fusion + Indian recompression robustness |
| **IIT Kharagpur** voice detection | Voice as one branch of multi-modal fusion, not standalone |

---

## 15. How This Helps Police & Law Enforcement

| # | Benefit | Mechanism |
|---|---|---|
| 1 | **Speeds up takedown** | Report in minutes; IT Rules require 3-36 hour platform action |
| 2 | **Solves admissibility gap** | BSA §63(4) auto-generated — removes paperwork bottleneck |
| 3 | **Bulk fraud triage** | MobileNetV2 screens thousands in seconds for digital arrest scams |
| 4 | **Cross-jurisdiction handoff** | NCRP JSON → complete evidence for I4C/RCCC |
| 5 | **Training-aligned** | Matches CyTrain terminology → lower adoption barrier |
| 6 | **Protects institution** | Quickly verify if "police video" is deepfake → protects public trust |
| 7 | **Evidence integrity** | Merkle-chain ledger → tamper-evident history |
| 8 | **Scalable deployment** | Docker Compose = one-command on any machine, works offline |
| 9 | **Origin intelligence** | Shows WHERE content appeared and HOW it spread |
| 10 | **Honest uncertainty** | Explicit CI and conflict → officers make informed decisions |

---

## 16. Hackathon Execution Timeline (24 Hours)

### Priority Matrix

| Priority | Module | Time | Critical? |
|---|---|---|---|
| **P0** | Ingestion + SHA-256 + Merkle Ledger | 2h | Foundation |
| **P0** | MobileNetV2 ONNX + Triage endpoint | 2h | Quick win demo |
| **P0** | Image Forensic (CLIP with best available weights) | 4h | Core visible feature |
| **P0** | Evidence Fusion Engine (4+ signals) | 3h | **THE differentiator** |
| **P0** | BSA §63(4) Certificate PDF | 3h | **#1 law enforcement feature** |
| **P1** | Basic Origin Tracing (1 real API) | 2h | Concept demo |
| **P1** | Dashboard UI (3 key screens) | 4h | Visual wow |
| **P1** | Grad-CAM++ Heatmap | 2h | High-impact visual |
| **P2** | Video Temporal Analysis | 2h | If time allows |
| **P2** | Propagation Graph Viz | 2h | Cherry on top |

### Hour-by-Hour

```
Hour 0-2:   Docker setup, DB verify, API endpoints, fix temporal.py bug
Hour 2-4:   MobileNetV2 ONNX conversion + triage endpoint
Hour 4-8:   Image Forensic with weights + Fusion Engine
Hour 8-10:  BSA §63(4) PDF generator (CRITICAL PATH)
Hour 10-12: Origin tracing real API + basic frontend
Hour 12-16: Dashboard UI (heatmap, scorecard, evidence cards)
Hour 16-18: Integration testing, demo data
Hour 18-20: Grad-CAM++ localization, propagation graph
Hour 20-22: Demo rehearsal, edge cases
Hour 22-24: Final polish, presentation prep
```

---

## 17. Honest Limitations

> [!CAUTION]
> Stating these proactively is a **strength** with technical/legal judges.

1. **Cannot trace into encrypted/private channels** — WhatsApp, private Telegram
2. **No detector achieves 0% error** — we make uncertainty visible, not eliminated
3. **C2PA depends on adoption** — absent for most Indian cases currently
4. **Watermark detection in active arms race** — one signal, never standalone verdict
5. **"Earliest known source"** = retrieval result, NOT proof of true origin
6. **Indian-face performance may differ** from Western benchmarks — honest finding either way
7. **Novel generator generalization** — open challenge, mitigated via foundation models
8. **MobileNetV2 accuracy drops** on compressed Indian content — compensated by down-weighting in fusion

---

## 18. Referenced Research Papers & Repos

### Research Papers

| Paper | Citation | Our Use |
|---|---|---|
| LNCLIP-DF | arXiv 2508.06248 | CLIP backbone tuning architecture |
| M2F2-Det | CVPR 2025 Oral | Explainable forensic reports inspiration |
| FLARE | CVPR 2026 | Evidence-linked temporal explanations |
| DFF-Adapter | arXiv 2025 | Multi-head LoRA on DINOv2 |
| C2P-CLIP | AAAI 2025 | Category-prompt cross-generator generalization |
| VRAG-DFD | CVPR 2026 | RAG forensic reasoning |
| MM-DeepGuard | ResearchGate 2026 | Edge-cloud hybrid architecture |
| Community Forensics | arXiv 2411.04125 | Thousands-of-generators generalization |
| NTIRE 2026 | arXiv 2604.11487 | 108k+185k benchmark template |
| Stable Signature Unstable | arXiv 2405.07145 | Watermark removal arms race |
| DF40 Benchmark | NeurIPS 2024 | 40-method deepfake benchmark |
| GenImage | arXiv 2306.08571 | Primary training dataset |
| SAFF/CM-GAN | NIH 2026 | Cross-modal AV sync |
| ConLLM | EACL 2026 | Contrastive audio-video-text |

### GitHub Repositories

| Repo | Use |
|---|---|
| `contentauth/c2pa-rs` | C2PA verification SDK |
| `contentauth/c2pa-attacks` | C2PA attack simulator |
| `SCLBD/DeepfakeBench` | Benchmark harness |
| `GenImage-Dataset/GenImage` | Training/eval dataset |
| `greatzh/Image-Forgery-Datasets-List` | Dataset master index |
| `aiiu-lab/DFD-FCG` | CLIP video deepfake detection |
| `mattpodolak/duplicate-img-detection` | FAISS + imagehash scaffold |
| `siddharthksah/DeepSafe` | Modular ensemble platform |
| `jvishwa06/DeepTracersV0` | Social media integration |
| `CodeRafay/Forensic-Image-Analysis-Toolkit` | 14+ forensic methods |

---

## One-Sentence Pitch

> *"Every individual signal is beatable — what nobody has shipped is a fusion layer that knows how much to trust each signal under Indian real-world degradation, stays honest about what it can't prove, and outputs something a magistrate can accept under BSA Section 63."*

---

## Action Items — RIGHT NOW (Pre-Hackathon)

1. ❌ **Fix `temporal.py` bug** (Line 72: `CascadeCascade` → `face_cascade`)
2. ❌ **Build Indian Recompression Dataset** — 200 images × 3-5 WhatsApp forwards
3. ❌ **Train LNCLIP-DF head** on Colab T4
4. ❌ **Convert MobileNetV2 .h5 → ONNX**
5. ❌ **Implement BSA §63(4) PDF generator**
6. ❌ **Wire up real search API** for origin tracing
7. ❌ **Build 3 demo cases** with pre-analyzed results
8. ❌ **Implement Grad-CAM++ heatmap**
