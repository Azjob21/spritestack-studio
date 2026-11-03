# SpriteStack Studio — AI Modules Team Guide
**April 2026 | Confidential | Chief's Reference**

---

## Overview

All four modules run behind a single local FastAPI server at `http://127.0.0.1:8000`. Each team member owns their endpoints. The offline requirement is **non-negotiable** — every model must run with the network cable unplugged. Test this explicitly before the demo. Integration order is: **Parser → Whisper → Tweening → Pixel Art**.

---

## Quick Reference Table

| Module | Primary Paper | Dataset Source | Endpoint | Priority |
|---|---|---|---|---|
| NLP Parser | DistilBERT (Sanh et al.) | Custom via Chatette | `/parse-scene` | 1 — Start immediately |
| Speech-to-Text | Whisper (Radford et al.) | Mozilla Common Voice | `/transcribe` | 2 — After parser skeleton |
| Keyframe Tweening | U-Net (Ronneberger et al.) | Liberated Pixel Cup (LPC) | `/tween-frames` | 3 — After dataset pipeline |
| Pixel Art Gen | LoRA (Hu et al.) | Pixelart-Dataset (HuggingFace) | `/generate-sprite` | 4 — Bonus, after 1–3 stable |

---

## Module 1 — NLP Scene Parser

**Priority: 1 — Start immediately**

**Your job in one sentence:** Build the model that turns a sentence like *"a dungeon with two skeletons on the left and a chest in the center"* into a JSON object the canvas can render directly.

**Focus:** Slot-filling and Named Entity Recognition (NER)

### Approach

**Step 1 — Dataset Construction** (bulk of your time, primary academic contribution)

There is no existing dataset for game-scene NLP — you are building it from scratch. Use the template system to generate sentences programmatically by filling slots (scene type, object names, positions) from the provided vocabulary lists.

- Target **500–1,000 labeled sentences**
- Auto-generate BIO tags from slot offsets
- Do a manual review pass of roughly 2 hours to catch edge cases
- Keep a **90/10 train/test split** from the start
- Commit dataset to `ai/nlp_parser/dataset/`

**Step 2 — Model Training**

Fine-tune `distilbert-base-uncased` from Hugging Face with a token classification head for NER. Training runs **30–60 minutes on Colab CPU**.

**Step 3 — Inference Script**

Write an `infer.py` that takes a raw string and outputs structured JSON using the position-to-coordinate map:

| Position Word | Coordinates |
|---|---|
| `left` | `(0.15, 0.5)` |
| `center` | `(0.5, 0.5)` |
| *(add others per spec)* | — |

**Step 4 — API Endpoint**

Expose `/parse-scene` at `http://127.0.0.1:8000`:
- **Input:** `{"prompt": "..."}`
- **Output:** placement JSON
- The app's `SceneUIPanel` already calls this endpoint — your server just needs to answer it correctly.

### Deliverables

- Labeled dataset of 500–1,000 sentences committed to `ai/nlp_parser/dataset/`
- Trained model saved to `ai/nlp_parser/model/` that loads fully offline
- `infer.py` that accepts a string and returns valid JSON every single time — no malformed output
- Token-level **F1 ≥ 80%** on held-out test split
- Inference latency **under 200ms** for a 20-token sentence on CPU
- `/parse-scene` endpoint running and reachable at localhost before integration testing

### Research Papers

- **"Attention Is All You Need"** (Vaswani et al.) — Essential for understanding the Transformer architecture behind DistilBERT.
- **"DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter"** (Sanh et al.) — Explains why this model is ideal for CPU-bound tasks like your parser.
- **"A Survey on Recent Advances in Named Entity Recognition"** (Li et al.) — Provides context on the BIO tagging schema you are using.

### Data Resources

- **[Dataset] MultiATIS++** — While designed for travel, it is the gold standard for slot-filling (intent + entity). Use its structure to mirror your "scene type" and "object" labels.
- **[Tool] Chatette** — A powerful DSL (Domain Specific Language) to generate thousands of NLU sentences from your templates automatically.

---

## Module 2 — Speech-to-Text (Whisper)

**Priority: 2 — Start after parser skeleton exists**

**Your job in one sentence:** Let the user speak a scene description into a microphone and have it automatically transcribed and fed into the NLP parser — fully offline, zero internet.

**Focus:** Robust offline transcription and accent adaptation

### Approach

This is the fastest module in the project. Whisper base is plug-and-play: download the model once, it runs entirely from disk after that.

**Step 1 — Recording Pipeline**

