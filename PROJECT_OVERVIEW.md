# PratiBimb Praman — Complete Project Overview
### प्रतिबिम्ब प्रमाण | AI Media Forensic Provenance & Origin Intelligence Platform
**Chandigarh Police National Hackathon 2026 — Track 4: AI-Generated/AI-Altered Media Detection**

---

## 1. Problem Statement

> **"Development of an AI-Powered Digital Forensic Platform to Detect AI-Generated or Manipulated Images and Videos, Verify Their Authenticity, and Trace Their Origin and Dissemination Across Social Media."**

### What the Problem Actually Contains (8 Distinct Challenges)

Most teams treat this as a single binary classification problem. The problem statement is actually 8 distinct technical challenges stacked together:

| Layer | Challenge |
|---|---|
| **Detection** | Detect fully AI-generated media (Midjourney, DALL-E, Stable Diffusion, Sora) |
| **Detection** | Detect AI-manipulated media — partial fakes: face-swap, inpainting, voice-cloning |
| **Detection** | Detect conventionally edited media — Photoshop splicing, copy-move, retouching |
| **Detection** | Correctly identify authentic, unmodified media |
| **Verification** | Verify cryptographic provenance (C2PA Content Credentials, watermarks) |
| **Verification** | Establish chain-of-custody — tamper-evident audit trail from ingestion to report |
| **Tracing** | Find the earliest indexed instance of media across the open web |
| **Tracing** | Reconstruct dissemination graph — which accounts, which platforms, what transformations |

### Why This Is Hard in India Specifically

```
Original AI-Generated Image
        |
        ▼ WhatsApp Forward #1 (JPEG Q ~72)
        |
        ▼ WhatsApp Forward #2 (JPEG Q ~55)
        |
        ▼ Screenshot + Telegram Share (PNG → JPEG Q ~45)
        |
        ▼ Instagram Repost (JPEG Q ~38)
        |
        ▼ WhatsApp Forward Again (JPEG Q ~28)
        |
        ▼
What the Investigator Receives: ~20% of original quality
```

- **WhatsApp aggressively recompresses** every send — content forwarded 5+ times loses the very frequency/texture artifacts that AI detectors rely on.
- **C2PA Content Credentials**: Near-zero adoption on Indian devices/platforms. Missing credentials ≠ fake.
- **Vernacular content** (Hindi/Punjabi overlays, Telegram meme composites) is absent from all Western benchmarks.
- **WhatsApp is E2E encrypted** — private groups legally cannot be scraped.
- **Indian face/skin-tone gap** — major datasets (DFDC, Celeb-DF) are overwhelmingly Western faces.

### Indian Scale (Verified Data, 2025-2026)

| Metric | Data |
|---|---|
| Cyber fraud losses | ₹52,976 crore over 6 years |
| Digital arrest scam losses alone | ₹22,495 crore in 2025 |
| NCRP complaint surge | 2.6 lakh (2021) → 24 lakh (2025) — 9× growth |
| Voice clone victimization | 47% of Indian adults (nearly 2× global average) |
| I4C interventions | ₹11,000+ crore saved via CFCFRMS |

---

## 2. Our Core Concept: Evidence Fusion, Not Another Classifier

> **"Every individual forensic signal is beatable. The novelty is the fusion layer that knows exactly how much to trust each signal under Indian real-world degradation, stays honest about uncertainty, and outputs something a magistrate can accept."**

### What Makes Us Different

| Dimension | Typical Team | Commercial APIs (Reality Defender, Sensity, Hive) | **PratiBimb Praman** |
|---|---|---|---|
| **Output** | Single score | Calibrated score | **Multi-signal fused score + explicit uncertainty + conflict surfacing** |
| **Provenance (C2PA)** | Ignored | Not a focus | **First-class module; absence ≠ fake enforced in code** |
| **India robustness** | Clean benchmark accuracy | Not published | **Dynamic DCT down-weighting for WhatsApp recompression chains** |
| **Legal admissibility** | Not considered | Generic "court-ready" | **Auto-generated BSA §63(4) certificate — India-specific law** |
| **Origin tracing** | Absent | Absent | **Core module — pHash + CLIP FAISS propagation graph** |
| **Explainability** | None | Score only | **Grad-CAM heatmaps, evidence cards, ELA overlays, bounding boxes** |
| **Uncertainty** | Hidden | Rarely stated | **Dempster-Shafer conflict mass explicitly surfaced** |
| **Document forensics** | Not considered | Not considered | **Font stroke-width analysis for marksheet/ID card tampering** |
| **AV sync (voice clone)** | Not considered | Separate tools | **Integrated AV correlation targeting "Digital Arrest" scams** |

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INVESTIGATOR BROWSER                          │
│                  Next.js 14 + TypeScript Dashboard                   │
│         (Case Intake → Live Analysis → Evidence Tabs → PDF Export)   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTP / REST API (port 3000 → 8000)
┌──────────────────────────────▼──────────────────────────────────────┐
│                    FastAPI BACKEND (port 8000)                        │
│  /api/v1/cases   /api/v1/analysis   /api/v1/reports   /health        │
└──────┬──────────────────────────┬───────────────────────────────────┘
       │                          │
       │ Async DB (asyncpg)        │ Triggers Celery Chord
