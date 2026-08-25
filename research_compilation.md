# Research Compilation: AI-Generated/Altered Media Detection & Origin Tracing
### For: Chandigarh Police Hackathon — Problem Statement 4

This is a working research base — real papers, real datasets, real repos, real companies — pulled from current search (Aug 2026). Use it to ground the architecture doc so you're citing actual prior art in the pitch, not inventing plausible-sounding references. Links are current as of this search; verify before printing them on a slide.

---

## 1. Core surveys to read first (gives you the vocabulary + a defensible "related work" section)

| Paper | Venue/Date | Why it matters for you |
|---|---|---|
| [AI-Generated Image Detection: An Empirical Study and Future Research Directions](https://arxiv.org/abs/2511.02791) | arXiv, Nov 2025 | Directly names the three failure modes of typical student projects: non-standardized benchmarks, inconsistent training protocols, and evaluation metrics that don't capture generalization or explainability. Quote this gap in your problem-decomposition slide. |
| [Methods and Trends in Detecting AI-Generated Images: A Comprehensive Review](https://arxiv.org/abs/2502.15176) | arXiv, Feb–Oct 2025 | Categorizes detectors into spatial-domain, frequency-domain, fingerprint-based, patch-based, training-free, and multimodal reasoning-based families — use this taxonomy directly for your Part 5/16 architecture comparison table. |
| [NTIRE 2026 Challenge on Robust AI-Generated Image Detection in the Wild](https://arxiv.org/pdf/2604.11487) | arXiv, 2026 | A real 2026 challenge built on 108,750 real and 185,750 AI-generated images from 42 generators, with 36 realistic post-processing/transformation types — this is your ready-made template for the "Media Attack Simulator" (Part 9). Cite it as evidence your robustness methodology matches an active peer-reviewed benchmark. |
| [Community Forensics: Using Thousands of Generators to Train Fake Image Detectors](https://arxiv.org/abs/2411.04125) (Park & Owens) | 2024 | The best single citation for "how do you generalize to unseen generators" — trains across thousands of generator checkpoints instead of a handful. |
| [Towards Universal Fake Image Detectors That Generalize Across Generative Models](https://arxiv.org/abs/2302.10174) (Ojha, Li, Lee) — CVPR 2023 | CVPR 2023 | Foundational "use a frozen CLIP feature space instead of training a classifier from scratch" result — the basis for most 2024–2026 generalization work below. |
| [DF40: Toward Next-Generation Deepfake Detection](https://arxiv.org/abs/2406.13495) | NeurIPS 2024 | 40-method deepfake benchmark — good source of unseen-forgery-type splits for your Part 8 evaluation design. |
| [Deepfake Media Forensics: Status and Future Challenges](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11943306/) | 2025 | Names "Impostor Bias" — growing public skepticism toward all media authenticity as a second-order harm — a strong line for your ethics/limitations section (Part 28). |

**Generalization-specific (Part 8) — recent methods to reference in your ablation study:**
- LNCLIP-DF — fine-tunes only the LayerNorm parameters (0.03% of weights) of a frozen CLIP encoder and enforces a hyperspherical feature manifold with L2 normalization, evaluated across 13 benchmarks spanning 2019–2025 ([arXiv 2508.06248](https://arxiv.org/html/2508.06248v1)). Its finding that pairing real/fake data from the same source video prevents shortcut learning better than just adding more datasets is directly relevant to your data-leakage design (Part 15).
- DFD-FCG (CVPR'25) — CLIP-encoder-based side network for generalized video deepfake detection, with [open code](https://github.com/aiiu-lab/DFD-FCG).
- C2P-CLIP (AAAI 2025) — injects a category prompt into CLIP specifically to improve cross-generator generalization.

---

## 2. C2PA / Content Credentials — official tooling (Part 3)

This is real, actively maintained, and free — use the actual SDK rather than re-implementing manifest parsing.

- **c2pa-rs** — [github.com/contentauth/c2pa-rs](https://github.com/contentauth/c2pa-rs) — the official Rust SDK and reference implementation for creating and validating C2PA manifests, with Node.js and Python bindings.
- **c2patool** — CLI wrapper around c2pa-rs for inspecting/attaching manifests without writing code (github.com/contentauthenticity/c2patool).
- **c2pa-attacks** — [github.com/contentauth/c2pa-attacks](https://github.com/contentauth/c2pa-attacks) — an official "Content Authenticity Security Tool" built as a testing framework on top of the c2pa-rs SDK for probing how Content Credentials implementations fail. This is gold for your Part 20 (adversarial attacks) section — cite it directly as prior art for your own attack simulator.
- **CAI Open Source SDK docs** — opensource.contentauthenticity.org — explains manifest stores, active manifest, ingredients, assertions, hard/soft bindings in plain language.
- **c2pa.wiki** — community-maintained hub listing all official repos, the current spec (v2.2), and certificate-cost FAQs (~$50–500/yr for signing certs).
- **Chrome extension precedent**: [digimarc-corp/c2pa-content-credentials-extension](https://github.com/digimarc-corp/c2pa-content-credentials-extension) — a working example of consumer-facing C2PA + watermark verification in the browser; useful UI reference for your investigator dashboard.

---

## 3. Watermarking — detection *and* the removal arms race (Part 4)

Important finding for your threat model: watermark removal tools are now a mature, actively-developed open-source category, not a hypothetical attack. This *strengthens* your Part 20/21 threat model — you can cite real tools rather than speculating.

- **SynthID** (Google DeepMind) — the industry reference invisible watermark; embedded in Gemini/Imagen output.
- **Stable Signature** (Meta) — watermark baked into the decoder weights of latent diffusion models. Notably, [Stable Signature is Unstable (arXiv 2405.07145)](https://arxiv.org/pdf/2405.07145) demonstrates that a watermark once thought robust to detection can in fact be removed — cite this directly when you explain why your platform treats "watermark absent" ≠ "not AI" (a removed watermark looks identical to a never-watermarked image).
- **Removal tooling that now exists in the wild** (cite as adversary capability, not as something to build): `noai-watermark` uses diffusion-based regeneration — encoding into latent space, adding noise, and reconstructing — to strip SynthID/Stable Signature/Tree-Ring watermarks while preserving visual fidelity; `reverse-SynthID` documents a spectral-analysis attack pipeline that defeats Google's SynthID detector while remaining visually lossless. These are strong, concrete evidence for your "Part 20: adversarial attacks against our system" section.
- **Detection-side reality check**: an independent SynthID detector project found that a correlation-template approach only scored highly on the exact images used to build its templates and detected 0 of 33 held-out AI images — i.e., naive watermark-template matching does not generalize. Cite this as justification for why your platform should treat third-party/self-built watermark detectors as one weighted signal, never as ground truth.

**Design implication for your Part 12 scoring model**: given that watermark removal tools are now freely available, "watermark absent" carries much weaker evidentiary value than "watermark present." Your evidence-fusion weights should reflect this explicitly — it's a genuinely defensible, non-obvious point that will impress judges who know the space.

---

## 4. Datasets (Part 14)

### Video deepfake detection
| Dataset | Real / Fake | Manipulation types | Access |
|---|---|---|---|
| **FaceForensics++** | 1,000 real YouTube videos, 4,000 fake, across Deepfakes, Face2Face, FaceSwap, NeuralTextures | Face-swap + reenactment | Free, request form |
| **Celeb-DF v2** | 590 real videos, 5,639 deepfakes of 59 celebrities, built to reduce the visible splicing/color-mismatch artifacts of earlier sets | Face-swap | Free |
| **DFDC (Facebook/Meta)** | 128,154 facial videos of 960 subjects | Multiple face-swap methods + audio swap | Free (Kaggle) |
| **DeeperForensics-1.0, WildDeepfake, ForgeryNet, FFIW-10K, FakeAVCeleb, Celeb-DF++** | varies | broader "in the wild" and audio-visual variants | See the curated list below |
| **DeepfakeBench** ([SCLBD/DeepfakeBench](https://github.com/sclbd/deepfakebench)) | — | Not a dataset but a **benchmark harness** covering 9 datasets with a standardized train/eval pipeline and Docker setup — use this to run your cross-dataset evaluation (Part 15) instead of writing your own splits from scratch. |

### AI-generated image detection
- **GenImage** ([genimage-dataset.github.io](https://genimage-dataset.github.io), [GitHub](https://github.com/GenImage-Dataset/GenImage)) — over one million real/fake image pairs across ImageNet's 1000 classes, generated with Midjourney, Stable Diffusion, ADM, GLIDE, Wukong, VQDM, and BigGAN. This is your primary Tier-1 training/eval set for image-level detection — it already ships a **cross-generator protocol** matching exactly what Part 8 of your brief asks for.
- **DiffusionDB, WildFake, ArtiFact** — supplementary diffusion-image sets referenced alongside GenImage in recent surveys.

### Manipulation localization (Part 7 / 11)
| Dataset | Size | Types | Notes |
|---|---|---|---|
| **CASIA v1.0 / v2.0** | 921 / 5,123 tampered images with binary ground-truth masks | Splicing, copy-move | Most-cited localization benchmark; community-fixed masks at [namtpham/casia1groundtruth](https://github.com/namtpham/casia1groundtruth) and casia2groundtruth |
| **COVERAGE** | 100 manipulated images with masks | Copy-move | Small but standard |
| **IMD2020** | 2,010 real-world manipulated images collected from the internet with manually created masks | Mixed, "in the wild" | Closest to your real deployment conditions |
| **NIST16 / NIST MFC** | 564 images | Copy-move, remove, splicing | See NIST section below — this is the gold-standard government benchmark |
| **DEFACTO** | 229,000 | Splicing, copy-move, removal | Large-scale, auto-generated |
| **GIM** ([arXiv 2406.16531](https://arxiv.org/pdf/2406.16531)) | million-scale | Generative (diffusion-based) manipulation localization | Most relevant to *AI-edited* (not just spliced) regions — closer to your Task E/K |

Curated master list: **[greatzh/Image-Forgery-Datasets-List](https://github.com/greatzh/Image-Forgery-Datasets-List)** — maintained table of ~15 localization datasets with direct download links.

---

## 5. NIST — the actual government-grade evaluation program (cite this heavily; a police hackathon audience will recognize it)

- **NIST Open Media Forensics Challenge (OpenMFC)** — [nist.gov/itl/iad/mig/open-media-forensics-challenge](https://www.nist.gov/itl/iad/mig/open-media-forensics-challenge), evaluation portal at mfc.nist.gov. Grew out of the DARPA MediFor program and evaluates automated image/video manipulation detection and localization, including GAN-manipulation detection tasks.
- NIST explicitly frames the *real* forensic questions as broader than binary classification: has it been manipulated, was it malicious, who performed the manipulation, what was the original source, which tool was used, how and where was it manipulated — this list is essentially a validation of your Part 1 task decomposition. Put this NIST slide-quote directly in your deck.
- **NISTIR 8377** — the user guide for the MFC datasets (probe/journal structure, GAN-manipulation flags) — useful if you want to describe your own dataset schema in a NIST-compatible way.
- **AFI2 (Accelerating Forensic Innovation for Impact)** — a newer NIST competition explicitly aimed at building more realistic test data that incorporates post-processing, social-media laundering, and anti-forensic filters — cite this to justify why your Media Attack Simulator (Part 9) isn't optional polish, it's what the field's own evaluators consider necessary rigor.

---

## 6. Origin tracing / provenance retrieval tooling (Part 10)

- **Perceptual hashing**: pHash/dHash implementations are mature and simple — `imagehash` (Python), `imgdupes`, `fast-near-duplicate-image-search` (pHash + KDTree + t-SNE viz). Key caveat worth citing in your design doc: DCT-based pHash is robust to mild JPEG recompression, resizing, and small overlays, but breaks under flips, crops, and color shifts — which is exactly why Part 10 of your brief is right to layer pHash with CLIP embeddings, not rely on it alone.
- **FAISS + hashing at scale**: [mattpodolak/duplicate-img-detection](https://github.com/mattpodolak/duplicate-img-detection) is a clean minimal reference (FastAPI + imagehash + FAISS) for exactly the "reverse-image similarity service" your architecture needs — good starting scaffold rather than building the API layer from zero.
- **Learned-embedding near-duplicate detection**: recent large-scale work (Meta's MONET dataset pipeline) uses a **two-pass** approach — pHash first, then a learned SSCD embedding second pass to catch flips, large crops, color shifts, and watermark insertion that defeat pHash. This two-tier design is worth adopting directly and citing as informed by production-scale practice, not invented from scratch.
- Academic framing of exactly your problem: [Dataset and Case Studies for Visual Near-Duplicates Detection in the Context of Social Media (arXiv 2203.07167)](https://arxiv.org/pdf/2203.07167) — built specifically for tracking manipulated/re-shared images on social platforms, and explicitly rejects plain pHash in favor of learned features for this exact reason.

---

## 7. Industry landscape — what's already commercial (Part 22 differentiators / Part 24 judge Q&A ammunition)

Judges will ask "why isn't this already solved?" — here's the honest state of the market so you can answer precisely instead of vaguely.

| Company | Focus | Relevant detail |
|---|---|---|
| **Truepic** | Capture-time provenance + C2PA signing | Ranked highest on cryptographic C2PA signing integration among reviewed platforms, positions itself as "sign at capture" rather than "detect after the fact." |
| **Reality Defender** | Multi-modal deepfake detection API | Offers a free tier of 50 audio/image scans per month; broad video/audio/image/text coverage under one API — a real detection-only competitor, no provenance-tracing or origin-graph component. |
| **Sensity AI** | Forensic-grade detection for law enforcement/finance | Marketed explicitly for court-admissible evidence use — closest existing competitor to your target use case, but per public comparisons it does **not** publish an origin/propagation-graph capability. |
| **Hive Moderation** | Content-moderation-scale API | Can identify which specific generation model produced an image (Midjourney, DALL-E, Stable Diffusion) — i.e., generator attribution is already commercially solved at some level; don't pitch "we can tell which model made it" as your sole differentiator. |
| **Intel FakeCatcher** | Real-time video calls | Uses blood-flow/PPG signal analysis — a fundamentally different (biological-signal) approach, inapplicable to static images. |

**The gap this market genuinely has, per independent reviews**: Reality Defender, Sensity, and Hive are reactive — you bring them content and they score it; none of them proactively construct a propagation/origin graph across the open web for arbitrary content. That gap — evidence-graph-based origin tracing combined with calibrated, explainable fusion scoring — is your legitimate, defensible differentiator. Say this explicitly to judges: "the detection piece is commoditized; the origin-intelligence and evidence-fusion layer is not."

---

## 8. What this means for your Top-3 pitch (tying it back to Part 22)

Given the actual state of the field found above, the strongest, most honest differentiators are:

1. **Evidence-graph origin tracing** (Section 6/7 gap) — genuinely underserved by commercial tools.
2. **A calibrated, multi-signal fusion score with explicit uncertainty**, instead of a single "97% fake" number — directly motivated by NIST's own finding that lab accuracy doesn't transfer to field conditions, and by the watermark-removal arms race in Section 3 showing why single-signal confidence is fragile.
3. **Adversarial robustness testing built on real, existing attack tooling** (c2pa-attacks, SynthID-removal repos) rather than hypothetical transformations — you can demo an actual attack from a real open-source tool and show your system correctly downgrades confidence rather than falsely asserting "proven fake" or "proven real."
4. **Honest evidentiary language** ("earliest known source," "evidence suggests") aligned with how NIST itself frames the unanswerable questions in this space — this specifically targets a police/forensic audience's real concern: courtroom defensibility.

---

## Sources referenced above (for your bibliography)
- arXiv: 2511.02791, 2502.15176, 2604.11487, 2411.04125 (Community Forensics), 2508.06248 (LNCLIP-DF), 2406.13495 (DF40), 2405.07145 (Stable Signature is Unstable), 2306.08571 (GenImage), 2406.16531 (GIM), 2108.03871, 2203.07167
- NIST: nist.gov/itl/iad/mig/open-media-forensics-challenge, NISTIR 8377, mfc.nist.gov
- C2PA/CAI: github.com/contentauth/c2pa-rs, github.com/contentauth/c2pa-attacks, opensource.contentauthenticity.org, c2pa.wiki
- GitHub: SCLBD/DeepfakeBench, GenImage-Dataset/GenImage, greatzh/Image-Forgery-Datasets-List, aiiu-lab/DFD-FCG, mattpodolak/duplicate-img-detection, Rinne414/SynthID-detector, aloshdenny/reverse-SynthID
- Industry reviews: realitydefender.com, fast.io deepfake-detector comparison (2026), global100.org Reality Defender review, revelum.ai comparison
