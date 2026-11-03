# Quick Start Guide

Get from zero to a finished, exported sprite stack in **5 minutes**.

---

## 1 — Launch the App

Double-click the **SpriteStack Studio** shortcut on your Desktop  
_(or run `python main.py` from the project folder)._

You'll see four main areas:

```
┌──────────┬──────────────────────────┬──────────────┐
│  TOOLS   │        CANVAS            │  LAYERS /    │
│  panel   │   (pixel art editor)     │  COLOR /     │
│          │                          │  3D PREVIEW  │
│          │                          │  (tabs)      │
├──────────┴──────────────────────────┴──────────────┤
│              ANIMATION TIMELINE                     │
└─────────────────────────────────────────────────────┘
```

---

## 2 — Create a New Canvas

1. Go to **File → New…** (or `Ctrl+N`).
2. Set the size — for sprite stacking, **32×32** or **64×64** is typical.
3. Set **Initial Layers** — this is the number of stacking slices. Start with **8**.
4. Click **OK**.

---

## 3 — Draw Something

1. Select **Layer 1** in the Layers panel (bottom-most slice of your stack).
2. Pick a color from the **Color** section (click the HSV square, or click a palette swatch).
3. Choose the **Pencil** tool (or press `B`).
4. Draw on the canvas — this is the _base footprint_ of your 3D object.
5. Switch to **Layer 2**, draw a slightly smaller or offset shape.
6. Repeat for each layer upward — each layer is a "height slice".

> **Tip:** Use **Stack → Auto-Generate Layers from Base** to let the app create shrinking layers automatically from your first drawing.

---

## 4 — Preview in 3D

1. Click the **3D Preview** tab on the right panel.
2. You'll see your layers stacked in 3D.
3. **Left-drag** to rotate, **scroll** to zoom, **middle-drag** to pan.
4. Adjust **Layer Spacing** slider to control the gap between slices.
5. Toggle **Auto Rotate** to spin the model automatically.

---

## 5 — Export

Go to **File → Export…** (`Ctrl+E`) and choose one of:

| Export Type         | Use Case                                                               |
| ------------------- | ---------------------------------------------------------------------- |
| Current Frame (PNG) | Simple flat sprite                                                     |
| 3D Rotation Sheet   | Sprite sheet with your stack rendered at N angles (for game engines)   |
| 3D Rotation GIF     | Animated preview to share online                                       |
| Animated GIF        | Frame-by-frame animation export                                        |
| Layer Strip         | Horizontal strip of all layers for engines that do stacking at runtime |

Set scale, angle count, etc., then click **OK** and choose a save location.

---

## That's It!

For the full feature reference, see the [User Manual](02-user-manual.md).  
For a detailed step-by-step walkthrough, see the [Workflow Tutorial](03-workflow-tutorial.md).