Write `transcribe.py` that:
1. Records from the microphone to a `.wav` file
2. Runs `whisper.load_model('base').transcribe('recorded.wav')`
3. Extracts the `text` field
4. POSTs it to the parser's `/parse-scene` endpoint

**Step 2 — API Endpoint**

The app (`SceneUIPanel`) records a WAV, then POSTs it to `/transcribe` on your server. Your server:
- Receives the audio file
- Runs Whisper on it
- Returns `{"text": "..."}`

That is the entire contract.

**Optional — Accent Fine-Tuning**

If your school specifically requires you to train or fine-tune the ASR component, Algerian-accented French/Darija is a legitimate gap in Whisper's coverage. You could fine-tune `whisper-tiny` on Mozilla Common Voice Arabic + French data in **2–4 hours on a Colab T4**. Only pursue this if required — it is not needed for the core demo.

### Deliverables

- Whisper base model downloaded and saved to `ai/whisper_asr/model/` — runs with zero internet
- A `/transcribe` endpoint that accepts a WAV file upload and returns `{"text": "..."}`
- Word Error Rate **under 5%** on a 10-second English scene description
- Full end-to-end latency (speak → JSON placed on canvas) **under 3 seconds** on demo hardware
- A brief test document showing the pipeline working offline with the network disabled

### Research Papers

- **"Robust Speech Recognition via Large-Scale Weak Supervision"** (Radford et al.) — The original Whisper paper. Crucial for understanding why the "base" model handles noise well.
- **"Common Voice: A Massively-Multilingual Speech Corpus"** (Ardila et al.) — Relevant if you pursue the Algerian-accented fine-tuning.

### Data Resources

- **[Dataset] Mozilla Common Voice (Arabic/French)** — The primary source for fine-tuning Whisper on North African accents.
- **[Dataset] Google AudioSet** — Useful for identifying background noise if you need to preprocess audio before transcription.

---

## Module 3 — Keyframe Tweening

**Priority: 3 — Start after dataset pipeline is designed**

**Your job in one sentence:** Given two animation keyframes, generate the frame that belongs between them — not a blurry blend, but a correctly-shaped intermediate frame.

**Focus:** Pixel-perfect frame interpolation

### Approach

**Step 1 — Dataset Generation** (fully automated)

Download LPC (Liberated Pixel Cup) sprite sheets — they are **CC0 licensed**. Write `dataset_gen.py` to:
- Cut each sheet into individual frames
- Produce triplets in the form `(frame_i, frame_i+2, frame_i+1)` where `frame_i+1` is your ground truth
- Apply cheap augmentations: horizontal flip, rotation, recoloring — pixel art is small so this is fast

50 sprite sheets will give you thousands of training triplets.

**Step 2 — Model Training**

Train a **U-Net encoder-decoder** from scratch:
- Input: `frame_A` and `frame_B` concatenated as a **6-channel image** (RGBA + RGBA)
- Output: single RGBA frame at the same resolution
- Keep input resolution at **32×32 or 64×64**
- Use **L1 pixel loss** plus **perceptual loss** computed on VGG features of a 4× upscaled image
- Training takes **1–2 hours on Colab T4**

**Step 3 — API Endpoint**

Expose `/tween-frames`. The app sends:
```json
{
  "current_frame": {"hex": "..."},
  "next_frame": {"hex": "..."},
  "num_intermediate": 1
}
```
And expects back:
```json
{
  "frames": [...],
  "confidence": 0.0
}
```

The app has a confidence threshold of **0.65** — if your model returns confidence below that, the app falls back to NumPy linear interpolation automatically. Make sure your model outputs a meaningful confidence score (e.g. based on reconstruction loss).

**Step 4 — Demo Preparation**

Prepare a side-by-side comparison of Tier 1 (linear interpolation) versus Tier 2 (your model). Linear produces ghosting and blur. Your model should produce clean, crisp shape transitions. **This contrast is your strongest jury moment.**

### Deliverables

- Automated dataset pipeline in `ai/tweening/dataset_gen.py`
- Trained U-Net or Conv-LSTM model saved to `ai/tweening/model/`
- A `/tween-frames` endpoint matching the JSON contract above exactly
- **SSIM score above 0.75** on held-out test triplets
- Inference time **under 50ms per frame** on CPU
- Confidence score returned with every prediction so the app's fallback logic works
- Side-by-side comparison demo prepared for the jury showing Tier 1 vs Tier 2

### Research Papers

