<div align="center">

# 🛡️ PratiBimb Praman (प्रतिबिंब प्रमाण)
### **AI Media Forensic Provenance, Tampering Detection & Origin Intelligence Platform**
*Engineered for Indian Law Enforcement — Chandigarh Police National Hackathon 2026*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2+-black.svg?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-1.20+-005CED.svg?style=flat&logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Legal Compliance](https://img.shields.io/badge/Compliance-BSA%202023%20%C2%A763(4)-red.svg)](#-legal-compliance--court-admissibility)

<p align="center">
  <b>Dual-Certified Court Evidence • WhatsApp/Telegram Recompression Resilience • Dempster-Shafer Mathematical Fusion • <5ms Tier-0 Neural Triage</b>
</p>

</div>

---

## 📌 Problem Statement

> **"Platform to Identify AI-Generated/AI-Altered Videos & Images and Trace Their Origin Across Social Media"**
> 
> *Development of an AI-Powered Digital Forensic Platform to Detect AI-Generated or Manipulated Images and Videos, Verify Their Authenticity, and Trace Their Origin and Dissemination Across Social Media.*

### Why Existing Tools Fail in Indian Law Enforcement:
1. **Network Degradation:** Closed messaging networks (WhatsApp, Telegram) recompress media 3–5 times, destroying naive frequency cues and stripping EXIF headers.
2. **False Confidence:** Binary "AI vs Real" detectors cannot quantify uncertainty or explain *why* a decision was reached.
3. **Judicial Inadmissibility:** Indian courts reject evidence that lacks a tamper-proof chain of custody under **Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63(4)** (formerly Indian Evidence Act Section 65B).

---

## 🌟 Key Innovations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PRATIBIMB PRAMAN CORE INNOVATIONS                     │
├───────────────────────┬─────────────────────────┬───────────────────────────┤
│ ⚡ Tier-0 Fast Triage  │ 🔬 Multi-Sensor Defense │ ⚖️ Dempster-Shafer Fusion │
│ • MobileNetV2 ONNX    │ • Error Level (ELA)     │ • Quantified Conflict (k) │
│ • 3.8ms per image     │ • 2D-DCT Frequency      │ • Epistemic Uncertainty   │
│ • Zero GPU required   │ • Font Stroke Variance  │ • Calibrated Confidence   │
├───────────────────────┴─────────────────────────┴───────────────────────────┤
│ 📜 Indian Legal Framework Ready (BSA 2023 §63(4) / I4C NCRP Interoperable)  │
│ • Merkle hash-chained chain-of-custody ledger                               │
│ • Automated Part A & Part B Court-admissible PDF certificate generation     │
│ • One-click JSON export for National Cybercrime Reporting Portal (NCRP)     │
└─────────────────────────────────────────────────────────────────────────────┘
```

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
├── docker-compose.yml              # 🐳 Production containerized orchestration
└── PROJECT_DOCUMENTATION.md        # 📖 Deep technical architecture & legal documentation
```

---

## 🚀 Quick Start Guide

### Option 1: Single-Command Local Run (Zero Docker Needed) ⭐
Runs directly on Windows, macOS, or Linux using local embedded SQLite and in-memory background queues:

```powershell
# 1. Clone the repository
git clone https://github.com/your-org/pratibimb-praman.git
cd pratibimb-praman

# 2. Run the all-in-one launcher
python run.py
```

*This automatically configures the database, launches the FastAPI backend on `http://localhost:8000`, starts the Next.js UI on `http://localhost:3000`, and opens your default browser!*

---

### Option 2: Production Containerized Run (Docker Compose) 🐳
For deployment on police server infrastructure with PostgreSQL (`pgvector`) and Redis:

```bash
cp .env.example .env
docker-compose up --build
```

---

## 🔬 Forensic Modules Breakdown

| Module | Method / Sensor | Forensic Indicator Detected |
|---|---|---|
| **MobileNetV2 Triage** | Fine-tuned CNN (ONNX) | Fast initial classification of synthetic diffusion/GAN patterns (< 5ms). |
| **Error Level Analysis** | Compression Residual | Identifies spliced regions possessing anomalous JPEG compression rates. |
| **DCT Frequency Analysis** | 2D Spectral Energy & BBDR | Detects high-frequency grid artifacts and 8×8 JPEG block boundary tampering. |
| **Metadata Forensics** | EXIF & Thumbnail Mismatch | Flags editing software signatures, timestamp inversions, and thumbnail edits. |
| **Document Forensics** | Font Stroke Analysis | Detects forged educational certificates, marksheets, and altered ID text. |
| **C2PA Credentials** | Cryptographic Manifests | Validates hardware camera signatures and Coalition provenance chains. |
| **Stego Watermark** | Frequency Steganography | Flags imperceptible generative watermarks (e.g. SynthID, DALL-E). |
| **Origin Tracing** | pHash + CLIP Vector Graph | Builds visual propagation graphs mapping earliest source and derivative edits. |

---

## ⚖️ Legal Compliance & Court Admissibility

### Bharatiya Sakshya Adhiniyam (BSA) 2023 Section 63(4):
PratiBimb Praman automatically generates a **dual-certified court report**:
- **Part A (Investigating Officer):** Captures officer identification, police station jurisdiction, and manual chain of custody.
- **Part B (System Device):** Captures hardware MAC address, operating system, tool version, and mathematical evidence fusion breakdown.
- **Merkle Hash Chain:** Every analysis step is hashed using SHA-256 and cryptographically linked to the previous log entry to prove zero alteration during police custody.

---

## 📊 REST API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Healthcheck and active model status |
| `GET` | `/api/v1/cases/` | List active investigation cases |
| `POST` | `/api/v1/cases/` | Create a new forensic investigation case |
| `POST` | `/api/v1/analysis/upload/{case_id}` | Upload media & trigger forensic analysis pipeline |
| `GET` | `/api/v1/analysis/{media_id}/results` | Retrieve fused multi-modal forensic results |
| `POST` | `/api/v1/reports/generate` | Generate BSA §63(4) PDF certificate or NCRP JSON |

Interactive OpenAPI Swagger docs available at **`http://localhost:8000/docs`**.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code style, testing protocols, and pull request workflows.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Developed for Chandigarh Police National Hackathon 2026 • AI Media Detection & Source Tracing</sub>
</div>
