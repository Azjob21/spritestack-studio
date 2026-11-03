# SpriteStack Studio — AI Features & Architecture

This document details how each AI feature in SpriteStack Studio is **implemented**, what **models and architectures** power them, and how the **desktop app communicates with the AI backend**.

---

## System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                     PyQt5 Desktop Application                    │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ SceneUIPanel  │  │  AIGenPanel  │  │     AIChatPanel        │ │
│  │ (scene_ui.py) │  │(ai_gen_panel)│  │  (ai_chat_panel.py)   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬─────────────┘ │
│         │                  │                      │               │
│         └──────────┬───────┴──────────────────────┘               │
│                    ▼                                              │
│          QNetworkAccessManager (async, non-blocking)              │
│                    │                                              │
│  ┌─────────────────┴──────────────────────────────────────────┐  │
│  │ MainWindow — AI Response Handlers                          │  │
│  │  • _decode_ai_image()      — universal pixel decoder       │  │
│  │  • parse_ai_scene_payload()— scene JSON normalizer         │  │
│  │  • apply_ai_scene_layout() — scene object placement        │  │
│  │  • canvas.insert_image_layer() — layer insertion           │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────────┘
                         │  HTTP (localhost:8000)
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                    FastAPI Server (api/server.py)                 │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │               Dynamic Plugin Registry                      │  │
│  │                                                            │  │
│  │  At startup, checks which model weights exist on disk:     │  │
│  │   • Model found   → loads real_*.py  (actual inference)    │  │
│  │   • Model missing  → loads fake_*.py (procedural fallback) │  │
│  │   • Real crashes   → auto-falls back to fake_*.py          │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Endpoints:                                                      │
│    POST /parse-scene      → real_parse_scene / fake_parse_scene  │
│    POST /transcribe       → real_transcribe / fake_transcribe    │
│    POST /generate-sprite  → real_generate_sprite / fake_generate │
│    POST /tween-frames     → real_tween_frames / fake_tween       │
│    POST /chat             → fake_chat (rule-based)               │
│    POST /inpaint-region   → fake_inpaint_region (procedural)     │
│    GET  /health           → plugin status + model availability   │
└──────────────────────────────────────────────────────────────────┘
```

All AI communication is **asynchronous and non-blocking** — the Qt app fires HTTP requests via `QNetworkAccessManager` and processes responses through signal callbacks. The UI never freezes waiting for inference.

---

## 1. AI Scene Construction

**Endpoint:** `POST /parse-scene`  
**App trigger:** Scene prompt bar (text input or transcribed voice)

### What It Does

Takes a natural-language scene description like _"a dungeon with 2 knights on the left and a dragon on the right"_ and produces structured object placements with normalized positions, types, and counts.

### Model Architecture

| Component                               | Details                                                                              |
| --------------------------------------- | ------------------------------------------------------------------------------------ |
| **Stage 1 — NER (Model A)**             | Fine-tuned `distilbert-base-uncased` (HuggingFace `AutoModelForTokenClassification`) |
| **Stage 2 — Level Generator (Model B)** | `ConditionalArchitectTransformer` — 4-layer autoregressive grid generator            |
| **Fine-tuned on**                       | Custom SpriteStack scene description dataset + Video Game Level Corpus (VGLC)        |
| **Model A size**                        | ~265 MB (`model.safetensors`)                                                        |
| **Model B size**                        | ~3.2 MB (`architect_transformer_weights.pth`)                                        |
| **Inference speed**                     | ~50ms on CPU (NER)                                                                   |

The scene parser uses a **two-stage pipeline**:

- **Model A (NER):** Extracts entities, counts, positions, and themes from the prompt.
- **Model B (Architect):** Takes extracted entities + optional left-context from a previous screen and generates a 16×16 tile grid with semantic layers (air, solid, loot, enemy, climbable, player).

If the full pipeline is unavailable, the system falls back to NER-only parsing with keyword-based spatial mapping.

**Entity labels** (BIO tagging scheme):

| Label       | Purpose            | Example                             |
| ----------- | ------------------ | ----------------------------------- |
| `OBJECT`    | Sprite/entity name | _"knight"_, _"dragon"_, _"tree"_    |
| `COUNT`     | Quantity           | _"two"_, _"3"_, _"several"_         |
| `POSITION`  | Spatial anchor     | _"on the left"_, _"top-right"_      |
| `ATTRIBUTE` | Visual properties  | _"red"_, _"large"_, _"glowing"_     |
| `THEME`     | Scene context      | _"dungeon"_, _"forest"_, _"castle"_ |

### Inference Pipeline

```
User prompt
    │
    ▼