┌──────▼──────┐          ┌────────▼──────────────────────────────────┐
│ PostgreSQL  │          │             REDIS MESSAGE BROKER            │
│  + pgvector │          │              (port 6379)                    │
│  (port 5432)│          └────────┬───────────────────────────────────┘
│             │                   │ Celery Workers consume tasks
│  Tables:    │          ┌────────▼───────────────────────────────────┐
│  cases      │          │         PARALLEL FORENSIC MODULES           │
│  media_items│          │  ┌────────────┐ ┌──────────────────────┐   │
│  analysis_  │          │  │ C2PA       │ │ Watermark Detector    │   │
│   results   │          │  │ Verifier   │ │ (FFT/SynthID probe)   │   │
│  ledger     │          │  └────────────┘ └──────────────────────┘   │
│  evidence_  │          │  ┌────────────┐ ┌──────────────────────┐   │
│   graph     │          │  │ CLIP ViT + │ │ MobileNetV2 ONNX     │   │
│             │          │  │ DCT Fusion │ │ (Tier-0 Triage 5ms)  │   │
└──────┬──────┘          │  └────────────┘ └──────────────────────┘   │
       │                 │  ┌────────────┐ ┌──────────────────────┐   │
       │                 │  │ Video      │ │ AV-Sync / Voice      │   │
       │                 │  │ Temporal   │ │ Clone Detector       │   │
       │                 │  └────────────┘ └──────────────────────┘   │
       │                 │  ┌────────────┐ ┌──────────────────────┐   │
       │                 │  │ ELA +      │ │ EXIF/Metadata        │   │
       │                 │  │ Noise      │ │ Consistency Check    │   │
       │                 │  │ Heatmap    │ └──────────────────────┘   │
       │                 │  └────────────┘                            │
       │                 │  ┌────────────┐ ┌──────────────────────┐   │
       │                 │  │ pHash+FAISS│ │ Document Font        │   │
       │                 │  │ Origin     │ │ Stroke Analysis      │   │
       │                 │  │ Tracing    │ │ (ID/Marksheet fraud) │   │
       │                 │  └────────────┘ └──────────────────────┘   │
       │                 └────────────┬───────────────────────────────┘
       │                              │ Chord callback
       │                    ┌─────────▼──────────────────────────────┐
       │                    │     EVIDENCE FUSION ENGINE              │
       │                    │  Platt Calibration → Dempster-Shafer   │
       │                    │  Conflict Detection → Confidence CI     │
       │                    └─────────┬──────────────────────────────┘
       │                              │
       └──────────────────────────────▼
                        ┌─────────────────────────────┐
                        │     PDF REPORT GENERATOR     │
                        │  BSA §63(4) Certificate      │
                        │  NCRP JSON Export            │
                        └─────────────────────────────┘
```

---

## 4. Complete Backend Module Map

### Module: `services/ingestion.py` — Media Ingestion & Hashing
**What it does:** The first thing that happens when a file is uploaded.
1. Computes **SHA-256 cryptographic hash** of the raw file bytes — the immutable fingerprint
2. Estimates **JPEG quality factor** from JPEG quantization tables (feeds DCT weighting)
3. Computes **pHash** (perceptual DCT hash) and **dHash** (difference hash) via `imagehash`
4. Computes **768-dim CLIP ViT-L/14 embedding** for semantic vector search
5. Extracts EXIF metadata
6. Writes the first **Merkle-chain ledger entry** (`LedgerAction.INGEST`)
7. Saves file to disk, creates DB record, triggers Celery pipeline

### Module: `services/ledger_service.py` — Chain-of-Custody Audit Trail
**What it does:** Creates a Blockchain-style (Merkle-chain) append-only evidence log.

Each entry's hash is computed as:
```python
SHA256(prev_hash | action | media_sha256 | timestamp | details)
```
Any retroactive modification to any entry in the log breaks all subsequent hashes — cryptographically detectable tampering. This is the **foundation of BSA §63(4) compliance**.

### Module: `services/pipeline.py` — Celery Chord Orchestration
**What it does:** Dispatches all forensic modules in **parallel** using a Celery `chord`.

```python
parallel_forensics = group(
    task_verify_c2pa,          # C2PA provenance check
    task_detect_watermark,     # Invisible watermark probe
    task_analyze_image,        # CLIP ViT-L/14 + DCT ensemble
    task_mobilenet_triage,     # MobileNetV2 ONNX (5ms Tier-0)
    task_analyze_video,        # Temporal + AV sync
    task_localize_manipulation, # ELA + noise heatmap
    task_check_metadata,       # EXIF consistency
    task_trace_origin,         # pHash + FAISS retrieval
    task_analyze_document,     # Font stroke analysis
)
# When ALL parallel tasks finish → fusion engine fires automatically
chord(parallel_forensics)(task_run_evidence_fusion)
```

Includes **ThreadPoolExecutor fallback** if Celery/Redis is unavailable — zero-config local dev.

---

## 5. Detection Modules — How We Detect Each Threat

### 5.1 AI-Generated Image Detection
**File:** `modules/image_forensic/detector.py`

**Two-Branch Hybrid Ensemble:**

```
Image Input
    │
    ├── Branch A: CLIP ViT-L/14 (Foundation Model — Semantic Features)
    │   • Frozen pre-trained vision transformer (openai/ViT-L-14)
    │   • Optional LightweightForensicHead on top (LayerNorm → Linear 768→256→1)
    │   • Hyperspherical feature normalization (L2-normalize before classification)
    │   • Captures GLOBAL semantic inconsistencies (proportions, physics, text)
    │   • Falls back to Laplacian variance heuristic if weights missing
    │
    └── Branch B: DCT Frequency Domain Analysis
        • 8×8 block DCT — measures high-frequency AC coefficient energy
        • 2D FFT spectral noise ratio — detects GAN checkerboard artifacts
        • JPEG 8-pixel block boundary ratio — catches copy-paste misalignment
        • Captures LOCAL pixel/texture-level artifacts
        │
        └── Dynamic Weight (KEY INDIA FEATURE):
            JPEG Quality > 65  → weight = 1.00 (full trust)
            JPEG Quality 40-65 → weight = 0.60 (moderate trust)
            JPEG Quality < 40  → weight = 0.25 (heavy WhatsApp degradation)
