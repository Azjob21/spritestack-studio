# Sprint Status & Remaining Scope

This document estimates project progress **as if development is organized in sprints**.

## Current Sprint (Now)

**We are in Sprint 4: Multi-object Sandbox + Multi-scene Integration (stabilization phase).**

Why Sprint 4:
- Core editor is already mature (tools, layers, timeline, palettes, export pipeline).
- 3D stack preview and advanced exports exist.
- Scene architecture exists (`SceneManager`, `Scene`, `ObjectPlacement`) and is wired in main UI.
- Remaining work is no longer “build core features”, but **stabilize scene workflows and close integration gaps**.

## What Is Already Implemented

1. Pixel-art editor fundamentals (drawing tools, layers, animation timeline, color tools, undo/redo).
2. Sprite-stack rendering and preview workflows.
3. Broad export/import capabilities.
4. Project persistence with scene-aware metadata.
5. Workspace model split (Create / Sandbox / Animate / Texture).
6. Scene/object data model with placement transforms (visibility, offsets, scale, rotation, opacity).

## What Is Left to Implement

## A) Sprint 4 completion (must-fix before AI)

1. **Scene workflow consistency**
   - Remove remaining mismatches between scene UI handlers and scene model APIs.
   - Ensure object add/rename/remove/type-convert flows are fully consistent across Create/Sandbox/Preview.

2. **Ensemble/Sandbox reliability**
   - Fix known “ensemble view not working properly” behavior.
   - Guarantee hierarchy visibility toggles and active-object switching always reflect true scene state.

3. **Project integrity**
   - Validate save/load with multiple scenes and multiple objects per scene.
   - Confirm scene switch keeps transforms and active object selection coherent.

## B) New scope: AI control by text/voice

### Sprint 5 — Text Command MVP
1. Add command input panel (prompt box + execution log + undo hint).
2. Implement command interpreter for scene actions:
   - select object
   - move/rotate/scale object
   - toggle visibility
   - duplicate/delete object
   - switch scene / create scene
3. Add deterministic action layer mapping intents to existing editor operations.
4. Add confirmation/preview step for destructive commands.

### Sprint 6 — Voice Command MVP
1. Add microphone capture pipeline and speech-to-text integration.
2. Reuse text-command interpreter for voice transcripts.
3. Add confidence handling (low-confidence = ask confirmation).
4. Add push-to-talk and privacy controls (local vs cloud speech mode).

### Sprint 7 — AI Robustness & Production Readiness
1. Context-aware commands (e.g., “move it left”, “hide all textures in Scene 2”).
2. Command history, retry, and correction UX.
3. Safety guardrails (blocked unsafe operations, explicit confirmations).
4. Regression tests for scene/object command execution and undo/redo compatibility.
5. Performance tuning for real-time scene feedback during repeated commands.

## Recommended Definition of Done for AI Integration

1. Text commands can control objects across scenes with undo/redo safety.
2. Voice commands execute through the same action pipeline as text commands.
3. Command execution is visible, reversible, and reliable in multi-scene projects.
4. Failure states are explicit (no silent command drops).
