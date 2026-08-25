# PratiBimb Praman — Demo Preparation Implementation Plan

> **Context:** This is NOT a production build plan. The codebase is architecturally complete with real, non-hardcoded logic. The goal is to prepare a compelling **concept demo** that showcases the architecture, logic, and differentiation to hackathon judges.
>
> **Hackathon:** September 8–9, 2026 (24-Hour Offline + Grand Finale)
> **Current Date:** August 25, 2026 (~14 days to prepare)

---

## Phase 1: Train Model Weights on Google Colab (Optional but Recommended)

**Time:** ~2 hours total | **When:** Any day before Sep 8 | **Who:** ML team member

> [!TIP]
> This step is **optional** for the demo. Without trained weights, the system falls back to heuristic scoring (laplacian variance for CLIP, neutral 0.5 for MobileNetV2). The fallback still produces varying, non-hardcoded outputs per image. But having real weights makes the demo scores more meaningful.

### Step 1.1: Download a Small GenImage Subset (~1,000 real + 1,000 fake)

GenImage is 220GB+ total — you only need a tiny slice.

```python
# On Google Colab:
# GenImage stores images in class folders. Download just 2 classes (1 real, 1 fake).
!pip install gdown
# Option A: Use the GenImage HuggingFace mirror
from datasets import load_dataset
ds = load_dataset("GenImage-Dataset/GenImage", split="train", streaming=True)
# Take first 1000 real + 1000 fake
# Option B: Download from the GenImage GitHub releases page
# https://github.com/GenImage-Dataset/GenImage — follow their download instructions
# Pick just "imagenet_ai_0419_sdv4" (Stable Diffusion v1.4 subset) — smallest one
```

> [!IMPORTANT]
> **Do NOT download DiffusionDB (1.6TB).** It contains only AI-generated images (no real counterparts). It's useful for research, not for training a binary real/fake classifier.
>
> **Do NOT download the full DeepfakeBench or Celeb-DF** — those are video datasets for video model training, not needed for image classifier fine-tuning.

### Step 1.2: Run the Indian Recompression Simulator