```

**Why CLIP?** CLIP was trained on 400M image-text pairs. When fine-tuned with only LayerNorm layers (LNCLIP-DF, arXiv:2508.06248), it achieves state-of-the-art generalization to *unseen* generators. A detector trained on Stable Diffusion still detects Midjourney because CLIP features are generator-agnostic semantic representations.

**Why DCT?** GAN/diffusion generators leave characteristic spectral artifacts — regular grid patterns in the Fourier spectrum, abnormal AC coefficient distributions. These are invisible to the human eye but visible in frequency space.

**Why the dynamic DCT weight?** Without it, a REAL photo forwarded 5× on WhatsApp would be falsely flagged as AI-generated because WhatsApp recompression destroys the same high-frequency signal the detector expects from AI images. This is an original contribution addressing the Indian recompression problem.

---

### 5.2 AI-Generated Image Detection — Tier-0 Triage
**File:** `modules/image_forensic/mobilenet_triage.py`

**What it does:** Runs MobileNetV2 in ONNX format via `onnxruntime` — executes in ~5ms on CPU, <1ms on GPU. Used as a fast pre-filter before the expensive CLIP inference.

**Why two models?**
- MobileNetV2 (CNN) → captures **LOCAL texture/pixel artifacts** (stroke inconsistency, compression boundaries)
- CLIP ViT (Transformer) → captures **GLOBAL semantic inconsistencies** (physics, lighting, anatomy)
- Together they form a **dual-architecture ensemble** — an adversary must fool both CNN-level and Transformer-level features simultaneously (different attack surfaces)

**Design rules enforced in code:**
- MobileNetV2 confidence is **capped at 0.75** in the fusion engine — CNN triage is never given more weight than CLIP
- Returns `0.5` with `confidence=0` when ONNX model file is missing — no false alarms

---

### 5.3 Manipulation / Splicing Detection & Localization
**File:** `modules/localization/gradcam.py`

**Three-layer spatial analysis:**

**1. Error Level Analysis (ELA)**
```
Original JPEG → Re-save at Q=75 → Compute pixel difference → Amplify
```
Authentic images: uniform compression history → LOW standard deviation in ELA residual
Spliced/tampered regions: different compression history → HIGH standard deviation at boundaries

**2. Noise Inconsistency Map (SRM-style)**
Computes Laplacian of Gaussian — measures second-order pixel discontinuity. Copy-pasted regions from different sources have different noise profiles → bright spots in the noise map.

**3. Composite Heatmap + Bounding Boxes**
ELA + Noise maps fused with `cv2.addWeighted`, blurred, thresholded, and contours extracted:
```python
cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
Each suspicious region returns: pixel bounding box, area percentage, anomaly intensity.

**Why this matters:** "Is it fake?" is not enough for court. "**Where** was it tampered?" is what a forensic examiner needs to present evidence.

---

### 5.4 Video Deepfake Detection — Temporal Analysis
**File:** `modules/video_forensic/temporal.py`

**Three biological consistency signals:**

**1. Facial Trajectory Jitter**
Tracks face centroid across 36 keyframes. Computes second-order derivative (acceleration) of face position trajectory. Face-swapped / reenacted videos exhibit **unnatural jitter** — the swapped face moves slightly independently of the head.
```python
velocities = np.diff(face_positions, axis=0)
accelerations = np.diff(velocities, axis=0)
jitter_score = np.mean(np.std(accelerations, axis=0))
```

**2. Optical Flow Consistency**
Farneback dense optical flow between consecutive frames. Real faces exhibit smooth, biologically consistent motion. DeepFake generators often produce subtle temporal discontinuities at face boundaries.

**3. Face Quality Gate (Critical Design Rule)**
If detected face < 60px or not detected consistently:
```python
return 0.50, 0.30, {"quality_gate": "LOW_RESOLUTION"}, "Face resolution below threshold"
```
**Explicitly refuses to guess** when confidence is insufficient — never outputs a falsely confident verdict on a degraded WhatsApp video.

---

### 5.5 Voice Clone / Audio-Visual Sync Detection
**File:** `modules/video_forensic/av_sync.py`

**Targets "Digital Arrest" Scam Videos** — where a fraudster's cloned voice is dubbed over a fabricated government official video.

