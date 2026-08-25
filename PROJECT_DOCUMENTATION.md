# 🛡️ PratiBimb Praman (प्रतिबिंब प्रमाण)
### AI Media Forensic Provenance, Tampering Detection & Origin Intelligence Platform
*Engineered for Indian Law Enforcement — Chandigarh Police National Hackathon 2026*

---

## 📑 Table of Contents
1. [Problem Statement & Background](#1-problem-statement--background)
2. [Deep Breakdown of Problem Statement](#2-deep-breakdown-of-problem-statement)
3. [Core Technical Architecture & Logic](#3-core-technical-architecture--logic)
4. [Technology Stack & Library Justifications](#4-technology-stack--library-justifications)
5. [System Architecture Diagram (Backend & Fusion Pipeline)](#5-system-architecture-diagram-backend--fusion-pipeline)
6. [Detailed Working Flowchart (Step-by-Step)](#6-detailed-working-flowchart-step-by-step)
7. [Forensic Analysis Modules (Deep Dive)](#7-forensic-analysis-modules-deep-dive)
8. [Evidence Fusion Logic (Dempster-Shafer Theory)](#8-evidence-fusion-logic-dempster-shafer-theory)
9. [Indian Legal Admissibility (BSA 2023 §63 & Merkle Ledger)](#9-indian-legal-admissibility-bsa-2023-63--merkle-ledger)
10. [Frontend UI Wireframe & Design Hierarchy](#10-frontend-ui-wireframe--design-hierarchy)
11. [Expected Inputs, Outputs & Test Scenarios](#11-expected-inputs-outputs--test-scenarios)
12. [How to Run (Single Command Local & Production Docker)](#12-how-to-run-single-command-local--production-docker)

---

## 1. Problem Statement & Background

### Official Problem Statement:
> **"Platform to Identify AI-Generated/AI-Altered Videos & Images and Trace Their Origin Across Social Media"**
> 
> *Development of an AI-Powered Digital Forensic Platform to Detect AI-Generated or Manipulated Images and Videos, Verify Their Authenticity, and Trace Their Origin and Dissemination Across Social Media.*

### Real-World Police Context:
Generative AI tools (Midjourney, Stable Diffusion, Flux, Sora, voice cloning) have made creating hyper-realistic synthetic media effortless. Malicious actors exploit this capability for:
- **Financial Cyber Fraud:** Forged marksheets, fake Aadhaar/ID cards, altered bank statements, deepfake KYC impersonation.
- **Law & Order / Disinformation:** Fabricated videos of public figures/officials, communal fake news circulated rapidly through closed messaging networks like WhatsApp and Telegram.
- **Judicial Challenge:** In Indian courts, digital evidence must strictly comply with **Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63(4)** (formerly Indian Evidence Act Section 65B). Evidence lacking verifiable chain-of-custody or clear explainability is rejected.

---

## 2. Deep Breakdown of Problem Statement

To solve this challenge end-to-end for Indian law enforcement, the problem is divided into **four foundational pillars**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FOUR PILLARS OF PRATIBIMB PRAMAN                         │
├───────────────────────┬─────────────────────────┬───────────────────────────┤
│ 1. AI & Tampering     │ 2. Cryptographic        │ 3. Origin Tracing &       │
│    Detection          │    Integrity & Provenance│    Propagation Graph      │
│ • Fast CNN Triage     │ • C2PA Manifests        │ • Dual-stage Retrieval    │
│ • Frequency (DCT)     │ • Steganographic Marks  │ • pHash Hamming Filter    │
│ • Compression (ELA)   │ • EXIF/Metadata Checks  │ • CLIP Cosine Similarity  │
│ • Font Consistency    │ • Merkle Audit Ledger   │ • Time/Format Inferences  │
├───────────────────────┴─────────────────────────┴───────────────────────────┤
│ 4. Indian Judicial Compliance (BSA 2023 §63 / I4C NCRP Integration)         │
│ • Automated 63(4) Part A & Part B Court Certificate Generation (PDF)        │
│ • Calibrated Probability + Epistemic Uncertainty Estimation ($k$-conflict)  │
│ • NCRP JSON Export for National Cybercrime Portal Interoperability         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Technical Architecture & Logic

The system operates on an **asynchronous multi-signal evidence fusion pipeline**:
1. **Tier-0 Ultra-Fast Triage:** An optimized MobileNetV2 ONNX model analyzes images in **< 5 milliseconds** to give immediate classification before running deeper heuristics.
2. **Parallel Forensic Analyzers:** Specialized worker tasks execute concurrently in the background (spatial compression, frequency residuals, metadata structure, text stroke-width, C2PA signatures).
3. **Dempster-Shafer Fusion Engine:** Rather than taking a naive arithmetic average, the fusion engine combines belief masses from each independent module and mathematically accounts for **conflict and uncertainty**.
4. **Immutable Audit Ledger:** Every stage of ingestion, normalization, and analysis calculates a SHA-256 hash linked to the previous step (hash chaining), ensuring court admissibility.

---

## 4. Technology Stack & Library Justifications

| Layer / Component | Technology / Library | Version | Technical Justification & Purpose |
|---|---|---|---|
| **API Framework** | **FastAPI** | `0.115+` | High-performance asynchronous Python API with automatic OpenAPI Swagger documentation. |
| **ASGI Server** | **Uvicorn** | `0.34+` | Production-grade ASGI server handling asynchronous request concurrency. |
| **Neural Inference** | **ONNX Runtime** | `1.20+` | Ultra-fast, cross-platform neural network execution without heavy TensorFlow/CUDA overhead. |
| **Image Processing** | **Pillow (PIL)** | `11.1+` | Image normalization, RGB conversion, quantization table extraction, and resizing. |
| **Computer Vision** | **OpenCV (`cv2`)** | `4.10+` | Spatial manipulation, morphological dilation for text extraction, and Grad-CAM color mapping. |
| **Frequency Analysis** | **SciPy (`fftpack`)** | `1.15+` | 2D Discrete Cosine Transform (DCT) for spatial frequency residual computation. |
| **Perceptual Hash** | **ImageHash** | `4.3+` | Perceptual DCT Hashing (pHash) and Difference Hashing (dHash) for fast duplicate detection. |
| **Metadata Extraction**| **ExifRead** | `3.0+` | Deep parsing of EXIF data, embedded JPEG thumbnails, and compression offsets. |
| **Database ORM** | **SQLAlchemy** | `2.0+` | Modern Async ORM with universal type abstraction (works identically on SQLite & PostgreSQL). |
| **Local Database** | **SQLite + aiosqlite**| `0.22+` | Zero-configuration, zero-dependency embedded database for standalone local running. |
| **Task Queue Engine** | **Celery** | `5.4+` | Distributed task queue orchestrating parallel forensic worker pipelines. |
| **Task Broker (Local)**| **Fakeredis / Memory**| `2.37+` | In-memory queue emulation allowing full Celery chord workflows without installing Redis. |
| **Court PDF Generator**| **ReportLab** | `5.0+` | Programmatic PDF generation creating official BSA §63(4) dual-certified court evidence documents. |
| **Frontend UI** | **Next.js (React 18)** | `14.2+` | Modern server-side rendered dashboard with cyber-police aesthetic and Tailwind CSS. |
| **Data Visualization** | **Lucide Icons & Recharts** | `Latest` | Interactive charts, probability gauges, and evidence breakdown drawers. |

---

## 5. System Architecture Diagram (Backend & Fusion Pipeline)

```mermaid
graph TD
    User([Investigating Officer / Browser]) -->|Upload Image/Video| Frontend[Next.js Cyber Dashboard :3000]
    Frontend -->|POST /api/v1/cases/ & /analysis/| API[FastAPI Backend :8000]
    
    subgraph Ingestion & Integrity Layer
        API --> Ingest[Ingestion Service]
        Ingest --> SHA[Compute Cryptographic SHA-256]
        Ingest --> PHASH[Compute Perceptual pHash / dHash]
        Ingest --> LEDGER[Append-Only Merkle Hash Ledger]
    end

    subgraph Forensic Analyzer Ensemble (Parallel Execution)
        SHA --> M0[Tier-0: MobileNetV2 ONNX Triage <5ms]
        SHA --> M1[Tier-1: Frequency Domain 2D-DCT Analysis]
        SHA --> M2[Tier-1: Error Level Analysis ELA + GradCAM]
        SHA --> M3[Tier-1: EXIF & Thumbnail Mismatch Check]
        SHA --> M4[Tier-1: Document Font Stroke Consistency]
        SHA --> M5[Tier-2: C2PA Cryptographic Provenance]
        SHA --> M6[Tier-2: AI Watermark & Stego Detection]
        SHA --> M7[Tier-2: Origin Retrieval & Graph Builder]
    end

    subgraph Mathematical Evidence Fusion
        M0 & M1 & M2 & M3 & M4 & M5 & M6 & M7 --> FUSION[Dempster-Shafer Fusion Engine]
        FUSION --> CALC[Calibrated Probability Score]
        FUSION --> CONF[Epistemic Uncertainty k-Conflict]
        FUSION --> BULLETS[Explainability Bullet Points]
    end

    subgraph Legal Output Generation
        FUSION --> DB[(SQLite / PostgreSQL Database)]
        FUSION --> PDF[BSA 2023 §63(4) Court Certificate PDF]
        FUSION --> JSON_OUT[NCRP I4C JSON Package]
    end

    PDF --> Frontend
    DB --> Frontend
```

---

## 6. Detailed Working Flowchart (Step-by-Step)

```
[START: Officer Uploads Media]
       │
       ▼
[Step 1: Ingestion & Cryptographic Registration]
  ├── Store original file in /uploads/
  ├── Calculate SHA-256 hash (e.g., e3b0c442...)
  ├── Calculate perceptual pHash (e.g., b4a39c2e...)
  └── Create Genesis Ledger entry in database
       │
       ▼
[Step 2: Tier-0 Real-Time MobileNetV2 ONNX Triage]
  ├── Preprocess image (224x224, Normalized [0, 1])
  ├── Run ONNX Runtime inference
  └── If score > 0.98 -> Immediate High-Risk Flag
       │
       ▼
[Step 3: Multi-Signal Parallel Forensic Analysis]
  ├── [DCT Module]: 2D-DCT spectral density + 8x8 JPEG grid boundary discontinuity
  ├── [ELA Module]: Resave at 90% quality -> compute pixel delta -> calculate Std-Dev
  ├── [EXIF Module]: Scan for 'Photoshop', 'GIMP', 'Midjourney' + check thumbnail offset
  ├── [Font Module]: Extract text contours -> measure stroke-width variance
  ├── [C2PA Module]: Parse JUMBF boxes for signed cryptographic manifests
  └── [Origin Trace]: Query internal pHash index + public visual match graph
       │
       ▼
[Step 4: Evidence Fusion (Dempster-Shafer Combination)]
  ├── Assign belief mass m(AI), m(Real), m(Uncertain) per module
  ├── Calculate orthogonal sum: m1 ⊕ m2 ⊕ ... ⊕ mN
  ├── Compute conflict factor k: k = Σ m1(A) * m2(B) for A ∩ B = ∅
  └── Output: Final Verdict + Fused Probability (0.0 to 1.0) + Confidence Interval
       │
       ▼
[Step 5: Judicial Certification & Dashboard Rendering]
  ├── Render interactive scorecard on Next.js UI
  ├── Display Grad-CAM / ELA heatmap overlay
  ├── Generate BSA 2023 Section 63(4) PDF Certificate
  └── [END: Ready for Courtroom Presentation / NCRP Submission]
```

---

## 7. Forensic Analysis Modules (Deep Dive)

### 1. MobileNetV2 ONNX Fast Triage (`backend/app/modules/image_forensic/mobilenet_triage.py`)
- **Trained Architecture:** MobileNetV2 backbone fine-tuned on authentic vs. generative AI datasets.
- **Conversion:** Exported to standard ONNX format (`mobilenet_v2_triage.onnx`, 9.9 MB).
- **Execution:** Runs in **3.8 ms** per image on standard CPU.
- **Preprocessing:** `(image / 255.0)` normalized into `(1, 224, 224, 3)`.

### 2. Error Level Analysis & Localization (`backend/app/modules/localization/gradcam.py`)
- **Scientific Principle:** When an image is saved as JPEG, the entire canvas compresses at a uniform error level. If a foreign object or AI face is spliced into the image, that region exhibits a different compression error rate compared to the background.
- **Calculation:**
  $$\text{ELA}(x, y) = |\text{Image}_{\text{original}}(x, y) - \text{Image}_{\text{resaved@90\%}}(x, y)| \times \text{Scale}$$
- **Output:** Color-mapped heatmap overlay showing exact modified regions + standard deviation manipulation score.

### 3. DCT Frequency & Block Boundary Analysis (`backend/app/modules/image_forensic/dct_analysis.py`)
- **Scientific Principle:** Natural optical lenses produce smooth continuous frequency distributions. Generative GAN/Diffusion models leave periodic high-frequency grid artifacts. Spliced images disrupt the standard $8 \times 8$ JPEG block boundary grid.
- **Calculation:** Evaluates high-to-low frequency energy ratios and computes the **Block Boundary Discontinuity Ratio (BBDR)** across 8-pixel intervals.

### 4. EXIF & Metadata Integrity (`backend/app/modules/metadata/exif_check.py`)
- **Scientific Principle:** Inspects binary headers for forensic markers:
  - Software editing tags (`Adobe Photoshop`, `Canva`, `GIMP`, `Stable Diffusion`).
  - Discrepancies between main image dimensions and embedded JPEG thumbnail dimensions.
  - Timestamp ordering conflicts (Creation date > Modification date).

### 5. Document Forensics & Font Analysis (`backend/app/modules/document_forensic/font_analysis.py`)
- **Scientific Principle:** In forged marksheets, certificates, and government circulars, fraudsters modify individual roll numbers or marks using digital text boxes. These substituted characters have different stroke-width distributions and pixel variances compared to the original document's typography.
- **Calculation:** Uses Otsu thresholding + contour boundary tracking to measure stroke-width variance across text characters.

---

## 8. Evidence Fusion Logic (Dempster-Shafer Theory)

Instead of relying on a single AI model (which can hallucinate or produce false positives), PratiBimb Praman implements **Dempster's Rule of Combination**:

Given frame of discernment $\Theta = \{\text{Synthetic (S)}, \text{Authentic (A)}\}$, each module $i$ provides basic belief assignments:
- $m_i(S)$: Belief that the media is AI-generated / tampered.
- $m_i(A)$: Belief that the media is authentic.
- $m_i(\Theta)$: Epistemic uncertainty (uncommitted belief).

### Mathematical Combination:
$$(m_1 \oplus m_2)(A) = \frac{\sum_{X \cap Y = A} m_1(X) m_2(Y)}{1 - k}$$

Where $k$ is the measure of **epistemic conflict** between sensors:
$$k = \sum_{X \cap Y = \emptyset} m_1(X) m_2(Y)$$

If $k \to 1$, the system flags a **High Sensor Conflict Warning** on the UI, alerting the forensic investigator that one sensor contradicts another (e.g., EXIF was stripped by WhatsApp, but pixel structure is pristine).

---

## 9. Indian Legal Admissibility (BSA 2023 §63 & Merkle Ledger)

Under **Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63(4)**, electronic records submitted in Indian courts require a dual-certification model:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               BSA 2023 SECTION 63(4) DUAL CERTIFICATION MODEL               │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ PART A: Examiner / Investigator      │ PART B: System / Server Device       │
│ • Officer Name & Badge Number        │ • Machine Hostname & MAC Address     │
│ • Hash of uploaded evidence          │ • Operating System & Kernel Version  │
│ • Date, Time, Police Station jurisdiction│ • Tool Name & Version (PratiBimb v1.0)│
│ • Signature & Declaration of Custody │ • Cryptographic SHA-256 Ledger State │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### Cryptographic Chain-of-Custody (Merkle Hash Chain):
Every transaction in the database is hash-chained:
$$\text{EntryHash}_n = \text{SHA256}(\text{EntryHash}_{n-1} + \text{Action} + \text{MediaSHA256} + \text{Timestamp} + \text{Details})$$
Any retroactive database tampering breaks the hash chain and is immediately flagged during courtroom validation.

---

## 10. Frontend UI Wireframe & Design Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [🛡️ PRATIBIMB PRAMAN]  [BSA §63 READY]             [Dashboard] [Case Queue] │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🛡️ CHANDIGARH POLICE NATIONAL HACKATHON 2026                                │
│ AI Media Forensic Provenance & Origin Intelligence Platform                 │
├─────────────────┬──────────────────┬──────────────────┬─────────────────────┤
│ Total Cases: 3  │ Detected: 84.2%  │ BSA Certs: 2     │ Avg Speed: 1.8 min  │
├─────────────────┴──────────────────┴──────────────────┴─────────────────────┤
│ ┌──────────────────────────────┐  ┌───────────────────────────────────────┐ │
│ │ 📥 Forensic Evidence Intake  │  │ 📋 Active Case Docket                 │ │
│ │ Case Title: [_____________]  │  │ Case ID       Title          Status   │ │
│ │ Category:   [Deepfake   v]   │  │ CHD-2026-F89A Forged Mark... COMPLETED│ │
│ │ Officer:    [Insp. R. Sharma]│  │ CHD-2026-E42C Viral Deepf... COMPLETED│ │
│ │ Dropzone:   [ Upload Media ] │  │ CHD-2026-A11B Tampered ID... ANALYZING│ │
│ │ [ Begin Forensic Analysis ]  │  │                                       │ │
│ └──────────────────────────────┘  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CASE ANALYSIS VIEW: CHD-2026-F89A12                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ [📊 Verdict Scorecard] [🗺️ Visual Heatmap] [📜 C2PA] [🌐 Origin Graph]     │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 🎯 Fused AI Probability: 94.2%       │ 📄 Case Custody & Legal Actions      │
│ 📏 Confidence Interval: 89% – 97%    │ • NCRP Number: NCRP-2026-CHD-00941   │
│ ⚡ MobileNetV2 Triage: 96.5% (3.8ms)  │ • SHA-256: e3b0c44298fc1c149afb...   │
│                                      │                                      │
│ Key Findings:                        │ [ 📥 Download BSA §63(4) PDF Cert ]  │
│ • High-frequency DCT grid anomaly    │ [ 📦 Download NCRP I4C JSON Package ]│
│ • ELA localized residual mismatch    │                                      │
│ • Font stroke-width variance high    │ [ 🔍 Explainability Breakdown Drawer]│
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 11. Expected Inputs, Outputs & Test Scenarios

### Scenario A: Authentic Police Bodycam / Official Photograph
* **Input:** Unedited JPEG/PNG photo from a genuine camera.
* **Output:**
  - **Verdict:** `AUTHENTIC / ORIGINAL`
  - **Fused AI Probability:** `4.8% [2% – 8%]`
  - **C2PA / Watermark:** Clean baseline; consistent quantization table.
  - **Court Action:** Certificate confirms genuine provenance with device hash.

### Scenario B: AI Deepfake / Spliced Marksheet
* **Input:** Midjourney-generated image or image with altered roll number/text.
* **Output:**
  - **Verdict:** `TAMPERED / AI-GENERATED`
  - **Fused AI Probability:** `96.5% [92% – 99%]`
  - **Grad-CAM / ELA:** Red glowing heatmap overlay on altered facial or text zones.
  - **Evidence Bullets:** Explicitly flags DCT grid anomaly, ELA std-dev elevation, and font stroke variance.
  - **Court Action:** Downloadable BSA §63(4) PDF complete with examiner declarations and hash ledger verification.

---

## 12. How to Run (Single Command Local & Production Docker)

### Option 1: Standalone Single-Command Run (Zero Docker Needed)
Runs on Windows, Linux, or macOS using local SQLite and in-process background workers:

```powershell
# From project directory:
python run.py
```
*Auto-detects environment, initializes database schemas, launches FastAPI backend on `:8000`, launches Next.js UI on `:3000`, and opens your default browser.*

### Option 2: Production Containerized Run (Docker Compose)
For enterprise deployment on police server infrastructure:

```bash
docker-compose up --build
```
*Spawns PostgreSQL with `pgvector`, Redis message broker, Celery worker nodes, FastAPI, and Next.js.*

---

### 🏛️ Developed for Chandigarh Police National Hackathon 2026
*Project Lead & Development Team — Digital Forensics & Cyber Intelligence Division*
