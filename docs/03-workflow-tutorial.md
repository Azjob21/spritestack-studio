# Workflow Tutorial — From Blank Canvas to Exported Sprite Stack

This tutorial walks through the **complete workflow** end-to-end:

1. Drawing a simple sprite
2. Turning it into a stackable 3D object with layers
3. Animating it
4. Previewing it in 3D
5. Exporting it for use in a game or for sharing

We'll create a **small treasure chest** as our example.

---

## Prerequisites

- SpriteStack Studio is running (double-click the desktop shortcut or run `python main.py`).
- No prior experience with pixel art or sprite stacking required.

---

## Part 1 — Drawing a Simple Sprite

### Step 1: Create a New Canvas

1. Go to **File → New…** (`Ctrl+N`).
2. Set **Width** = `32`, **Height** = `32`.
3. Set **Initial Layers** = `1` (we'll add more later).
4. Click **OK**.

You now have a 32×32 transparent canvas with one layer.

### Step 2: Pick Your Colors

1. In the right panel, find the **Color** section.
2. In the palette dropdown, select **DB32** or your preferred palette.
3. Click a **brown** swatch for the chest wood (e.g., a medium brown).

### Step 3: Draw the Base Shape

1. Select the **Pencil** tool (`B`) from the Tools panel.
2. Set **Brush Size** to `1`.
3. Zoom in — press `Ctrl+=` a few times or scroll with `Ctrl+Wheel`.
4. Draw a rectangular base for the treasure chest:
   - Use the **Rectangle** tool (`R`) to outline a box roughly 20×12 pixels, centered on the canvas.
   - Switch back to **Pencil** and fill in details — a horizontal line across the middle for the lid seam, some darker lines for wood planks.
5. Use the **Fill** tool (`G`) to fill large interior areas with the wood color.
6. Pick a **golden yellow** and draw a small lock/clasp on the front center.

### Step 4: Refine

- Use the **Eyedropper** (`I`) to re-pick colors from existing pixels as needed.
- Use the **Eraser** (`E`) to clean up stray pixels.
- Add a darker brown for shadows on the bottom and right edges.
- Add a highlight (lighter brown or cream) on the top-left edges.

> **Checkpoint**: You should have a nice top-down view of a treasure chest on Layer 1. This is your base slice.

---

## Part 2 — Building the 3D Stack (Layer by Layer)

Sprite stacking creates 3D depth by drawing each layer as a horizontal cross-section from bottom to top.

### Step 5: Add Layers

1. In the **Layers** panel, click the **+ (Add)** button 5 times. You now have 6 layers total.
2. Rename them (right-click → Rename):
   - Layer 1: `Base`
   - Layer 2: `Lower Body`
   - Layer 3: `Upper Body`
   - Layer 4: `Lid Bottom`
   - Layer 5: `Lid Top`
   - Layer 6: `Clasp`

### Step 6: Draw Each Height Slice

**Layer 1 — Base** (already drawn in Part 1)  
This is the very bottom of the chest — the footprint when viewed from above.

**Layer 2 — Lower Body**

1. Click **Layer 2** in the Layers panel.
2. Draw a shape slightly smaller than Layer 1 (inset by 1 pixel on each side), with the same wood color.
3. Add darker edges for depth.

**Layer 3 — Upper Body**

1. Click **Layer 3**.
2. Same footprint as Layer 2 but add the horizontal lid-separation line.
3. Use a slightly different shade to start transitioning to the lid.

**Layer 4 — Lid Bottom**

1. Click **Layer 4**.
2. Draw the lid shape — same width as the body but with a slightly rounded or arched top profile.
3. Start curving the top edge upward (remove corner pixels).

**Layer 5 — Lid Top**

1. Click **Layer 5**.
2. A smaller shape — just the very top of the arched lid.
3. Add a highlight color along the top.

**Layer 6 — Clasp**

1. Click **Layer 6**.
2. Draw only the clasp/lock that protrudes from the front — a few golden pixels.

> **Shortcut — Auto Generate**: If you want to skip manual layer drawing, go to **Stack → Auto-Generate Layers from Base**. This automatically creates inward-shrinking duplicates of Layer 1. It's faster but less detailed than hand-drawn layers.

### Step 7: Check the 3D Preview

1. Click the **3D Preview** tab on the right panel.
2. You should see your treasure chest rendered in 3D!
3. Drag to rotate it. Adjust **Layer Spacing** to make it taller or flatter.
4. Try different **Render Modes** — Stack, Voxel, Billboard — to see which look you prefer.

> **Checkpoint**: Your chest looks like a 3D object in the preview. Each layer you drew is a visible slice.

---

## Part 3 — Animating the Sprite

Let's make the chest open and close — a 6-frame animation.

### Step 8: Set Up Frames

1. Look at the **Timeline** at the bottom.
2. You currently have **Frame 1** (the closed chest). This is our starting pose.
3. Click **Dup (Duplicate Frame)** 5 times — you now have 6 identical frames.

### Step 9: Edit Each Frame

**Frame 1** — Closed chest (already done, no changes needed).

**Frame 2** — Lid starts to open:

1. Click Frame 2's thumbnail in the timeline.
2. Select **Layer 5 (Lid Top)**.
3. Shift the lid pixels upward by 1–2 pixels using select + move, or erase and redraw.
4. Select **Layer 4 (Lid Bottom)** — shift its top edge upward slightly.

**Frame 3** — Lid half-open:

1. Click Frame 3.
2. Move lid layers (4 & 5) further up. The lid should be visibly tilted/open.
3. You might thin the lid layers or shift them backward (toward the top of the canvas, which represents the "back" of the chest).

**Frame 4** — Lid almost fully open:

1. Click Frame 4.
2. Lid layers are now behind the body, shifted up and back significantly.

**Frame 5** — Fully open:

1. Click Frame 5.
2. Lid layers are at maximum height/offset. You can see inside the chest.
3. Optionally, add some sparkle or glow pixels inside the chest body layers.

**Frame 6** — Sparkle / Gold visible:

1. Click Frame 6.
2. Keep lid open. Add golden pixel highlights inside the chest (on Layers 2–3) to suggest treasure.

### Step 10: Preview the Animation

1. Set **FPS** to `8` in the timeline FPS spinbox.
2. Click **▶ Play** (or press `F5`).
3. Watch the chest open in a loop!
4. Adjust timing — slow it down (lower FPS) or speed it up (higher FPS).
5. **Enable Onion Skin** to see the previous frame as a ghost when editing, making alignment easier.

> **Tip**: For a "ping-pong" effect (open then close), duplicate frames 4-3-2 after frame 6, giving you: 1-2-3-4-5-6-5-4-3-2... repeat.

> **Checkpoint**: You have a 6-frame "chest opening" animation with smooth lid movement.

---

## Part 4 — Fine-Tuning the 3D Preview

### Step 11: Adjust 3D Settings

1. Switch to the **3D Preview** tab.
2. Scrub through animation frames in the timeline — the 3D preview updates for each frame.
3. Fine-tune these controls:

| Control            | Recommendation                          |
| ------------------ | --------------------------------------- |
| **Layer Spacing**  | 1.5–3.0 for a natural look              |
| **Render Mode**    | `Stack` for game-ready output           |
| **Outlines**       | ✅ On — helps definition at small sizes |
| **Shadows**        | ✅ On — adds grounding                  |
| **Auto Rotate**    | ✅ On to preview all angles             |
| **Rotation Speed** | ~30 for a gentle spin                   |

### Step 12: Check All Angles

With **Auto Rotate** on, watch the chest from every angle.  
If any angle looks wrong (gaps between layers, misaligned pixels), go back to the canvas and fix the relevant layer.

---

## Part 5 — Exporting

### Export A: Rotation Sprite Sheet (for Game Engines)

This is the most common export for sprite stacking games.

1. Go to **File → Export…** (`Ctrl+E`).
2. Select **3D Rotation Sheet**.
3. Set:
   - **Rotation Angles**: `16` (gives 22.5° increments — good balance of quality vs file size)
   - **Render Size**: `64` (2× your 32px canvas for crisp output)
   - **Transparent BG**: ✅
4. Click **OK** and choose a save location.

**Result**: A single PNG with 16 pre-rendered views of your stacked model, ready to load as a sprite sheet in any game engine.

```
  0°    22.5°   45°   67.5°   90°   ... (16 columns)
┌──────┬──────┬──────┬──────┬──────┬─────┐
│      │      │      │      │      │     │  ← Row of rendered angles
└──────┴──────┴──────┴──────┴──────┴─────┘
```

### Export B: Animated GIF (for Sharing Online)

1. Go to **File → Export…** (`Ctrl+E`).
2. Select **Animated GIF**.
3. Set:
   - **Scale**: `4` (128px from your 32px canvas — sharp for web)
   - **Frame Delay**: `125` ms (= 8 FPS)
4. Click **OK** and save.

**Result**: A looping `.gif` file showing your chest-opening animation.

### Export C: 3D Rotation GIF (Rotating 3D View)

1. Select **3D Rotation GIF** in the Export dialog.
2. Set:
   - **Rotation Angles**: `36` (10° increments — smooth rotation)
   - **Render Size**: `96`
   - **Frame Delay**: `50` ms (20 FPS)
3. Click **OK** and save.

**Result**: A looping GIF of the 3D model spinning 360°.

### Export D: Layer Strip (for Runtime Stacking)

Some game engines perform sprite stacking at runtime. They need a strip image.

1. Select **Layer Stack Strip** in the Export dialog.
2. Set **Scale**: `1` (keep native resolution).
3. Click **OK** and save.

**Result**: A single horizontal image with all layers side-by-side:

```
┌────────┬────────┬────────┬────────┬────────┬────────┐
│ Layer1 │ Layer2 │ Layer3 │ Layer4 │ Layer5 │ Layer6 │
└────────┴────────┴────────┴────────┴────────┴────────┘
```

### Export E: Individual Frames / Sprite Sheet

For traditional 2D animation:

- **Current Frame (PNG)** — exports only the current frame as a flattened PNG.
- **Sprite Sheet (Horizontal)** — all frames in a row.
- **Sprite Sheet (Grid)** — all frames in rows × columns grid layout.

---

## Summary — Full Workflow at a Glance

```
1.  File → New (32×32, layers)
          │
2.  Draw base sprite on Layer 1
          │
3.  Add layers → draw height slices
          │
4.  Check 3D Preview → adjust layer spacing
          │
5.  Duplicate frames → edit each for animation
          │
6.  Play animation → tweak timing
          │
7.  3D Preview → fine-tune render settings
          │
8.  Export → Rotation Sheet / GIF / APNG / Sprite Sheet
          │
9.  Save Project (.sss) for future editing
```

---

## What's Next?

- Try importing existing sprite sheets (**File → Import…**) to convert 2D art into stacked 3D.
- Experiment with **Voxel** render mode for a different aesthetic.
- Create walk-cycle animations by stacking character slices across frames.
- Use **Mirror X** for symmetric character designs.
- Export at different rotation counts (8, 16, 24, 36) and compare quality vs performance.