**How it works:**
1. Extracts audio with `librosa` (16kHz, 15s window)
2. Computes RMS energy envelope + onset strength (speech activity detection)
3. Extracts mouth region bounding boxes using `cv2.CascadeClassifier` across frames
4. Measures cross-correlation between audio speech energy and visual mouth opening dynamics
5. Natural speech: mouth moves **in sync** with audio onsets → high correlation
6. Voice clone over a different video: mouth motion **leads or lags** audio → low correlation → desync score

---

### 5.6 Document Forensic — Font Stroke Analysis
**File:** `modules/document_forensic/font_analysis.py`

**Targets:** Tampered marksheets, ID cards, affidavits, Aadhaar cards

**How copy-paste text tampering is detected:**

**Step 1: Text Gate** — Skips photos/natural images. Only runs if ≥25 text-like contour regions detected (prevents false positives on portraits).

**Step 2: Stroke Width via Distance Transform**
```python
dist_transform = cv2.distanceTransform(binary_text_region, cv2.DIST_L2, 5)
avg_stroke_width = np.mean(dist_transform[dist_transform > 0]) * 2
```
Authentic documents printed from one source: **uniform stroke widths** (low variance)
Copy-pasted text from different fonts/printers: **mixed stroke widths** (high variance → tamper signal)

**Step 3: Background Brightness Consistency**
Checks if background luminance is consistent across text regions. A genuine certificate printed uniformly should have the same background across all text areas. Paste-in text from a scan/screenshot shows luminance discontinuities.

---

### 5.7 C2PA Content Credentials Verification
**File:** `modules/c2pa/verifier.py`

**Four-state output (never binary):**
- `VALID_PROVENANCE` → Cryptographically signed chain intact → Strong authenticity evidence
- `BROKEN_CHAIN` → Manifest present but signature invalid → **Strong manipulation evidence**
- `NO_CREDENTIALS` → **NEUTRAL** — not evidence of anything in the Indian context
- `UNSUPPORTED_FORMAT` → Cannot check

**Critical design rule enforced in code and fusion engine:**
> `NO_CREDENTIALS` NEVER pushes the fusion score toward 'Fake'. In India, 95%+ of social media re-shares strip all metadata by the 3rd or 4th forward. Absence of credentials is the default state.

Also performs **binary file header scan** for JUMBF metadata boxes (`c2pa`, `jumd`, `c2ma` magic bytes) even without `c2patool` installed.

---

### 5.8 Invisible Watermark Detection
**File:** `modules/watermark/detector.py`

**Targets:** Google SynthID, Meta Stable Signature, Tree-Ring watermarks

**How it works:**
1. **2D FFT spectral analysis** — SynthID embeds patterns in the frequency domain. These appear as abnormal periodic spikes in the magnitude spectrum.
2. **Spike significance metric:**
```python
spike_significance = (max_spike - high_freq_energy) / (std_dev + 1e-5)
# Threshold > 4.2 → watermark detected
```
3. **Rotational asymmetry check** — Tree-Ring watermarks show specific radial patterns.

**Asymmetric evidence rule (honest design):**
- Watermark `DETECTED` → Strong evidence of AI generation (95% confidence mass)
- Watermark `NOT_DETECTED` → **Near-neutral** (could be real OR watermark removed by open-source tools)

---

### 5.9 EXIF / Metadata Consistency Analysis
**File:** `modules/metadata/exif_check.py`

Checks for contradictions between EXIF claims and image reality:
- Camera make/model present but GPS coordinates impossible
- Software field contains known AI generator names (`Stable Diffusion`, `MidJourney`, `DALL-E`)
- Timestamp inconsistencies between EXIF DateTime and FileModifyDate
- Thumbnail embedded in EXIF doesn't match main image (classic tampering indicator)

---

### 5.10 Origin Tracing — Two-Stage Retrieval
**File:** `modules/origin_trace/retriever.py` + `retriever_internal.py`

**Stage 1 (Fast Filter): pHash Hamming Distance**
```python
hamming_distance = int(imagehash.hex_to_hash(h1) - imagehash.hex_to_hash(h2))
# Threshold: < 10 bits → near-duplicate (resilient to JPEG recompression)
```

**Stage 2 (Semantic Matching): CLIP Embedding + FAISS Cosine Similarity**
```python
cosine_sim = dot(a, b) / (norm(a) * norm(b))
# Threshold: > 0.85 → semantic match (survives crops, filters, color changes, mirroring)
```

**Why two stages?** pHash breaks under extreme crops/color changes. CLIP embeddings are semantically meaningful — they match content, not pixels. But CLIP is expensive; pHash is O(1). Two-stage: pHash pre-filters candidates, CLIP verifies them.

**What it finds:** Any previously ingested media in the database that matches the current submission. If "Case 1" was the original AI-generated image and "Case 2" is a cropped + filtered version, the system finds the link and builds a propagation edge.

**Honest limitation:** External social media crawling (X/Twitter, public Telegram) requires API keys and is currently architected as a stub. WhatsApp is E2E encrypted and cannot be legally crawled. We say "earliest **indexed** source," never "proven origin."

---

## 6. Evidence Fusion Engine — The Brain

**File:** `modules/fusion/engine.py` + `dempster_shafer.py` + `calibration.py`

### Step 1: Platt Scaling Calibration
**File:** `modules/fusion/calibration.py`

