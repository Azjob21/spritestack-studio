# SpriteStack Studio – AI UI Integration (App-Side Contract)

This document describes **how the current app consumes AI responses and renders them**.  
It is for backend/API implementation alignment only; no API server code is included here.

## Runtime + transport

- Base URL used by app: `http://127.0.0.1:8000`
- Networking is non-blocking via `QNetworkAccessManager` (`reply.finished` callbacks).
- On network/decode errors, the app shows a status-bar message and skips rendering for that action.

---

## 1. AI Scene Construction (`/parse-scene`)

### Request (from `SceneUIPanel`)

- Method: `POST`
- Content-Type: `application/json`
- Body:

```json
{
  "prompt": "tree on left, rock on right"
}
```

### Response shape expected by UI

Top-level must be a **JSON object** (dict).  
Inside it, placements can be provided through one of:

- `placements`
- `objects`
- `sprites`
- `scene` (either list or object containing `objects` / `placements`)

Each item can include:

- identity: `name` (fallbacks: `object`, `sprite`, `label`)
- type: `type` (`stack`, `sprite`, `texture`; invalid values fallback to `sprite`)
- position:
  - numeric: `x`/`y` or `normalized_x`/`normalized_y` (0..1 recommended)
  - semantic: `position` or `anchor` with values like `left`, `center`, `right`, `top`, `bottom`, `top-left`, etc.
  - or string `"x,y"` / object `{ "x": ..., "y": ... }`
- transforms: `scale`, `rotation`
- visibility: `visible`
- alpha: `opacity` (0..255)

### Rendering path in app

1. `scene_ui.py` parses JSON and emits `scene_parsed(payload, prompt)`.
2. `main_window.py::_on_ai_scene_parsed` calls `parse_ai_scene_payload(...)`.
3. `scene_model.py` normalizes positions and values.
4. `apply_ai_scene_layout(...)` applies to current scene:
   - normalized coords become scene offsets:
   - `offset_x = (nx - 0.5) * canvas_width`
   - `offset_y = (ny - 0.5) * canvas_height`
5. Missing objects are auto-created by name/type, then scene placement is updated.

---

## 2. Voice Input / Whisper (`/transcribe`)

### Request (from `SceneUIPanel`)

- Method: `POST`
- Content-Type: `multipart/form-data`
- File part:
  - field name: `file`
  - filename: `prompt.wav`
  - mime: `audio/wav`

### Response shape expected

Top-level JSON object with transcript text in first available key:

1. `text`
2. `transcript`
3. `prompt`

If text is empty, app shows an error message and does not continue.

### Rendering/flow in app

1. Returned transcript fills the scene prompt input.
2. App auto-triggers `/parse-scene` with that text.
3. Scene rendering then follows the same path as section 1.

---

## 3. AI Pixel Art Tool (`/generate-sprite`)

### UI trigger

- Tool sidebar includes `AI Assist`.
- Selecting this tool opens a prompt dialog in `main_window.py`.

### Request

- Method: `POST`
- Content-Type: `application/json`
- Body:

```json
{
  "prompt": "small slime enemy",
  "width": 64,
  "height": 64
}
```

### Response decoding accepted by app

The decoder is permissive. It can consume:

- dict wrappers containing `frames` or `intermediate_frames` (uses first item)
- direct image fields: `hex`, `pixels`, `pixel_hex`, `data`, `image`
- optional dimensions: `width`/`height` or `w`/`h`
- list payloads:
  - token list of hex colors (`RRGGBB` or `RRGGBBAA`)
  - or list fragments concatenated as one hex stream
- string payloads:
  - continuous hex stream (`RRGGBB...` or `RRGGBBAA...`)
  - non-hex characters are stripped before decoding

### Rendering path in app

1. Response is decoded into `QImage` (`_decode_ai_image`).
2. `canvas.insert_image_layer(image, name="AI N")` inserts as a new layer.
3. Image is fit/centered to canvas size if dimensions differ.
4. Layer/timeline UI refreshes.

---

## 4. Keyframe Prediction (`/tween-frames`)

### UI trigger

- Timeline has button: **Predict Intermediate Frames**.
- It uses current frame + next frame; if unavailable, request is not sent.

### Request

- Method: `POST`
- Content-Type: `application/json`
- Body:

```json
{
  "current_frame": {
    "width": 64,
    "height": 64,
    "hex": "<RGBA8888 full-frame hex stream>"
  },
  "next_frame": {
    "width": 64,
    "height": 64,
    "hex": "<RGBA8888 full-frame hex stream>"
  },
  "num_intermediate": 1
}
```

`hex` is generated from `QImage.Format_RGBA8888` bytes.

### Response keys used by app

- confidence score: `confidence` (fallback key: `score`)
- predicted frame payload priority:
  1. `frames[0]`
  2. `intermediate_frames[0]`
  3. `frame`
  4. `intermediate`
  5. `result`

The selected frame payload is decoded using the same image decoder as `/generate-sprite`.

### Decision logic + rendering

- Confidence threshold in app: `0.65`.
- If decoded AI frame exists **and** `confidence >= 0.65`:
  - use AI output.
- Otherwise:
  - use NumPy linear interpolation (`t=0.5`) between current and next frames.

Then app:

1. inserts a new frame after current index,
2. writes chosen image into active layer of that inserted frame,
3. loads the inserted frame and refreshes timeline/layers.

---

## Minimal response examples (safe targets)

### `/parse-scene`

```json
{
  "placements": [
    { "name": "Tree", "type": "sprite", "position": "left", "scale": 1.0 },
    { "name": "Rock", "type": "sprite", "position": "right", "scale": 1.0 }
  ]
}
```

### `/transcribe`

```json
{ "text": "tree on left rock on right" }
```

### `/generate-sprite`

```json
{
  "width": 64,
  "height": 64,
  "pixels": ["00000000", "FF0000FF", "..."]
}
```

### `/tween-frames`

```json
{
  "confidence": 0.82,
  "frames": [
    { "width": 64, "height": 64, "pixels": ["...", "..."] }
  ]
}
```