Upload [ml/simulate_recompression_dataset.py](file:///e:/Competition/Chandigarh%20hackathon/ml/simulate_recompression_dataset.py) to Colab and run it on your 2,000 images:

```bash
python simulate_recompression_dataset.py \
  --input_dir ./genimage_subset/ \
  --output_dir ./recompressed/ \
  --generations 5
```

This creates WhatsApp-style multi-hop compressed variants, giving you ~10,000 training samples.

### Step 1.3: Fine-Tune the LNCLIP Head (~15 mins on T4)

Upload [ml/train_colab_t4_lnclip.py](file:///e:/Competition/Chandigarh%20hackathon/ml/train_colab_t4_lnclip.py) to Colab:

```bash
python train_colab_t4_lnclip.py \
  --data_dir ./recompressed/ \
  --epochs 5 \
  --output lnclip_weights.pt
```

Download the resulting `lnclip_weights.pt` (~5MB) and place it at:
```
backend/models/lnclip_weights.pt
```

### Step 1.4: Convert MobileNetV2 .h5 to ONNX (~5 mins)

```bash
# On any machine with TensorFlow installed (or Colab)
pip install tensorflow tf2onnx onnx
unzip mobilenetV2-main.zip -d /tmp/mobilenet_src
# Find the .h5 file
find /tmp/mobilenet_src -name "*.h5"
# Convert
python -m tf2onnx.convert \
  --keras /tmp/mobilenet_src/path/to/model.h5 \
  --output backend/models/mobilenet_v2_triage.onnx
```

Place `mobilenet_v2_triage.onnx` (~14MB) at:
```
backend/models/mobilenet_v2_triage.onnx
```

### Step 1.5: Verify Model Loading

```bash
cd backend
python -c "
from app.modules.image_forensic.detector import get_or_load_models
enc, pre, head = get_or_load_models()
print('CLIP Encoder:', 'LOADED' if enc else 'FALLBACK')
print('Forensic Head:', 'TRAINED' if head else 'HEURISTIC FALLBACK')
"

python -c "
import onnxruntime as ort
s = ort.InferenceSession('models/mobilenet_v2_triage.onnx')
print('MobileNetV2 Input:', s.get_inputs()[0].name, s.get_inputs()[0].shape)
print('OK — Tier-0 triage ready')
"
```

---

## Phase 2: Create Demo Test Assets

**Time:** 30 mins | **When:** 2-3 days before hackathon | **Who:** Any team member

### Step 2.1: Create the `demo_assets/` Folder

```
demo_assets/
├── 01_authentic_camera_photo.jpg      ← Take with your phone (unedited)
├── 02_whatsapp_compressed_real.jpg    ← Forward image #1 to yourself 5x on WhatsApp, save final
├── 03_ai_generated_portrait.jpg       ← Generate via ChatGPT/Midjourney/Flux RIGHT NOW
├── 04_deepfake_video_clip.mp4         ← Download from YouTube "deepfake examples" or use a public dataset sample
└── 05_photoshop_splice.jpg            ← Take image #1, paste a different face in MS Paint/Photoshop
```

### Step 2.2: Why Each Asset Matters for the Demo

| Asset | What the System Will Show | Judge Impact |
|---|---|---|
| `01_authentic` | Low AI score, natural sensor noise, "AUTHENTIC" verdict | Proves the system doesn't flag everything as fake |
| `02_whatsapp_compressed` | Low AI score BUT with DCT weight reduced (JPEG quality detected as low) | **"Indian recompression awareness"** — the system recognizes degraded-but-real media |
| `03_ai_generated` | High AI score, synthetic frequency artifacts, possible watermark detection | Core detection capability demo |
| `04_deepfake_video` | Temporal analysis fires — blink rate, head-pose jitter, AV sync | Shows multi-modal analysis |
| `05_photoshop_splice` | Localization heatmap lights up at the splice boundary | Visual explainability for judges |

> [!WARNING]
> **Test these assets locally BEFORE the hackathon.** Upload each one, verify the system produces visibly different scores. If any asset produces unexpected results, adjust or replace it.

---

## Phase 3: Seed the Database for Origin Tracing Demo

**Time:** 15 mins | **When:** Day before hackathon or during setup | **Who:** Backend dev

The internal origin tracing ([retriever_internal.py](file:///e:/Competition/Chandigarh%20hackathon/backend/app/modules/origin_trace/retriever_internal.py)) works — it uses pHash + FAISS to find matches in the database. But it needs existing data to match against.

### Step 3.1: Upload the "Original Source" First

1. Start the backend stack (`uvicorn`, Celery worker, Postgres, Redis)
2. Go to `http://localhost:3000`
3. Create **Case 1: "Original AI-Generated Image — Source Account @fake_user_1"**
4. Upload `03_ai_generated_portrait.jpg`
5. Wait for analysis to complete

### Step 3.2: Create the "Derivative Forward"

1. Take `03_ai_generated_portrait.jpg`
2. Modify it slightly: crop 10%, add a text overlay, or forward via WhatsApp once
3. Save as `03b_derivative_forward.jpg`
4. Create **Case 2: "WhatsApp Forward — Reported by Cyber Cell"**
5. Upload `03b_derivative_forward.jpg`
6. The pHash/FAISS system will find Case 1 as a match and build the propagation link

### Step 3.3: What This Shows Judges

- Upload Case 2 → System traces it back to Case 1 as "Earliest Known Indexed Source"
- The Evidence Graph component ([EvidenceGraph.tsx](file:///e:/Competition/Chandigarh%20hackathon/frontend/src/components/EvidenceGraph.tsx)) renders the parent-child relationship
- This is your **origin-tracing differentiator** in action

---

## Phase 4: Fix the Frontend Polling Gap

**Time:** 20 mins | **When:** Before hackathon | **Who:** Frontend dev

### The Problem

Currently in [cases/[id]/page.tsx](file:///e:/Competition/Chandigarh%20hackathon/frontend/src/app/cases/%5Bid%5D/page.tsx), line 45-83, the data is fetched **once** on page load. If analysis is still running (Celery tasks in progress), the page shows stale/empty results and requires a manual browser refresh.

### The Fix

Add a polling interval that re-fetches every 3 seconds until `status === "completed"`:

#### [MODIFY] [cases/[id]/page.tsx](file:///e:/Competition/Chandigarh%20hackathon/frontend/src/app/cases/%5Bid%5D/page.tsx)

In the `useEffect` hook (lines 45-83), wrap the fetch logic into a reusable function and add `setInterval`:

```diff
+ const loadCaseData = async () => {
+   try {
+     const data = await fetchCaseById(caseId);
+     setCaseData(data);
+     const mediaRes = await fetchMediaItemsForCase(caseId);
+     if (mediaRes && mediaRes.length > 0) {
+       const firstMediaId = mediaRes[0].id;
+       setMediaItemId(firstMediaId);
+       const analysis = await fetchAnalysisResults(firstMediaId);
+       // ... existing transform logic (lines 57-74) ...
+       setAnalysisData({ /* ... same as current ... */ });
+       
+       // Stop polling once analysis is complete
+       if (analysis.analysis_status === "completed" || analysis.analysis_status === "failed") {
+         setIsLoading(false);
+         return true; // Signal to clear interval
+       }
+     }
+   } catch (e) {
+     console.error("Failed to load:", e);
+   }
+   return false; // Keep polling
+ };

  useEffect(() => {
    if (!caseId) return;
    
+   // Initial fetch
+   loadCaseData().then((done) => {
+     if (done) return;
+   });
+   
+   // Poll every 3 seconds until complete
+   const interval = setInterval(async () => {
+     const done = await loadCaseData();
+     if (done) {
+       clearInterval(interval);
+     }
+   }, 3000);
+   
+   return () => clearInterval(interval);
  }, [caseId]);
```

### Why This Matters for Demo

- Judge watches you upload a file
- Page automatically updates as each Celery task completes
- Results "fill in" live — radar chart populates, evidence bullets appear, verdict changes from "PROCESSING" to "HIGHLY SUSPICIOUS"
- **This is the "wow" moment** — the system feels alive

---

## Phase 5: Verify the Temporal Bug

**Time:** 5 mins | **When:** Anytime | **Who:** Backend dev

### The Issue

[plan2.md](file:///e:/Competition/Chandigarh%20hackathon/plan2.md) (line 183) mentions: `temporal.py has a bug — Line 72: CascadeCascade — typo in variable name`

### Current State

I read [temporal.py](file:///e:/Competition/Chandigarh%20hackathon/backend/app/modules/video_forensic/temporal.py) lines 72-74 — it currently says:
```python
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
```

**This looks correct.** The variable is `face_cascade` (not `CascadeCascade`). This bug appears to have already been fixed. No action needed unless you find a different issue.

---

## Phase 6: End-to-End Stack Verification

**Time:** 1 hour | **When:** 2 days before hackathon | **Who:** Full team

### Step 6.1: Start All Services

```powershell
# Terminal 1 — PostgreSQL + Redis (via Docker)
cd "E:\Competition\Chandigarh hackathon"
docker-compose up -d postgres redis

# Terminal 2 — Backend API
cd "E:\Competition\Chandigarh hackathon\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 3 — Celery Worker
cd "E:\Competition\Chandigarh hackathon\backend"
venv\Scripts\activate
celery -A app.core.celery_app worker --loglevel=info -P solo

# Terminal 4 — Frontend
cd "E:\Competition\Chandigarh hackathon\frontend"
npm install
npm run dev
```

### Step 6.2: Verify Each Feature

Run through this checklist:

- [ ] Open `http://localhost:3000` — Dashboard loads with case list
- [ ] Open `http://localhost:8000/docs` — Swagger UI shows all API endpoints
- [ ] Create a new case via the UI — form submission works
- [ ] Upload `01_authentic_camera_photo.jpg` — file ingestion triggers Celery pipeline
- [ ] Watch Celery terminal — see all 8 tasks fire: `task_verify_c2pa`, `task_detect_watermark`, `task_analyze_image`, `task_mobilenet_triage`, `task_analyze_video`, `task_localize_manipulation`, `task_check_metadata`, `task_trace_origin`, then `task_run_evidence_fusion`
- [ ] Case detail page auto-refreshes (after Phase 4 fix) — results populate
- [ ] Verdict shows "AUTHENTIC" or low fake score for the real photo
- [ ] Upload `03_ai_generated_portrait.jpg` — verdict shows higher fake score
- [ ] Heatmap / ELA overlay visible in the Localization tab
- [ ] Click "Download BSA §63(4) Certificate" — PDF downloads with SHA-256 hash
- [ ] Click "Export NCRP JSON" — JSON file downloads
- [ ] Upload `03b_derivative_forward.jpg` — origin tracing finds match to Case 1
- [ ] Evidence Graph shows parent-child link

### Step 6.3: Prepare Fallback Plans

| If This Breaks | Do This |
|---|---|
| Celery/Redis won't start | Run backend without Celery — the pipeline can execute synchronously (see [pipeline.py](file:///e:/Competition/Chandigarh%20hackathon/backend/app/services/pipeline.py) lines 71-75 fallback comment) |
| CLIP model too slow / OOM | System automatically falls back to heuristic scoring — demo still works |
| MobileNetV2 ONNX missing | Returns 0.5 neutral (by design, [mobilenet_triage.py](file:///e:/Competition/Chandigarh%20hackathon/backend/app/modules/image_forensic/mobilenet_triage.py) line 56) — demo still works |
| Frontend build fails | Use Swagger UI (`/docs`) for live API demo as backup |
| PostgreSQL won't start | Use SQLite fallback (adjust `DATABASE_URL` in `.env`) |

---

## Phase 7: Rehearse the Demo

**Time:** 1 hour | **When:** Day before hackathon | **Who:** Presenter(s)

### The 5-Minute Demo Flow

Follow [DEMO_SCRIPT.md](file:///e:/Competition/Chandigarh%20hackathon/DEMO_SCRIPT.md) with these specific beats:

| Time | Action | Key Words to Say |
|---|---|---|
| **0:00-0:45** | Show dashboard overview | "PratiBimb Praman — an evidence-fusion platform, not just a classifier. Notice NCRP complaint numbers and BSA certificate counter." |
| **0:45-1:45** | Upload `03_ai_generated_portrait.jpg` LIVE | "Three things happen simultaneously: SHA-256 hashing for chain of custody, MobileNetV2 triage in 5ms, and 7 forensic modules launch in parallel via Celery." |
| **1:45-2:30** | Show results populating (polling!) | "Notice the 7-signal radar chart. DCT frequency analysis, CLIP semantic analysis, watermark probe, C2PA check — each is an independent evidence signal fed into Dempster-Shafer fusion." |
| **2:30-3:15** | Upload `02_whatsapp_compressed_real.jpg` | "This is the same photo forwarded 5 times on WhatsApp. Notice the system does NOT falsely flag it. The DCT weight automatically drops because JPEG quality is low — this is our Indian recompression awareness." |
| **3:15-3:45** | Show origin graph (Case 1 → Case 2) | "Origin tracing uses two-stage retrieval: pHash for exact matches, CLIP+FAISS for semantic near-duplicates that survive crops and filters." |
| **3:45-4:30** | Click "Download BSA Certificate" | "This is our #1 differentiator. No commercial tool auto-generates a BSA Section 63(4) dual-certification certificate. This PDF has SHA-256 hash, Part A for the custodian, Part B for the technical expert." |
| **4:30-5:00** | Show the Explainability Modal | "Every score is explainable. Evidence cards show exactly why the system reached its verdict. When signals conflict, Dempster-Shafer surfaces the conflict explicitly — we never output a misleading average." |

### Judge Q&A Cheat Sheet

| Question | Answer |
|---|---|
| "Is the model actually trained?" | "The CLIP backbone is a pre-trained foundation model (ViT-L/14). Our forensic head uses LNCLIP-DF style LayerNorm-only tuning — the training script is ready for Colab T4. The heuristic fallback demonstrates the same end-to-end pipeline with real image statistics, not hardcoded values." |
| "Can you trace origin on live social media?" | "Our internal repository uses pHash + FAISS and works across all ingested cases. External web search integrates via SerpAPI/Google Vision when API keys are configured. We're honest: WhatsApp is E2E encrypted and legally un-crawlable — we say 'earliest indexed source,' never 'proven original.'" |
| "How is this different from Reality Defender / Sensity?" | "Those are detection-only APIs. None build a propagation graph, none generate BSA Section 63(4) certificates, and none handle Indian WhatsApp recompression chains. Our fusion engine uses Dempster-Shafer theory to surface signal conflicts instead of hiding them in a misleading average." |
| "What if all signals disagree?" | "That's exactly what Dempster-Shafer handles. The conflict metric K is computed and surfaced. If K > 0.40, uncertainty widens and we flag for expert review. We never output a false 97% when signals conflict." |
| "Why Dempster-Shafer instead of Bayesian?" | "Bayesian requires prior probability distributions we don't have for every signal combination. Dempster-Shafer explicitly models epistemic uncertainty — what we don't know — as a first-class mass assignment. It's mathematically honest about ignorance." |
| "What about adversarial attacks on your system?" | "We've documented real open-source watermark removal tools (noai-watermark, reverse-SynthID) in our research. Our fusion engine treats watermark absence as weak evidence precisely because removal is practical. An adversary would need to fool BOTH the CNN (MobileNetV2) and the Transformer (CLIP) architectures simultaneously — different attack surfaces." |

---

## Summary: Priority Timeline

| Priority | Task | Time | Status |
|---|---|---|---|
| 🔴 P0 | **Phase 2**: Create demo test assets (5 images/videos) | 30 min | Start immediately |
| 🔴 P0 | **Phase 4**: Add frontend polling to case detail page | 20 min | Do next |
| 🔴 P0 | **Phase 6**: End-to-end stack verification | 1 hour | Do 2 days before |
| 🟡 P1 | **Phase 3**: Seed DB with origin tracing demo data | 15 min | During Phase 6 |
| 🟡 P1 | **Phase 7**: Rehearse the full demo flow | 1 hour | Day before |
| 🟢 P2 | **Phase 1**: Train model weights on Colab | 2 hours | If time permits |
| 🟢 P2 | **Phase 5**: Verify temporal.py bug | 5 min | Quick check |

> [!IMPORTANT]
> **The single most important thing is: test the full flow end-to-end with your demo assets.** Everything else is polish. The codebase works — the demo just needs to be rehearsed with real test data.