Problem: CLIP outputs "0.8" and Watermark outputs "0.8" but they don't mean the same empirical probability. Without calibration, naive averaging is misleading.

**Solution — Per-module Platt Scalers:**
```python
P(Y=1|s) = 1 / (1 + exp(A*s + B))
```
Each forensic module has its own fitted `(A, B)` parameters, ensuring "0.8" means the same probability of synthetic origin regardless of which module produced it.

### Step 2: Dempster-Shafer Theory — Why Not Weighted Average?

**Frame of Discernment:** Θ = {Real, Fake, Uncertain}

Each forensic signal contributes a **belief mass assignment**:
```python
BeliefMass(m_real=0.85, m_fake=0.05, m_uncertain=0.10)  # e.g. valid C2PA
BeliefMass(m_real=0.05, m_fake=0.80, m_uncertain=0.15)  # e.g. SynthID watermark detected
```

**Dempster's Combination Rule:**
```
K = m1(Real)×m2(Fake) + m1(Fake)×m2(Real)   [conflict mass]
m(Real) = [m1(Real)×m2(Real) + m1(Real)×m2(Uncertain) + m1(Uncertain)×m2(Real)] / (1-K)
m(Fake) = [m1(Fake)×m2(Fake) + m1(Fake)×m2(Uncertain) + m1(Uncertain)×m2(Fake)] / (1-K)
```

**Why is this better than weighted average?**

| Scenario | Weighted Average | Dempster-Shafer |
|---|---|---|
| C2PA says REAL (95%), Visual says FAKE (90%) | Reports 52.5% — a misleading near-neutral | Reports HIGH conflict (K > 0.40), widens uncertainty band, flags for human review |
| All signals agree on FAKE | Correctly reports high fake probability | Also correctly reports high fake probability |
| Few signals available | Averages with zeros → underestimates confidence | High `m_uncertain` → explicitly reports low confidence |

**Output:**
```
Forensic Assessment: HIGHLY SUSPICIOUS (Likely AI-Generated / Manipulated)
AI Generation Probability: 91% (95% CI: 84% – 95%)
Uncertainty Band: 8.2%
Signal Conflict K: 0.12 (LOW)

Evidence:
✓ Cryptographic C2PA provenance verified (absent — neutral for Indian social forward)
✓ Synthetic watermark signature detected (SynthID/Tree-Ring)
✓ Visual/frequency anomalies indicate synthetic generation (87%)
✓ MobileNetV2 CNN triage: 82% tampered (fast Tier-0 screen)
✓ Natural facial movement preserved (video temporal consistent)
```

### Step 3: 95% Confidence Interval
```python
uncertainty_spread = fused_mass.m_uncertain * 0.25
ci_lower = max(0.01, fused_ai_prob - uncertainty_spread)
ci_upper = min(0.99, fused_ai_prob + uncertainty_spread)
```

---

## 7. Legal Compliance: BSA §63(4) Certificate

**File:** `services/report_generator.py`

### The Legal Requirement (Bharatiya Sakshya Adhiniyam, 2023)

BSA Section 63 replaced the Indian Evidence Act's §65B on July 1, 2024. Electronic evidence submitted in Indian courts now requires a **dual-certification certificate**:

```
┌─────────────────────────────────────────────────────┐
│  BSA Section 63(4) Certificate — DUAL CERTIFICATION │
├─────────────────────────────────────────────────────┤
│  PART A: Person in lawful control of device/data    │
│    - Device details (Make, Model, Serial)           │
│    - Operating conditions during material period    │
│    - Attestation of faithful/accurate output        │
│                                                     │
│  PART B: Independent technical expert               │
│    - Technical verification of integrity            │
│    - SHA-256 hash of evidence (mandatory)           │
│    - Tool/software identification                   │
│    - Process description                            │
└─────────────────────────────────────────────────────┘
```

**PratiBimb Praman auto-generates this certificate using ReportLab:**
- Part A fields: populated from the case officer record
- Part B fields: populated from the analysis log — SHA-256 hash, analysis tool names, process description
- Signature lines: left blank for human signatures
- Hash-chain verification: included as an appendix

**No commercial deepfake detector (Reality Defender, Sensity, Hive, Intel FakeCatcher) generates this certificate. This is our single strongest legal differentiator.**

---

## 8. Technology Stack & Libraries — Full Rationale

### Backend Languages & Framework

| Technology | Purpose | Why This One |
|---|---|---|
| **Python 3.11** | Core ML and API | Dominant ML ecosystem; all critical libraries are Python-first |
| **FastAPI** | REST API layer | Async-first, auto-generates OpenAPI/Swagger docs, Pydantic validation |
| **SQLAlchemy 2.0** | ORM (async) | Async-native with `asyncpg`, clean ORM for complex queries |
| **PostgreSQL 16 + pgvector** | Primary database + vector search | JSONB for flexible details, pgvector extension for CLIP embedding nearest-neighbour |
| **Celery 5 + Redis** | Distributed task queue | Industry-standard for parallel forensic pipeline; `chord` primitive maps exactly to "run all, then fuse" pattern |

### ML / AI Libraries

