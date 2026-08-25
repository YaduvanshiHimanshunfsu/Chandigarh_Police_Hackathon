# Demo Walkthrough Script
# Chandigarh Police Hackathon — PratiBimb Praman v1.0
# Judge Presentation Guide

---

## Pre-Demo Checklist (T-15 minutes)
- [ ] `docker-compose up -d` — all services running (backend :8000, frontend :3000, postgres, redis)
- [ ] `python scripts/seed_demo_data.py` — 3 demo cases loaded
- [ ] Browser open at `http://localhost:3000` on full-screen
- [ ] PDF viewer ready (BSA cert download)
- [ ] Terminal ready for quick `docker logs` if needed
- [ ] Test image ready: `demo_assets/deepfake_sample.jpg`

---

## Talking Points: What Makes Us Different

> **"Every individual forensic signal is beatable — what nobody has shipped is a fusion layer that knows exactly how much to trust each signal under Indian real-world degradation, stays honest about uncertainty, and outputs something a magistrate can accept under BSA Section 63."**

Key differentiators to hit during demo:
1. **MobileNetV2 Tier-0 triage** — 5ms CNN screen before expensive models
2. **Dempster-Shafer fusion** — explicitly handles conflicting signals (no blind averaging)
3. **WhatsApp recompression awareness** — JPEG quality downweights DCT branch automatically
4. **BSA §63(4) auto-cert** — dual-signature PDF in one click (Part A + Part B)
5. **NCRP JSON export** — structured handoff to I4C / cybercrime.gov.in
6. **Origin propagation graph** — shows WHERE the deepfake first appeared

---

## Segment 1: Dashboard Overview (0:00 – 0:45)

**Show:** `http://localhost:3000`

**Say:**
> "This is PratiBimb Praman — Hindi for 'Authentic Reflection'. It's the Chandigarh Police's AI-native evidence intake platform. Notice the four metrics at the top: total cases triaged, deepfake detection rate, BSA certificates issued, and average takedown speed — 1.8 minutes against the IT Rules 3-hour clock."

**Point out:**
- Case docket shows NCRP complaint numbers linking to cybercrime.gov.in
- Categories: Deepfake, Impersonation, Digital Arrest Scam, Misinformation

---

## Segment 2: Live Upload & MobileNetV2 Triage (0:45 – 1:45)

**Action:** Drag `demo_assets/deepfake_sample.jpg` into the Forensic Evidence Intake form.

**Fill in:**
- Case Title: "Live Demo — UT Official Deepfake"
- Category: Deepfake / AI Synthetic
- Officer: Inspector R. Sharma
- Click: **Begin Forensic Analysis & Custody Log**

**Say:**
> "The moment this file is uploaded, three things happen simultaneously: SHA-256 hash is computed for BSA §63(4) chain of custody, the MobileNetV2 Tier-0 triage fires in 5 milliseconds to give us an immediate CNN-based indicator, and all 7 forensic modules launch in parallel via Celery."

**Point out:**
> "Notice we now show MobileNetV2 triage result immediately — before the full CLIP analysis completes. This is the dual-architecture advantage: CNN catches local pixel artifacts, CLIP ViT-L/14 catches global semantic inconsistencies."

---

## Segment 3: Full Analysis Results (1:45 – 3:30)

**Navigate to:** Pre-seeded Case 1 "Viral Deepfake of UT Administrator"

**On the Fusion tab:**

**Say:**
> "91.4% AI generation probability — but more importantly, look at the 95% confidence interval: 84 to 95 percent. The system is being *honest* about what it doesn't know. The Dempster-Shafer conflict K is 0.21 — all signals are concordant. When signals conflict, we widen this interval rather than hiding the uncertainty."

**Walk through evidence bullets:**
- ✓ Green = confirmed evidence (CLIP, MobileNetV2, watermark)
- • Grey = neutral (C2PA absent — explain this is CORRECT for WhatsApp forwards)
- ⚠ Amber = conflict (if shown)

**Say:**
> "The MobileNetV2 violet card here — 87% tampered in 4.2 milliseconds. This is the same model from the hackathon's provided zip file, converted to ONNX so it runs without TensorFlow — no memory bloat in production."

