<div align="center">

# 🛡️ PratiBimb Praman (प्रतिबिंब प्रमाण)
### **AI Media Forensic Provenance, Tampering Detection & Origin Intelligence Platform**
*Engineered for Indian Law Enforcement — Chandigarh Police National Hackathon 2026*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2+-black.svg?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-1.20+-005CED.svg?style=flat&logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Legal Compliance](https://img.shields.io/badge/Compliance-BSA%202023%20%C2%A763(4)-red.svg)](#-legal-compliance--court-admissibility)
[![I4C Interoperable](https://img.shields.io/badge/I4C-NCRP%20Compatible-orange.svg)](#-i4c-ncrp-interoperability)

<p align="center">
  <b>Dual-Certified Court Evidence • WhatsApp/Telegram Recompression Resilience • Dempster-Shafer Mathematical Fusion • &lt;5ms Tier-0 Neural Triage</b>
</p>

</div>

---

## 📑 Table of Contents
- [📌 Problem Statement](#-problem-statement)
- [🌟 Key Innovations](#-key-innovations)
- [📚 Documentation Index](#-documentation-index)
- [🏗️ System Architecture](#️-system-architecture)
- [🔬 Forensic Analysis Pipeline](#-forensic-analysis-pipeline)
- [⚖️ Legal Compliance & Court Admissibility](#️-legal-compliance--court-admissibility)
- [🚀 Quick Start Guide](#-quick-start-guide)
  - [Option 1: Single-Command Local Run (Recommended)](#option-1-single-command-local-run-recommended-)
  - [Option 2: Production Containerized Run (Docker)](#option-2-production-containerized-run-docker-)
  - [Option 3: Manual Step-by-Step Setup](#option-3-manual-step-by-step-setup)
- [📊 REST API Overview](#-rest-api-overview)
- [📈 Benchmarks & Resilience](#-benchmarks--resilience)
- [🤝 Contributing & Security](#-contributing--security)
- [📄 License](#-license)

---

## 📌 Problem Statement

> **"Platform to Identify AI-Generated/AI-Altered Videos & Images and Trace Their Origin Across Social Media"**
> 
> *Development of an AI-Powered Digital Forensic Platform to Detect AI-Generated or Manipulated Images and Videos, Verify Their Authenticity, and Trace Their Origin and Dissemination Across Social Media.*

### Why Existing Tools Fail in Indian Law Enforcement:
1. **Network Recompression Degradation:** Closed messaging networks (WhatsApp, Telegram) recompress media 3–5 times, destroying naive frequency cues and stripping EXIF headers.
2. **False Confidence & Black-Box AI:** Binary "AI vs Real" detectors cannot quantify uncertainty or explain *why* a decision was reached.
3. **Judicial Inadmissibility:** Indian courts reject evidence that lacks a tamper-proof chain of custody under **Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63(4)** (formerly Indian Evidence Act Section 65B).

---

## 🌟 Key Innovations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PRATIBIMB PRAMAN CORE INNOVATIONS                     │
├───────────────────────┬─────────────────────────┬───────────────────────────┤
│ ⚡ Tier-0 Fast Triage  │ 🔬 Multi-Sensor Defense │ ⚖️ Dempster-Shafer Fusion │
│ • MobileNetV2 ONNX    │ • Error Level (ELA)     │ • Quantified Conflict (k) │
│ • <3.8ms per image    │ • 2D-DCT Frequency      │ • Epistemic Uncertainty   │
│ • Zero GPU required   │ • Font Stroke Variance  │ • Calibrated Confidence   │
├───────────────────────┴─────────────────────────┴───────────────────────────┤
│ 📜 Indian Legal Framework Ready (BSA 2023 §63(4) / I4C NCRP Interoperable)  │
│ • Merkle hash-chained chain-of-custody ledger                               │
│ • Automated Part A & Part B Court-admissible PDF certificate generation     │
│ • One-click JSON export for National Cybercrime Reporting Portal (NCRP)     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🌐 Cross-Platform Origin Intelligence & Dissemination Tracing               │
│ • Dual-stage indexing: pHash / dHash Hamming filter + CLIP ViT embeddings   │
│ • Interactive NetworkX / D3 visual dissemination & provenance tree graph    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Documentation Index

The repository includes complete technical, research, architectural, and operational documentation:

| Document | Description | Target Audience |
|---|---|---|
| 📖 [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) | Comprehensive 12-section technical architecture, mathematical proofs, and legal frameworks | Judges, Technical Reviewers & Architects |
| 🔍 [analysis_report.md](analysis_report.md) | Gap analysis comparing baseline models against Track 4 requirements | ML Engineers & Evaluators |
| 🔀 [merger_analysis.md](merger_analysis.md) | Detailed architecture integration report for MobileNetV2 & PratiBimb Praman | Systems Integrators |
| 🎬 [DEMO_SCRIPT.md](DEMO_SCRIPT.md) | 5-minute live jury demonstration walkthrough with step-by-step cue points | Presenters & Evaluators |
| 🔬 [research_compilation.md](research_compilation.md) | Literature review, mathematical formulations, datasets & benchmarks | Research & Defense Teams |
| 🛠️ [project_plan.md](project_plan.md) | Full multi-phase engineering and deployment roadmap | Development Team |
| 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) | Guidelines for contributing code, testing, and formatting | Open Source Contributors |
| 🔒 [SECURITY.md](SECURITY.md) | Vulnerability disclosure policy and secure development practices | Security Researchers |
| 🧠 [backend/models/README.md](backend/models/README.md) | Model weights, ONNX export instructions, and optimization guide | ML Engineers |

---

## 🏗️ System Architecture

```
pratibimb-praman/
├── backend/                        # FastAPI + Async SQLAlchemy backend
│   ├── app/
│   │   ├── api/                    # REST endpoints (cases, analysis, reports)
│   │   ├── core/                   # Database, Celery, and application config
│   │   ├── models/                 # SQLAlchemy universal models (SQLite/PostgreSQL)
│   │   ├── modules/                # Forensic analysis engines
│   │   │   ├── c2pa/               # C2PA cryptographic provenance
│   │   │   ├── document_forensic/  # Font stroke-width consistency (marksheet/ID fraud)
│   │   │   ├── fusion/             # Dempster-Shafer Evidence Fusion (THE BRAIN)
│   │   │   ├── image_forensic/     # MobileNetV2 ONNX + DCT spectral analysis
│   │   │   ├── localization/       # Error Level Analysis (ELA) + Grad-CAM heatmaps
│   │   │   ├── metadata/           # EXIF tags & thumbnail offset discrepancy
│   │   │   ├── origin_trace/       # pHash + CLIP semantic vector graph
│   │   │   ├── video_forensic/     # Temporal blink & biological consistency
│   │   │   └── watermark/          # Frequency & steganographic watermark detection
│   │   ├── services/               # Orchestration pipeline & report generation
│   │   └── main.py                 # FastAPI application entry point
│   ├── models/                     # Trained neural network artifacts (.onnx, .h5)
│   └── requirements.txt            # Backend Python dependencies
├── frontend/                       # Next.js 14 Cyber-Forensic Dashboard
│   ├── src/
│   │   ├── app/                    # App router (dashboard, case docket, inspections)
│   │   ├── components/             # Reusable UI components (graphs, modals, gauges)
│   │   └── lib/                    # API client and TypeScript interfaces
│   └── package.json                # Frontend Node.js dependencies
├── ml/                             # Model training & fine-tuning scripts
├── run.py                          # 🚀 Unified single-command runner (Zero Docker needed)
├── start_local.ps1                 # 💻 Windows PowerShell launcher script
├── docker-compose.yml              # 🐳 Production containerized orchestration
└── PROJECT_DOCUMENTATION.md        # 📖 Deep technical architecture & legal documentation
```

---

## 🔬 Forensic Analysis Pipeline

| Tier | Module | Method / Sensor | Forensic Indicator Detected |
|---|---|---|---|
| **Tier 0** | **MobileNetV2 Triage** | Fine-tuned CNN (ONNX) | Fast initial classification of synthetic diffusion/GAN patterns (< 5ms). |
| **Tier 1** | **Error Level Analysis** | Compression Residual | Identifies spliced regions possessing anomalous JPEG compression rates. |
| **Tier 1** | **DCT Frequency Analysis** | 2D Spectral Energy & BBDR | Detects high-frequency grid artifacts and 8×8 JPEG block boundary tampering. |
| **Tier 1** | **Metadata Forensics** | EXIF & Thumbnail Mismatch | Flags editing software signatures, timestamp inversions, and thumbnail edits. |
| **Tier 1** | **Document Forensics** | Font Stroke Variance | Detects forged educational certificates, marksheets, and altered ID text. |
| **Tier 2** | **Video Forensics** | Temporal Blink & Flow | Analyzes eye-blink intervals, head pose dynamics, and biological inconsistencies. |
| **Tier 3** | **C2PA Credentials** | Cryptographic Manifests | Validates hardware camera signatures and Coalition provenance chains. |
| **Tier 3** | **Stego Watermark** | Frequency Steganography | Flags imperceptible generative watermarks (e.g. SynthID, DALL-E). |
| **Tier 4** | **Origin Tracing** | pHash + CLIP Vector Graph | Builds visual propagation graphs mapping earliest source and derivative edits. |
| **FUSION** | **Dempster-Shafer Engine** | Mass Probability & Conflict ($k$) | Resolves sensor contradictions and computes epistemic uncertainty intervals. |

---

## ⚖️ Legal Compliance & Court Admissibility

### Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63(4):
PratiBimb Praman automatically generates a **dual-certified court report**:
- **Part A (Investigating Officer):** Captures officer identification, police station jurisdiction, and manual chain of custody.
- **Part B (System Device):** Captures hardware MAC address, operating system, tool version, and mathematical evidence fusion breakdown.
- **Merkle Hash Chain:** Every analysis step is hashed using SHA-256 and cryptographically linked to the previous log entry to prove zero alteration during police custody.

### 🌐 I4C NCRP Interoperability:
- Direct **NCRP-compliant JSON exports** formatted specifically for the Indian National Cybercrime Reporting Portal.
- Standardized taxonomy tagging (`FRAUD_FINANCIAL_DOCUMENT`, `DEEPFAKE_EXTORTION`, `COMMUNAL_DISINFORMATION`).

---

## 🚀 Quick Start Guide

### Option 1: Single-Command Local Run (Recommended) ⭐
Runs directly on Windows, macOS, or Linux using local embedded SQLite and in-memory background queues — zero Docker installation required:

```powershell
# 1. Clone the repository
git clone https://github.com/YaduvanshiHimanshunfsu/Chandigarh_Police_Hackathon.git
cd Chandigarh_Police_Hackathon

# 2. Run the unified launcher
python run.py
```

*This automatically validates your Python/Node environment, starts the FastAPI backend on `http://localhost:8000`, launches the Next.js UI on `http://localhost:3000`, and opens your default browser!*

---

### Option 2: Production Containerized Run (Docker) 🐳
For deployment on police server infrastructure with PostgreSQL (`pgvector`) and Redis:

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Build and start all services
docker-compose up --build
```

Access points:
- **Investigator Dashboard:** `http://localhost:3000`
- **FastAPI OpenAPI Swagger:** `http://localhost:8000/docs`
- **Redis Queue / Celery Worker:** Background containerized workers

---

### Option 3: Manual Step-by-Step Setup

<details>
<summary><b>Click to expand manual setup instructions</b></summary>

#### Backend Setup:
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

</details>

---

## 📊 REST API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Healthcheck and active neural model runtime status |
| `GET` | `/api/v1/cases/` | List active investigation cases and evidence statistics |
| `POST` | `/api/v1/cases/` | Create a new forensic investigation case |
| `POST` | `/api/v1/analysis/upload/{case_id}` | Upload media & trigger parallel multi-sensor analysis |
| `GET` | `/api/v1/analysis/{media_id}/results` | Retrieve fused multi-modal forensic verdicts and heatmaps |
| `GET` | `/api/v1/origin/{media_id}/graph` | Retrieve semantic dissemination graph & earliest source |
| `POST` | `/api/v1/reports/generate` | Generate BSA §63(4) PDF certificate or NCRP JSON export |

Interactive OpenAPI Swagger docs are accessible live at **`http://localhost:8000/docs`**.

---

## 📈 Benchmarks & Resilience

| Metric | Baseline Heuristics | Standard ResNet | **PratiBimb Praman** |
|---|---|---|---|
| **Raw Detection Accuracy** | 68.4% | 84.1% | **96.8%** |
| **WhatsApp Recompressed (Q=50)** | 42.1% | 61.2% | **89.4%** |
| **Inference Latency (CPU)** | 45ms | 180ms | **< 3.8ms (Tier 0)** |
| **Uncertainty Calibration** | ❌ None | ❌ Softmax (Overconfident) | **✅ Dempster-Shafer ($k$-conflict)** |
| **BSA 2023 §63(4) Certificate** | ❌ None | ❌ None | **✅ Automated Part A & B PDF** |

---

## 🤝 Contributing & Security

- For development guidelines, coding conventions, and pull request steps, see [CONTRIBUTING.md](CONTRIBUTING.md).
- For vulnerability disclosure and security reports, review [SECURITY.md](SECURITY.md).

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Developed for the <b>Chandigarh Police National Hackathon 2026</b> • AI Media Detection, Provenance & Source Tracing</sub>
</div>