| Library | Module It Powers | Why This One |
|---|---|---|
| **open-clip-torch 2.29** | Image forensic detector | Provides ViT-L/14 with frozen pre-trained weights; more flexible than HuggingFace for custom heads |
| **PyTorch 2.5** | CLIP inference, forensic head | Standard deep learning framework; CUDA support for GPU acceleration |
| **onnxruntime 1.20** | MobileNetV2 Tier-0 triage | Eliminates TensorFlow dependency; cross-platform; ~5ms inference on CPU |
| **scikit-learn** | Platt calibration scalers | Proven calibration implementations (LogisticRegression, IsotonicRegression) |
| **timm 1.0** | Model backbone registry | Access to 700+ pretrained vision models if CLIP is swapped out |
| **transformers 4.47** | Optional DINOv2 backbone | HuggingFace hub access if switching away from OpenCLIP |

### Computer Vision Libraries

| Library | Module It Powers | Why This One |
|---|---|---|
| **OpenCV (headless) 4.10** | DCT, FFT, ELA, optical flow, cascade classifier | The standard CV library; `cv2.dct()`, `cv2.calcOpticalFlowFarneback()`, `cv2.CascadeClassifier()` |
| **Pillow 11.1** | Image loading, ELA re-save, format handling | PIL provides `ImageChops.difference()` used directly in ELA computation |
| **imagehash 4.3** | pHash and dHash computation | Simple, battle-tested; Hamming distance via `h1 - h2` operator |
| **MediaPipe 0.10** | Face landmark tracking | Google's cross-platform, CPU-friendly face mesh for biological consistency analysis |
| **faiss-cpu 1.9** | CLIP embedding nearest-neighbour | Efficient vector similarity search; cosine index for 768-dim embeddings |

### Media Processing Libraries

| Library | Module It Powers | Why This One |
|---|---|---|
| **PyAV 14.0** | Video decode and audio extraction | Python bindings for FFmpeg; handles all container formats (MP4, MKV, WEBM) |
| **librosa 0.10** | Audio AV sync analysis | Industry-standard audio feature extraction; RMS energy, onset strength, MFCC |
| **soundfile 0.13** | Audio I/O | Low-level audio file reading for `librosa.load()` backend |

### Metadata & Provenance Libraries

| Library | Module It Powers | Why This One |
|---|---|---|
| **pyexiftool 0.5** | EXIF deep extraction | Wraps Phil Harvey's ExifTool — most complete EXIF reader, handles 200+ formats |
| **exifread 3.0** | JPEG thumbnail offset detection | Lightweight; checks if embedded thumbnail differs from main image |
| **c2patool** (subprocess) | C2PA manifest verification | Official reference CLI from `contentauth` — correctness over convenience |

### Report Generation

| Library | Module It Powers | Why This One |
|---|---|---|
| **ReportLab 4.2** | BSA certificate and forensic PDF | Production-grade Python PDF library; precise layout control needed for legal documents |
| **Jinja2 3.1** | NCRP JSON template formatting | Standard Python templating |

### Frontend Stack

| Technology | Purpose | Why This One |
|---|---|---|
| **Next.js 14 (App Router)** | Dashboard framework | Server components, fast routing, React 18 concurrent features |
| **TypeScript** | Type safety across all frontend | Catches API contract mismatches at compile time |
| **Tailwind CSS** | Styling | Rapid iteration under hackathon time pressure |
| **Lucide React** | Icon set | Consistent, lightweight icon library |
| **Recharts / Chart.js** | Radar chart for fusion scores, confidence gauges | Clean defaults, responsive |

### Infrastructure

| Technology | Purpose | Why This One |
|---|---|---|
| **Docker Compose** | Multi-service orchestration | Single `docker-compose up` starts Postgres + pgvector + Redis + Backend + Celery + Frontend |
| **pgvector/pgvector:pg16** | PostgreSQL image | Official pgvector image with extension pre-installed |
| **redis:7-alpine** | Message broker | Minimal image; Celery uses it as both broker and result backend |

---

## 9. Complete Flowcharts

### 9.1 End-to-End User Flow

```
👮 Officer Opens Dashboard
         │
         ▼
Creates New Case
(Case Number: CHD-2026-XXXXXX, NCRP Link, Category, Officer Name)
         │
         ▼
Uploads Media File (Image / Video / Audio / Document)
         │
         ▼
         ┌─────────────────────────────────────┐
         │          INGESTION SERVICE           │
         │  1. Read bytes                       │
         │  2. SHA-256 hash                     │
         │  3. JPEG quality estimation          │
         │  4. pHash + dHash computation        │
         │  5. CLIP embedding computation       │
         │  6. EXIF extraction                  │
         │  7. Save to disk                     │
         │  8. Create DB record                 │
         │  9. Append Ledger Entry #1 (INGEST)  │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │    CELERY CHORD DISPATCHED           │
         │    (9 tasks fire simultaneously)     │
         └────────┬────────────────────────────┘
                  │
    ┌─────────────┼─────────────────────────────────────────┐
    │             │                                         │
    ▼             ▼             ▼          ▼         ▼      ▼
 C2PA         Watermark     CLIP+DCT   MobileNet  Video  Document
 Check        Probe         Image      ONNX       Temp.  Font
                            Forensic   Triage     +AV    Analysis
    │             │             │          │       Sync       │
    └─────────────┴─────────────┴──────────┴───────┴─────────┘
                                │
              + Localization (ELA+Noise Heatmap)
              + EXIF Metadata Check
              + Origin pHash+FAISS Search
                                │
                                ▼
         ┌─────────────────────────────────────┐
         │       EVIDENCE FUSION ENGINE         │
         │  1. Platt-calibrate all scores       │
         │  2. Convert to BeliefMass objects    │
         │  3. Dempster-Shafer combination      │
         │  4. Compute conflict metric K        │
         │  5. Derive 95% CI                    │
         │  6. Generate verdict + evidence list │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │      FRONTEND DASHBOARD UPDATES     │
         │  • Verdict card                     │
         │  • 7-signal radar chart             │
         │  • Heatmap overlay                  │
         │  • Origin graph                     │
         │  • Evidence bullet list             │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │     REPORT GENERATION (On demand)   │
         │  • BSA §63(4) Certificate PDF        │
         │  • Full Forensic Dossier PDF         │
         │  • NCRP-compatible JSON Export       │
         └─────────────────────────────────────┘
```

