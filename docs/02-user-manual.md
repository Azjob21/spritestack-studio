# SpriteStack Studio — User Manual

Complete reference for every feature in the application.

---

## Table of Contents

- [Interface Overview](#interface-overview)
- [Canvas & Drawing](#canvas--drawing)
- [Tools Panel](#tools-panel)
- [Layers Panel](#layers-panel)
- [Color & Palette](#color--palette)
- [Animation Timeline](#animation-timeline)
- [3D Preview](#3d-preview)
- [Menus Reference](#menus-reference)
- [Import & Export](#import--export)
- [Project Files](#project-files)
- [Tips & Best Practices](#tips--best-practices)

---

## Interface Overview

The main window is divided into four regions connected by splitters you can resize:

| Region       | Location      | Contents                                               |
| ------------ | ------------- | ------------------------------------------------------ |
| **Tools**    | Left          | Tool buttons, brush size, mirror toggles, view options |
| **Canvas**   | Center        | The pixel art editing area — zoom, pan, draw           |
| **Panels**   | Right         | Tabbed: _Layers & Color_ / _3D Preview_                |
| **Timeline** | Bottom-center | Animation frame strip, playback controls, FPS          |

The **Status Bar** at the very bottom shows:

- Mouse position (X, Y) on the canvas
- Canvas dimensions (W × H)
- Current frame / total frames
- Current zoom percentage

---

## Canvas & Drawing

### Navigation

| Action             | Input                                    |
| ------------------ | ---------------------------------------- |
| Zoom in/out        | `Ctrl+Mouse Wheel`, or `Ctrl+=`/`Ctrl+-` |
| Fit canvas to view | `Ctrl+0`                                 |
| Pan                | `Space + drag`, or `Middle-mouse drag`   |

### Grid

Toggle the pixel grid via the **Grid** checkbox in the Tools panel, or **View → Grid**.  
The grid appears automatically at higher zoom levels and shows individual pixel boundaries.

### Drawing

- Click and drag to paint with the currently active tool.
- The canvas stores separate RGBA image data per **layer** per **frame**.
- Drawing only affects the currently selected layer and frame.

### Undo / Redo

- **Ctrl+Z** — Undo (up to 100 steps)
- **Ctrl+Y** — Redo

### Onion Skinning

Enable **Onion Skin** from the toolbar checkbox or the timeline.  
When active, the previous frame is drawn as a semi-transparent overlay beneath the current frame, helping you align animation frames.

---

## Tools Panel

Located on the left side. Each tool can be activated by clicking its button or pressing the associated key.

| Tool               | Shortcut | Description                                                               |
| ------------------ | -------- | ------------------------------------------------------------------------- |
| **Pencil**         | `B`      | Freehand pixel drawing. Respects brush size.                              |
| **Eraser**         | `E`      | Paints with full transparency (erases pixels).                            |
| **Fill (Bucket)**  | `G`      | Flood-fills a contiguous region of the same color with the current color. |
| **Eyedropper**     | `I`      | Click a pixel to pick its color as the current drawing color.             |
| **Line**           | `L`      | Click and drag to draw a straight line.                                   |
| **Rectangle**      | `R`      | Draw a rectangle outline.                                                 |
| **Rectangle Fill** | —        | Draw a filled rectangle.                                                  |
| **Circle**         | `C`      | Draw an ellipse outline.                                                  |
| **Circle Fill**    | —        | Draw a filled ellipse.                                                    |
| **Select**         | `S`      | Draw a selection rectangle on the canvas.                                 |

### Brush Size

Adjust the brush size (1–64 px) using the slider or spin box below the tool buttons.  
Larger brushes paint a square stamp of the specified width.

### Mirror / Symmetry

- **Mirror X** — Horizontally mirrors every stroke across the canvas center.
- **Mirror Y** — Vertically mirrors every stroke across the canvas center.
- Both can be enabled simultaneously for quad-symmetry.

---

## Layers Panel

Located in the right panel under the **Layers & Color** tab.

### Concepts

- Each _frame_ has its own independent set of layers.
- Layer **1** (bottom of the list) is the lowest slice; the topmost layer is the highest slice.
- In **sprite stacking**, each layer represents a horizontal cross-section at a different height.

### Controls

| Button                    | Action                                            |
| ------------------------- | ------------------------------------------------- |
| **+** (Add)               | Creates a new empty layer at the top              |
| **−** (Remove)            | Deletes the selected layer                        |
| **↑** (Up) / **↓** (Down) | Moves the selected layer in the stack order       |
| **⊕** (Duplicate)         | Copies the selected layer                         |
| **⤓** (Merge)             | Merges the selected layer down onto the one below |
| **≡** (Flatten)           | Flattens all layers into one                      |

### Opacity

Use the **Opacity** slider (0–100%) to control the visibility of the selected layer.  
This affects both canvas rendering and the 3D preview.

### Visibility

Click the **eye** icon next to a layer name to show/hide it. Hidden layers are excluded from the 3D preview and exports.

### Renaming

Right-click a layer → **Rename** to give it a descriptive name.

---

## Color & Palette

Located in the right panel under the **Layers & Color** tab, below the layer list.

### Color Picker

- **HSV Wheel / Square**: Click the hue-saturation square to pick hue and saturation; use the vertical slider for value (brightness).
- **Alpha Slider**: Below the HS square — controls transparency of your drawing color.
- **Hex Input**: Type a hex code directly (e.g., `#FF6600`).
- **RGB Spinboxes**: Fine-tune Red, Green, Blue channels numerically.

### Primary / Secondary Colors

Two swatches show your **primary** (foreground) and **secondary** (background) colors.  
Click **Swap** (or the swap button) to exchange them.

### Palette Swatches

A grid of saved colors. Click any swatch to set it as the current color.  
Click **Add to Palette** to save the current color to the palette.

### Preset Palettes

Three built-in palettes accessible via a dropdown:

| Palette        | Colors | Style                                   |
| -------------- | ------ | --------------------------------------- |
| **DB32**       | 32     | DawnBringer's classic pixel art palette |
| **PICO-8**     | 16     | Retro fantasy console palette           |
| **Endesga 32** | 32     | Modern vibrant pixel art palette        |

### Save / Load Palette

- **Save Palette** — exports the current swatches as `.json` or `.gpl` (GIMP Palette).
- **Load Palette** — imports a `.json` or `.gpl` palette file.

---

## Animation Timeline

Located at the bottom of the canvas area.

### Frame Strip

Shows thumbnail previews of each frame. Click a thumbnail to navigate to that frame.  
The currently active frame has a highlighted border.

### Playback Controls

| Button    | Action                    |
| --------- | ------------------------- |
| **⏮**    | Jump to first frame       |
| **⏪**    | Previous frame            |
| **▶ / ⏸** | Play / Pause animation    |
| **⏹**     | Stop (returns to frame 1) |
| **⏩**    | Next frame                |
| **⏭**    | Jump to last frame        |

### Frame Management

| Button    | Action                                              |
| --------- | --------------------------------------------------- |
| **+ Add** | Adds a new blank frame after the current one        |
| **⊕ Dup** | Duplicates the current frame (including all layers) |
| **− Del** | Deletes the current frame                           |

### FPS

Spin box (1–60) controls the playback speed. Default: **12 FPS**.

### Onion Skin

Checkbox enables onion skinning (ghost of previous frame visible while drawing).

---

## 3D Preview

Located in the right panel under the **3D Preview** tab.

### What It Shows

The 3D preview takes all layers of the current frame and renders them as a stacked 3D object. Each layer image is drawn at a different vertical offset, producing the "sprite stacking" effect.

### Navigation

| Action | Input                        |
| ------ | ---------------------------- |
| Rotate | Left-mouse drag horizontally |
| Tilt   | Left-mouse drag vertically   |
| Zoom   | Mouse scroll wheel           |
| Pan    | Middle-mouse drag            |

### Render Modes

| Mode          | Description                                                                                                          |
| ------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Stack**     | Classic sprite stacking — layers are rotated and offset. The default mode for game-ready sprite stacking.            |
| **Voxel**     | Isometric voxel rendering — each opaque pixel is drawn as a small cube. Shows the 3D form in a Minecraft-like style. |
| **Billboard** | Simple vertical spread — layers fanned out vertically with no rotation, useful as a quick depth check.               |

### Controls

- **Layer Spacing** (0.5–10.0): Controls the gap between each rendered layer slice.
- **Mode** dropdown: Switch between Stack / Voxel / Billboard.
- **Auto Rotate**: Spins the model continuously.
- **Rotation Speed** (1–100): Speed of the auto-rotation.
- **Outlines**: Draws dark edges around each layer slice for definition.
- **Shadows**: Renders a shadow beneath each layer.

### Auto-Refresh

The 3D preview automatically updates every 500ms to reflect canvas edits.

---

## Menus Reference

### File

| Item             | Shortcut       | Description                                             |
| ---------------- | -------------- | ------------------------------------------------------- |
| New…             | `Ctrl+N`       | Create a new canvas with specified size and layer count |
| Open Project…    | `Ctrl+O`       | Load a `.sss` project file                              |
| Save Project     | `Ctrl+S`       | Save current work to `.sss` file                        |
| Save Project As… | `Ctrl+Shift+S` | Save to a new `.sss` file                               |
| Import…          | —              | Import images (as layers, frames, or stacks)            |
| Export…          | `Ctrl+E`       | Export to PNG, GIF, sprite sheets, etc.                 |
| Exit             | `Ctrl+Q`       | Quit the application (prompts if unsaved changes)       |

### Edit

| Item           | Shortcut | Description                                     |
| -------------- | -------- | ----------------------------------------------- |
| Undo           | `Ctrl+Z` | Undo last canvas operation                      |
| Redo           | `Ctrl+Y` | Redo last undone operation                      |
| Clear Layer    | —        | Erase all pixels on the current layer           |
| Fill Layer     | —        | Fill entire current layer with the active color |
| Resize Canvas… | —        | Change canvas dimensions (with anchor position) |

### View

| Item          | Shortcut | Description                     |
| ------------- | -------- | ------------------------------- |
| Zoom In       | `Ctrl+=` | Increase zoom                   |
| Zoom Out      | `Ctrl+-` | Decrease zoom                   |
| Fit to Window | `Ctrl+0` | Auto-zoom to fit canvas in view |
| Toggle Grid   | —        | Show/hide pixel grid            |

### Layer

| Item            | Description                             |
| --------------- | --------------------------------------- |
| Add Layer       | Create a new empty layer                |
| Remove Layer    | Delete the selected layer               |
| Duplicate Layer | Copy the selected layer                 |
| Merge Down      | Merge selected layer into the one below |
| Flatten All     | Combine all layers into one             |

### Animation

| Item           | Shortcut | Description                |
| -------------- | -------- | -------------------------- |
| Play/Pause     | `F5`     | Toggle animation playback  |
| Stop           | `F6`     | Stop and rewind to frame 1 |
| Next Frame     | `F7`     | Advance to next frame      |
| Previous Frame | `F8`     | Go back one frame          |
| Add Frame      | —        | Add a new blank frame      |
| Delete Frame   | —        | Remove the current frame   |

### Stack

| Item                           | Description                                              |
| ------------------------------ | -------------------------------------------------------- |
| Auto-Generate Layers from Base | Creates progressively inset layers from Layer 1          |
| Import Layer Strip…            | Loads a horizontal strip image and splits it into layers |
| Export Rotation Sheet…         | Quick-export a multi-angle sprite sheet                  |
| Export Layer Strip…            | Quick-export a horizontal layer strip                    |

### Help

| Item  | Description              |
| ----- | ------------------------ |
| About | Version info and credits |

---

## Import & Export

### Import Dialog

Accessed via **File → Import…**

| Import Type                   | Description                                   |
| ----------------------------- | --------------------------------------------- |
| Single Image as Layer         | Adds a PNG/BMP/JPG as a new layer             |
| Sprite Sheet → Frames         | Splits a sheet into animation frames          |
| Sprite Sheet → Layers (Stack) | Splits a sheet into layers for stacking       |
| Folder → Layers (Stack)       | Loads numbered images from a folder as layers |
| Folder → Animation Frames     | Loads numbered images from a folder as frames |

### Export Dialog

Accessed via **File → Export…** (`Ctrl+E`)

| Export Type               | Description                                   |
| ------------------------- | --------------------------------------------- |
| Current Frame (PNG)       | Flattened image of the current frame          |
| All Layers (PNGs)         | Each layer saved as a separate PNG file       |
| Sprite Sheet (Horizontal) | All frames side by side in one image          |
| Sprite Sheet (Grid)       | Frames arranged in rows and columns           |
| Animated GIF              | Looping GIF of all frames                     |
| Animated PNG (APNG)       | Higher quality animated PNG                   |
| 3D Rotation Sheet         | Sprite sheet of the stacked model at N angles |
| 3D Rotation GIF           | Animated GIF of the model rotating 360°       |
| Layer Stack Strip         | Horizontal strip of all layers in one image   |

### Export Options

- **Scale**: 1×–16× — upscale the output for higher resolution.
- **Columns**: For grid-layout sprite sheets — how many frames per row.
- **Rotation Angles**: For rotation exports — how many angles (4–72) around 360°.
- **Render Size**: Size of each rotation render in pixels.
- **Frame Delay**: Milliseconds between GIF frames.
- **Transparent BG**: Keep the background transparent (otherwise white).

---

## Project Files

Projects are saved as `.sss` files (SpriteStack Studio format).

### What's Inside

A `.sss` file is a standard **ZIP archive** containing:

```
project.json           ← metadata (canvas size, frame count, layer info)
layers/
  frame_0000_layer_0000.png
  frame_0000_layer_0001.png
  frame_0001_layer_0000.png
  ...
```

### Metadata (project.json)

```json
{
  "version": "1.0",
  "width": 32,
  "height": 32,
  "frames": [
    {
      "layers": [
        { "name": "Layer 1", "opacity": 1.0, "visible": true },
        { "name": "Layer 2", "opacity": 1.0, "visible": true }
      ]
    }
  ]
}
```

### Compatibility

Since `.sss` is a ZIP, you can rename it to `.zip` and extract images manually in any tool.

---

## Tips & Best Practices

### For Sprite Stacking

1. **Start from the bottom** — Layer 1 is the ground-level footprint. Draw the widest outline here.
2. **Progress upward** — Each successive layer should be the shape at that height. For a tree: trunk base → trunk → canopy bottom → canopy → top.
3. **Keep it simple** — Sprite stacking works best at small resolutions (16×16 to 64×64).
4. **Use the Auto-Generate feature** for quick prototyping — it creates inset layers from your base automatically.
5. **Preview often** — keep the 3D tab visible while drawing to see the result in real-time.

### For Animation

1. **Use Onion Skin** to maintain consistency between frames.
2. **Duplicate frames** to make incremental changes instead of drawing each from scratch.
3. **Set FPS first** — decide on your target framerate before animating so timing feels right.

### For Pixel Art

1. **Lock to small brush sizes** (1–3 px) for detailed work.
2. **Use the Eyedropper** (`I`) constantly — pick colors from existing pixels to stay consistent.
3. **Use Mirror X** for characters and symmetric objects.
4. **Zoom in** for detail work, **zoom out** to check overall silhouette.

### For Export

1. **Rotation sheets** of 8 or 16 angles cover most game engine needs.
2. **Test your GIF at the intended framerate** using the timeline before exporting.
3. **Use 2× or 4× scale** when exporting for web or higher-res displays.