┌────────────────────┐
│  1. Spell Check    │  PySpellchecker corrects typos
│     (pre-process)  │  "trhee kngihts" → "three knights"
└────────┬───────────┘
         ▼
┌────────────────────┐
│  2. Tokenize       │  DistilBERT WordPiece tokenizer
│                    │  max_length=128, padding, truncation
└────────┬───────────┘
         ▼
┌────────────────────┐
│  3. NER Inference  │  Forward pass → logits → argmax per token
│     (DistilBERT)   │  Extracts B-/I- entity spans (BIO scheme)
└────────┬───────────┘
         ▼
┌────────────────────┐
│  4. Post-process   │  • Group token spans into entities
│                    │  • Resolve COUNT words → integers ("two" → 2)
│                    │  • Normalize POSITION → semantic anchors
│                    │  • Deduplicate overlapping entities
└────────┬───────────┘
         ▼
┌────────────────────┐
│  5. Spatial Layout  │  Map positions to normalized (x, y) coords:
│                    │    "left" → (0.2, 0.5)
│                    │    "right" → (0.8, 0.5)
│                    │    "top-left" → (0.2, 0.2)
│                    │  Expand counted entities with x-offset jitter (±0.03)
└────────┬───────────┘
         ▼
  JSON response with object placements
```

**When Model B is available**, an additional stage runs:

```
NER entities + optional left_context (previous screen's rightmost 8 columns)
    │
    ▼
┌────────────────────────┐
│  Architect Transformer │  Autoregressive 16×16 tile grid generation
│  (Model B)             │  Tile types: 0=air, 1=solid, 2=loot,
│                        │    3=enemy, 4=climbable, 5=player
│                        │  Supports left-context stitching for
│                        │    seamless multi-screen worlds
└────────────┬───────────┘
             ▼
┌────────────────────────┐
│  Grid → Placements     │  Each non-air cell → normalized bbox:
│                        │    x = (col + 0.5) / grid_width
│                        │    y = (row + 0.5) / grid_height
│                        │  Player auto-placed above first solid
│                        │    tile if requested but missing
└────────────────────────┘
```

### Spatial Position Mapping

```
    (0.2, 0.2)     (0.5, 0.2)     (0.8, 0.2)
     top-left         top          top-right
         ┌──────────────────────────────┐
         │                              │
(0.1,0.5)│  (0.2,0.5)  (0.5,0.5)  (0.8,0.5)  │(0.9,0.5)
far-left │    left      center      right  │ far-right
         │                              │
         └──────────────────────────────┘
    (0.2, 0.8)     (0.5, 0.8)     (0.8, 0.8)
   bottom-left      bottom       bottom-right
```

### How the App Renders It

1. `SceneUIPanel` sends prompt (+ optional `left_context` grid from previous screen) → receives JSON.
2. `parse_ai_scene_payload()` normalizes the response — handles many key formats (`placements`, `objects`, `entities`, `sprites`, `tiles`), semantic positions, coordinate normalization, and bounding boxes.
3. Each item becomes an `ObjectPlacement` with normalized `(nx, ny)` coords.
4. `apply_ai_scene_layout()` converts to canvas offsets: `offset_x = (nx - 0.5) × canvas_width`.
5. **Multi-screen support:** For multi-screen worlds, screen-local normalized x is converted to global coordinates: `nx = (target_screen + local_x) / num_screens`.
6. **Procedural object generation** (`_ensure_ai_object`): Missing objects are auto-created with theme-aware placeholder graphics — brick patterns for solids, ladder rungs for climbables, treasure chests for loot, skull marks for enemies — based on the scene theme (dungeon, desert, grassland).
7. The 2.5D sandbox stage renders the final scene.

---

## 2. Voice Prompt Input (Speech-to-Text)

**Endpoint:** `POST /transcribe`  
**App trigger:** Microphone button in Scene UI panel

### What It Does

Records audio from the user's microphone, transcribes it locally, and auto-feeds the text into the scene construction pipeline.

### Model Architecture

| Component           | Details                                                         |
| ------------------- | --------------------------------------------------------------- |
| **Engine**          | `faster-whisper` (CTranslate2-optimized Whisper)                |
| **Model variant**   | `whisper-small-en` (English-only, ~244M parameters)             |
| **Quantization**    | `int8` on CPU, `float16` on CUDA                                |
| **Model size**      | ~483 MB                                                         |
| **Inference speed** | ~1–3s for short prompts on CPU                                  |
| **Configuration**   | Fully configurable via env vars (`SPRITESTACK_TRANSCRIPTION_*`) |

### Pipeline

```
┌───────────────────────┐
│  Qt App: Record Audio │  QAudioRecorder → 16kHz mono WAV
│  (scene_ui.py)        │  saved to temp file on disk
└───────────┬───────────┘
            │  POST /transcribe (multipart/form-data, field="file")
            ▼
┌───────────────────────┐
│  faster-whisper        │  • beam_size=5
│  Transcription         │  • language="en"
│                        │  • VAD filter enabled (500ms min silence)
│                        │  • Local files only (no downloads)
└───────────┬───────────┘
            │  {"text": "three knights on the left"}
            ▼
┌───────────────────────┐
│  Auto-trigger          │  Transcript fills the prompt input
│  /parse-scene          │  and immediately fires scene parsing
└───────────────────────┘
```

**Voice Activity Detection (VAD)** is enabled to skip silence, improving accuracy for short voice commands recorded in noisy environments.

---

## 3. AI Sprite Generation

**Endpoint:** `POST /generate-sprite`  
**App trigger:** AI Gen panel dock widget, or AI Assist drawing tool

### What It Does

Generates pixel art sprites from text prompts. The output is a color-quantized, pixelated image inserted as a new layer on the canvas.

### Model Architecture

| Component            | Details                                                                |
| -------------------- | ---------------------------------------------------------------------- |
| **Base model**       | Stable Diffusion 1.5 — LCM variant (`dreamshaper-8-lcm`)               |
| **LoRA**             | `PixelArtRedmond15V-PixelArt-PIXARFK.safetensors` (fused at scale 0.9) |
| **Scheduler**        | `LCMScheduler` (Latent Consistency Model — fast 4–8 step inference)    |
| **Precision**        | `float16` on CUDA, `float32` on CPU                                    |
| **Total model size** | ~4.3 GB (UNet 3.44 GB + Text Encoder 492 MB + VAE 335 MB + LoRA 27 MB) |
| **Inference speed**  | ~2–8s on GPU, ~30–60s on CPU                                           |

### Pipeline

```
User prompt: "small slime enemy"
    │
    ▼
┌──────────────────────────────────────────────────┐
│  1. Prompt Augmentation                          │
│     full_prompt = "pixel art, {prompt},           │
│       pixelated, retro game sprite,              │
│       transparent background"                     │
│     negative = "blurry, realistic, photograph,   │
│       3d render, smooth, anti-aliased"           │
└──────────────────┬───────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────┐
│  2. Stable Diffusion Inference (512×512)         │
│     • 8 LCM steps (fast convergence)             │
│     • guidance_scale = 1.8 (LCM sweet spot)       │
│     • LoRA fused: pixel art style enforcement    │
│     → produces 512×512 PIL Image                 │
└──────────────────┬───────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────┐
│  3. Nearest-Neighbor Pixelation                  │
│     512 → 64px (pixel_size=8) → back to 512     │
│     Creates hard pixel boundaries                │
│     (step-through via 256px for targets ≤ 32px)  │
└──────────────────┬───────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────┐
│  4. Resize to Target                             │
│     512×512 → target size (e.g. 32×32, 64×64)   │
│     Nearest-neighbor interpolation               │
└──────────────────┬───────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────┐
│  5. Color Quantization                           │
│     Reduce to 32 colors (MAXCOVERAGE, no dither) │
│     Alpha channel extracted, quantized separately,│
│     then recomposited as RGBA                    │
└──────────────────┬───────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────┐
│  6. Encode to Hex Stream                         │
│     RGBA pixels → "RRGGBBAA" uppercase hex       │
│     Continuous string in JSON response           │
└──────────────────────────────────────────────────┘
```

### How the App Renders It

The app's `_decode_ai_image()` is a **permissive multi-format decoder** that handles:

- Hex streams (RGB or RGBA, auto-detected by byte length)
- Lists of hex color strings
- Base64-encoded PNG data
- Nested `frames[]` or `intermediate_frames[]` wrappers

The decoded `QImage` is inserted as a new named layer (`"AI 1"`, `"AI 2"`, ...) via `canvas.insert_image_layer()` and scaled to fit the canvas if dimensions differ.

---

## 4. Keyframe Prediction (Animation Tweening)

**Endpoint:** `POST /tween-frames`  
**App trigger:** Timeline button — "Predict Intermediate Frames"

### What It Does

Given two animation keyframes, predicts intermediate frames to smooth out the animation. Includes a confidence score for quality gating.

### Model Architecture

| Component             | Details                                                                                      |
| --------------------- | -------------------------------------------------------------------------------------------- |
| **Base architecture** | Custom RIFE-RGBA (`IFNet_RGBA` — Real-Time Intermediate Flow Estimation)                     |
| **Format**            | TorchScript serialized (`.pt`), optimized with `torch.jit.optimize_for_inference`            |
| **Memory format**     | `channels_last` (NHWC) for CPU cache efficiency                                              |
| **Input**             | Two RGBA 64×64 frames → concatenated to `[1, 8, 64, 64]` tensor                              |
| **Output**            | Predicted RGBA frame `[1, 4, 64, 64]` + confidence scalar                                    |
| **Model size**        | ~43 MB                                                                                       |
| **Inference speed**   | ~28ms on CPU                                                                                 |
| **Threading**         | Offloaded to thread pool via `loop.run_in_executor()` to avoid blocking the async event loop |

### Pipeline

```
┌───────────────────────────────────────────────┐
│  App: Extract Frames                          │
│  current_frame + next_frame → QImage RGBA8888 │
│  Convert to hex streams                       │
└───────────────────┬───────────────────────────┘
                    │  POST /tween-frames
                    ▼
┌───────────────────────────────────────────────┐
│  1. Decode hex → tensors                      │
│     hex string → bytes → uint8 numpy array    │
│     → float32 torch tensor [4, H, W]         │
│     Resize to 64×64 if needed (bilinear)      │
└───────────────────┬───────────────────────────┘
                    ▼
┌───────────────────────────────────────────────┐
│  2. Concatenate frames                        │
│     [frame0(4ch), frame1(4ch)] → [8, 64, 64] │
│     + timestep t = 0.5 (midpoint)             │
└───────────────────┬───────────────────────────┘
                    ▼
┌───────────────────────────────────────────────┐
│  3. RIFE-RGBA Forward Pass (thread pool)      │
│     • Convert uint8 HWC → float32 NCHW [0,1]  │
│     • Set channels_last memory format         │
│     • Forward: model(frame0, frame1)          │
│     • Clamp [0,1] → scale ×255 → uint8       │
│     Output: predicted RGBA frame [4, 64, 64]  │
└───────────────────┬───────────────────────────┘
                    ▼
┌───────────────────────────────────────────────┐
│  4. Post-process                              │
│     Resize back to original dims if ≠ 64×64   │
│     Encode to uppercase RRGGBBAA hex stream   │
│     confidence = 0.95 on success              │
│     (0.10 on dimension mismatch, 0.0 on error)│
└───────────────────────────────────────────────┘
```

### Confidence-Gated Fallback (App-Side)

The app implements a **quality gate** to ensure animation integrity:

```
confidence >= 0.65 ?
    ├── YES → Use AI-predicted frame
    └── NO  → Use NumPy linear interpolation (t=0.5)
              lerp(current_pixels, next_pixels, 0.5)
```

The interpolated or predicted frame is inserted as a new frame after the current index in the timeline, written into the active layer.

---

## 5. AI Chat Assistant

**Endpoint:** `POST /chat`  
**App trigger:** AI Chat panel dock widget

### What It Does

Provides context-aware guidance on sprite creation — prompt engineering tips, style tag recommendations, palette suggestions, and blend mode advice. Currently **rule-based** (no ML model).

### How It Works

The app sends the user's message along with canvas context:

```json
{
  "message": "how do I make this sprite look more retro?",
  "context": {
    "canvas_width": 64,
    "canvas_height": 64,
    "layer_count": 5,
    "current_tool": "pencil",
    "primary_color": "#FF0000",
    "secondary_color": "#000000"
  }
}
```

The `fake_chat.py` handler uses keyword matching and rule-based response templates to provide relevant advice. Responses are rendered as HTML chat bubbles in the panel.

---

## 6. Region Inpainting

**Endpoint:** `POST /inpaint-region`  
**App trigger:** AI Gen panel (when canvas selection exists)

### What It Does

Replaces a selected canvas region with AI-generated content based on a prompt, respecting the surrounding context. Currently **procedural** (no ML model) — planned to use the same SD pipeline as sprite generation with inpainting masking.

---

## Plugin System — Graceful Degradation

The server's **dynamic plugin registry** (`api/server.py`) is the architectural centerpiece that makes the AI features modular and failure-tolerant.

### How It Works

At startup, the server checks which model weight files exist on disk:

```python
# Example: Parse Scene plugin selection
if (models/nlp_parser/.../SpriteStack_Model_Slim_v2/model.safetensors).exists():
    register → plugins.real_parse_scene    # Actual DistilBERT inference
else:
    register → plugins.fake_parse_scene    # Keyword-based procedural fallback
```

**Three-tier fallback chain:**

```
Request arrives
    │
    ▼
Real plugin loaded? ──YES──→ Run real inference
    │                              │
    NO                          Crashes?
    │                              │
    ▼                           YES
Run fake plugin               │
    │                          ▼
    ▼                     Run fake plugin (auto-fallback)
  Response                    │
                              ▼
                           Response
```

### Model Detection Paths

| Plugin            | Model Check                                        | Weight File                     |
| ----------------- | -------------------------------------------------- | ------------------------------- |
| `parse-scene`     | `models/nlp_parser/.../SpriteStack_Model_Slim_v2/` | `model.safetensors`             |
| `generate-sprite` | `models/pixel-art-model/`                          | `unet/` directory exists        |
| `transcribe`      | `models/whisper-small-en/`                         | `model.bin`                     |
| `tween-frames`    | `models/`                                          | `sprite_tweener_rgba_64_cpu.pt` |
| `chat`            | —                                                  | Always fake (rule-based)        |
| `inpaint-region`  | —                                                  | Always fake (procedural)        |

All models are **lazily loaded** — the first request triggers model loading into memory, subsequent requests reuse the singleton. This keeps startup fast.

---

## Model Summary Table

| Feature           | Model                             | Architecture                      | Parameters | Size on Disk | Device  | Speed         |
| ----------------- | --------------------------------- | --------------------------------- | ---------- | ------------ | ------- | ------------- |
| Scene Parser      | SpriteStack NER v2                | DistilBERT (Token Classification) | ~66M       | 265 MB       | CPU     | ~50ms         |
| Voice Input       | whisper-small-en                  | Whisper (CTranslate2, int8)       | ~244M      | 483 MB       | CPU     | ~1–3s         |
| Sprite Generation | dreamshaper-8-lcm + PixelArt LoRA | Stable Diffusion 1.5 + LCM + LoRA | ~860M      | 4.3 GB       | GPU/CPU | 2–8s / 30–60s |
| Frame Tweening    | sprite_tweener_rgba_64            | RIFE-RGBA (TorchScript)           | ~10M       | 43 MB        | CPU     | ~28ms         |
| Chat Assistant    | — (rule-based)                    | Keyword matching                  | —          | —            | CPU     | <1ms          |

---

## Separate Repositories

The AI model weights, training scripts, datasets, and model-specific configurations are **not included** in this repository. They are maintained in dedicated repos:

| Component               | Contents                                                                        | Repository      |
| ----------------------- | ------------------------------------------------------------------------------- | --------------- |
| **Pixel Art Diffusion** | SD 1.5 LCM checkpoint, PixelArt LoRA, conversion scripts                        | _Separate repo_ |
| **NLP Scene Parser**    | DistilBERT NER fine-tuning, training data, Architect Transformer, level corpora | _Separate repo_ |
| **Whisper STT**         | CTranslate2 whisper-small-en model files                                        | _Separate repo_ |
| **Sprite Tweener**      | RIFE-RGBA training, TorchScript export, frame interpolation datasets            | _Separate repo_ |

To run with real AI models, clone the model repos and place weights under `api/models/`. Without them, the app runs fully using procedural fallback handlers.