---

## Segment 4: Heatmap Localization (3:30 – 4:00)

**Click:** Visual & Grad-CAM Heatmap tab

**Say:**
> "This is the ELA + SRM noise residual fusion heatmap — red zones show where compression anomalies are highest. The face boundary and neck contour, 14.8% of surface area. In a court, this is the spatial evidence — *where* was the image manipulated."

---

## Segment 5: BSA §63(4) Certificate (4:00 – 5:00)

**Click:** "BSA §63(4) Certificate" button — wait for PDF download.

**Open PDF and show:**

**Say:**
> "This is a legally prescribed dual-certification certificate. Part A is signed by the Investigating Officer — certifying the computer system was operating properly. Part B is the technical expert certificate — that's our system, PratiBimb Praman, certifying the cryptographic hash at ingestion matches the bitstream now."
>
> "Under BSA Section 63(4) — the successor to Section 65B of the Indian Evidence Act — this certificate is what makes electronic evidence admissible in court without requiring the original device. No other deepfake detection tool in India generates this automatically."

**Point to the SHA-256 in the certificate:**
> "This hash is tamper-evident. Any modification to the evidence file after ingestion will invalidate it."

---

## Segment 6: NCRP JSON Export (5:00 – 5:30)

**Click:** "NCRP JSON Export" button.

**Say:**
> "This structured JSON matches the I4C / National Cybercrime Reporting Portal schema. The investigating officer can upload this directly to cybercrime.gov.in — no manual data entry. The chain of custody, SHA-256, verdict, confidence interval, and origin data all travel together."

---

## Segment 7: Origin Propagation (5:30 – 6:00)

**Click:** Origin Propagation Graph tab

**Say:**
> "This graph shows the deepfake's propagation history — earliest indexed source, Telegram, August 15, then 17 re-shares across WhatsApp and X. For takedown requests under IT Rules 2021, this is the evidence of the original uploader."

---

## Segment 8: Case 3 — Authentic Contrast (6:00 – 7:00)

**Navigate to:** Case 3 "Authentic Press Conference — VERIFIED"

**Say:**
> "Now let me show the *other* direction. Same pipeline, genuine image with a valid C2PA signature from the Chandigarh Police Media Cell. Result: 8.2% AI probability. The system correctly identifies this as authentic. The Dempster-Shafer K is 0.05 — all signals in concordance."
>
> "This is critical for police use — avoiding false positives is just as important as catching deepfakes."

---

## Closing Statement (7:00 – 7:30)

> "Most deepfake detection tools give you a single number and no legal pathway. PratiBimb Praman gives you: an uncertainty-aware ensemble verdict, spatial localization of *where* the manipulation is, an origin propagation graph, a BSA §63(4) court-admissible certificate, and a machine-readable NCRP export — all in under 2 minutes."
>
> "We're not just detecting deepfakes. We're building the Indian Police's evidentiary chain from intake to courtroom."

---

## Q&A Responses

**Q: What if the model gets an image it's never seen before?**
> "Dempster-Shafer explicitly handles this — when signals conflict or are weak, the uncertainty mass increases. The confidence interval widens. The system says 'INCONCLUSIVE' instead of guessing. That epistemic honesty is the design goal."

**Q: Why ONNX for MobileNetV2?**
> "TensorFlow in the same process as PyTorch causes memory conflicts. ONNX Runtime is framework-agnostic — the model loads in 50ms, infers in 5ms, and adds zero TF/CUDA dependency overhead."

**Q: How does this handle WhatsApp recompression?**
> "We estimate JPEG quality at ingestion. Below Q=50, we automatically reduce the weight of the DCT frequency branch in the fusion engine — because repeated recompression destroys high-frequency artifacts. The system is tuned for Indian social media distribution chains, not clean lab images."

**Q: Is this BSA §63(4) compliant out of the box?**
> "The certificate structure follows the Schedule to BSA 2023. It requires an officer signature for Part A — which the system prompts for at case creation. Part B is auto-generated by the forensic engine. Both are required under Section 63(4) for electronic record admissibility."