### 9.2 Image Analysis Sub-Flow

```
Image File
    │
    ├── JPEG Quality Estimation ──────────────────┐
    │   (from quantization table in JPEG header)  │
    │                                             │
    ├── Branch A: CLIP ViT-L/14                   │
    │   preprocess → encode_image → [768-d vec]  │
    │   → LightweightForensicHead → sigmoid → score│
    │   (Fallback: Laplacian variance heuristic)  │
    │                                             │ DCT weight
    ├── Branch B: DCT Analysis ◄──────────────────┘
    │   8×8 DCT blocks → AC energy + variance
    │   2D FFT → spectral noise ratio
    │   8px boundary ratio → block misalignment
    │   → raw_score (0.05 – 0.95)
    │
    └── Dynamic Fusion
        score_A * 1.0 + score_B * jpeg_weight
        ─────────────────────────────────────
                  1.0 + jpeg_weight
        = fused_ai_score
```

### 9.3 Dempster-Shafer Combination Flowchart

```
Module 1 Output → BeliefMass(m_real=0.85, m_fake=0.05, m_uncertain=0.10)
                         │
                         │ Dempster Combination
                         ▼
Module 2 Output → BeliefMass(m_real=0.05, m_fake=0.80, m_uncertain=0.15)
                         │
                         │ K = 0.85×0.80 + 0.05×0.05 = 0.68 + 0.0025 = 0.68
                         │ HIGH CONFLICT → uncertainty band widened
                         │ → Report: "Signals disagree; human review needed"
                         │
                         ▼
Module 3 Output → BeliefMass(m_real=0.20, m_fake=0.20, m_uncertain=0.60)
                         │ (No credentials → mostly uncertain)
                         │
                         ▼
            Combined Final: m_real | m_fake | m_uncertain
                         │
                         ▼
            fused_ai_prob = m_fake / (m_fake + m_real)
            ci_lower = fused_ai_prob - m_uncertain × 0.25
            ci_upper = fused_ai_prob + m_uncertain × 0.25
```

### 9.4 Chain-of-Custody Ledger

```
Entry #1 (INGEST):
  entry_hash = SHA256("0"×64 | "INGEST" | file_sha256 | T1 | details)
  prev_hash  = "0"×64

Entry #2 (ANALYSIS_START):
  entry_hash = SHA256(Entry#1.hash | "ANALYSIS_START" | file_sha256 | T2 | details)
  prev_hash  = Entry#1.hash

Entry #3 (ANALYSIS_COMPLETE):
  entry_hash = SHA256(Entry#2.hash | "ANALYSIS_COMPLETE" | file_sha256 | T3 | details)
  prev_hash  = Entry#2.hash

Entry #4 (REPORT_GENERATED):
  entry_hash = SHA256(Entry#3.hash | "REPORT_GENERATED" | file_sha256 | T4 | details)
  prev_hash  = Entry#3.hash

If any row is modified: all subsequent hashes become invalid → tamper detected
```

---

## 10. Backend API Endpoints

| Method | Endpoint | What It Does |
|---|---|---|
| `GET` | `/health` | Health check — returns service status |
| `GET` | `/api/v1/cases` | List all cases |
| `POST` | `/api/v1/cases` | Create a new case |
| `GET` | `/api/v1/cases/{id}` | Get case details |
| `GET` | `/api/v1/cases/{id}/ledger` | Get hash-chained audit trail |
| `POST` | `/api/v1/analysis/{case_id}/upload` | Upload media + trigger pipeline |
| `GET` | `/api/v1/analysis/{media_id}/results` | Get analysis results + fusion summary |
| `GET` | `/api/v1/analysis/{media_id}/heatmap/{filename}` | Serve heatmap image |
| `POST` | `/api/v1/reports/generate` | Generate BSA cert or forensic PDF |

---

## 11. Database Schema