- **"U-Net: Convolutional Networks for Biomedical Image Segmentation"** (Ronneberger et al.) — Though originally for medical use, this is the foundational architecture for your encoder-decoder.
- **"Video Frame Interpolation via Adaptive Separable Convolution"** (Niklaus et al.) — Great for understanding how to handle motion between frames.
- **"Deep Video Frame Interpolation"** (Reda et al.) — Discusses the loss functions (L1 and Perceptual) you will be using.

### Data Resources

- **[Dataset] Liberated Pixel Cup (LPC)** — Your primary source for CC0 sprite sheets.
- **[Dataset] SMID (Stuttgart Many-In-Dataset)** — A high-frame-rate dataset; while not pixel art, the logic of "triplet" generation is well-documented here.

---

## Module 4 — AI Pixel Art Generation

**Priority: 4 — Bonus feature, begin only if modules 1–3 are stable**

**Your job in one sentence:** Take a text prompt like *"a red dragon head 32×32"* and generate a pixel art sprite as a valid image the canvas can immediately render as a new layer.

**Focus:** Sequential generation and LoRA adaptation

### Approach

The key insight is treating a 32×32 sprite as a **sequence of 1,024 hex color tokens** rather than an image generation problem. This means you can fine-tune GPT-2 small with LoRA instead of running a diffusion model, which would be impossible within this timeline.

**Step 1 — Dataset Pipeline**

Build `dataset_prep.py` in `ai/pixel_art_gen/`:
- Load PNG sprites, flatten to row-major pixel order
- Convert each pixel to `#RRGGBB` (transparent pixels become `#00000000`)
- Join into a space-separated string
- Pair with a caption from the filename or metadata
- Target **5,000–10,000 pairs** saved as `.jsonl`
- Source from the Pixelart-Dataset on Hugging Face or CC0 packs from itch.io

**Step 2 — Model Training**

Fine-tune `gpt2` with LoRA via Hugging Face PEFT:
- Task: causal language modeling — the model sees the caption and predicts the hex token sequence
- Training takes **2–3 hours on Colab T4** with roughly 2GB VRAM

**Step 3 — Inference Script**

After training:
1. Take a prompt string
2. Run the model, parse the 1,024 hex tokens back into pixel RGBA values
3. Assemble a `QImage`

**Step 4 — API Endpoint**

The app calls `/generate-sprite` with:
```json
{
  "prompt": "...",
  "width": 32,
  "height": 32
}
```
And expects back an object containing the image as a **hex-encoded pixel string**. The `_on_ai_sprite_ready` handler will decode it, scale it to canvas size, and insert it as a new named layer automatically.

> ⚠️ **Important — Latency:** Generation must complete in **under 5 seconds** on demo hardware. Test this early — GPT-2 on CPU is slow. If latency is a problem, quantize the model with `bitsandbytes int8` or limit `max_new_tokens` aggressively.

### Deliverables

- Dataset pipeline in `ai/pixel_art_gen/dataset_prep.py` producing `.jsonl` pairs
- Fine-tuned GPT-2 + LoRA model saved to `ai/pixel_art_gen/model/`
- A `/generate-sprite` endpoint matching the contract the app expects
- Output that parses cleanly back into a valid `QImage` without errors — no malformed hex
- At least **10 test prompts** generating recognizable sprites covering **5 distinct object categories**
- Generation latency **under 5 seconds** on demo hardware — benchmark this before the jury

### Research Papers

- **"Language Models are Few-Shot Learners"** (Brown et al.) — The GPT-3 paper; the principles of sequence-to-sequence generation apply directly to your GPT-2/Hex approach.
- **"LoRA: Low-Rank Adaptation of Large Language Models"** (Hu et al.) — Explains how you can fine-tune GPT-2 on a consumer GPU in under 3 hours.

### Data Resources

- **[Dataset] Pixelart-Dataset (Hugging Face)** — Contains over 10k images. This is your primary source for `(caption, hex_string)` pairs.
- **[Dataset] Bit-68 Dataset** — A specialized collection of very low-res pixel art (32×32 and 64×64) perfect for tokenization.

---

## Cross-Team Notes

**Server contract:** All four modules run behind the same local FastAPI server at `http://127.0.0.1:8000`. Each team member owns their endpoints. Agree on startup order and make sure the server launches with a single command before integration week.

**Offline requirement is non-negotiable:** Every model must run with the network cable unplugged. Test this explicitly before the demo. Any module that phones home during evaluation fails the academic requirement.

**Integration order:** Parser → Whisper → Tweening → Pixel Art. Do not wait for Module 4 to be perfect before integrating Modules 1–3. The parser alone is a defensible submission.