```
cases
  id (UUID PK), case_number, ncrp_complaint_number, title, category,
  status, priority, officer_name, officer_badge, created_at

media_items
  id (UUID PK), case_id (FK), original_filename, stored_filename,
  media_type, mime_type, file_size_bytes,
  sha256_hash, phash, dhash,                    ← forensic fingerprints
  width, height, jpeg_quality_estimate,
  clip_embedding (VECTOR(768)),                  ← pgvector for FAISS-style search
  exif_data (JSONB), analysis_status, created_at

analysis_results
  id (UUID PK), media_item_id (FK), module_type,
  ai_generation_score, manipulation_score, confidence,
  c2pa_status, watermark_status,
  details (JSONB),                               ← full module output
  explanation (TEXT), heatmap_path,
  suspicious_regions (JSONB), created_at

ledger_entries
  id (UUID PK), case_id (FK), media_item_id (FK),
  sequence_number, action,
  media_sha256, entry_hash, prev_hash,           ← Merkle chain
  actor, details (JSONB), created_at

evidence_graph_nodes / edges
  For origin propagation graph storage
```

---

## 12. Key Differentiators — Summary

1. **Dempster-Shafer Fusion** — Surfaces signal conflicts explicitly rather than hiding them in a weighted average. Unique in the Indian hackathon context.

2. **Dynamic DCT Recompression Weighting** — Automatically reduces frequency analysis weight when JPEG quality is low. Directly addresses the Indian WhatsApp forwarding problem. No public benchmark models this.

3. **BSA §63(4) Auto-Generation** — India-specific, legally required document format. No commercial tool generates this.

4. **Dual-Architecture Ensemble** — CNN (MobileNetV2, pixel/texture artifacts) + Transformer (CLIP ViT, semantic inconsistencies) running as independent evidence channels.

5. **Document Forensics** — Font stroke-width distance-transform analysis for marksheet/ID card tampering. Directly addresses Aadhaar fraud and educational certificate manipulation.

6. **AV Sync Voice Clone Detection** — Targets "Digital Arrest" scam videos — India's largest and fastest-growing cyber fraud category.

7. **Honest Uncertainty** — The system explicitly models what it doesn't know. Confidence intervals widen when signals conflict. We never output a false 97% when the evidence is contradictory.

8. **Two-Stage Origin Retrieval** — pHash (fast, compression-resilient) pre-filter followed by CLIP embedding cosine similarity (semantics-resilient) for propagation graph construction.

9. **Merkle-Chain Ledger** — Every action on evidence is hash-chained, making the audit trail tamper-evident — the chain of custody itself becomes cryptographic proof.

10. **Face Quality Gate** — Explicitly refuses to report temporal analysis scores on degraded video rather than outputting a misleading confident verdict. Epistemic honesty.

---

## 13. Running the Project

### Option A: Docker (Recommended)
```bash
# Start all services (Postgres + Redis + Backend + Celery Worker + Frontend)
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend API + Swagger: http://localhost:8000/docs
```

### Option B: Local (Without Docker)
```powershell
# Terminal 1: Database
docker-compose up -d db redis

# Terminal 2: Backend
cd backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 3: Celery Worker
cd backend && venv\Scripts\activate
celery -A app.core.celery_app worker --loglevel=info -P solo

# Terminal 4: Frontend
cd frontend && npm install && npm run dev
```

### Environment Variables (`.env`)
```env
DATABASE_URL=postgresql+asyncpg://pratibimb:secret@localhost:5432/pratibimb_praman
DATABASE_URL_SYNC=postgresql://pratibimb:secret@localhost:5432/pratibimb_praman
REDIS_URL=redis://localhost:6379/0
CLIP_MODEL_NAME=ViT-L-14
DEVICE=cpu           # or cuda
FORENSIC_HEAD_CHECKPOINT=./models/lnclip_weights.pt
MOBILENET_ONNX_PATH=./models/mobilenet_v2_triage.onnx
```

---

## 14. Honest Limitations (Stated Proactively)

Stating limitations proactively builds credibility with a technical/legal judging panel.

1. **Trained model weights** — The architecture is complete; weights are trained offline on Colab T4 using GenImage + Indian recompression-augmented dataset. Heuristic fallbacks produce real, non-hardcoded outputs without weights.
2. **Cannot trace into encrypted channels** — WhatsApp/private Telegram groups are legally and technically inaccessible. Origin tracing is bounded to the indexable web.
3. **No detector achieves 0% error** — The platform's job is to make uncertainty visible and quantified, not to eliminate it.
4. **C2PA ecosystem adoption** — Will be absent for the vast majority of Indian media for the foreseeable future.
5. **Watermark removal arms race** — Watermark absence is deliberately treated as weak evidence.
6. **Indian face/accent performance** — Benchmark evaluation on Indian demographics is an open research question.

---

## 15. Research Foundation

| Paper | Relevance |
|---|---|
| **LNCLIP-DF** (arXiv:2508.06248) | LayerNorm-only fine-tuning for CLIP — the approach behind our forensic head |
| **Ojha et al., CVPR 2023** | Foundational frozen-CLIP as universal fake detector |
| **NTIRE 2026** (arXiv:2604.11487) | Robustness benchmark methodology (108,750 real + 185,750 AI images, 42 generators) |
| **DF40** (NeurIPS 2024) | 40-method deepfake detection benchmark |
| **Community Forensics** (arXiv:2411.04125) | Cross-generator generalization strategies |
| **AI-Generated Image Detection: Empirical Study** (arXiv:2511.02791) | Three documented failure modes this platform addresses |

---

*"प्रतिबिम्ब" (Reflection) — Does the image reflect reality, or is it a synthetic mirror?*
*"प्रमाण" (Proof) — Can it prove that in court?*
