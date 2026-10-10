---
name: stl-print
description: Design parametric 3D-printable parts (boxes, organizers, inserts, lids, holders, brackets) and export STL files. Use when the user wants an STL, something to 3D print, a box/case/insert/holder for physical objects, or asks to model a part in 3D. Optionally adds a dimensioned 2D drawing via the CADCraft MCP.
---

# STL print

Build printable parts as a Python script on manifold3d (exact booleans, always-manifold meshes),
with fit checks as asserts. Units mm, z up, bed at z=0.

## Tools in this skill

- `~/.claude/skills/stl-print/run.sh model.py`: runs a model script with `stlkit` importable. It creates
  `.venv` (manifold3d, numpy, matplotlib) on first use. Outputs land in the current directory.
- `stlkit.py`: `rrect`, `slab`, `union`, `grid`, `hole`, `assert_clear`, `on_bed`, `write_stl`, `preview`.
  Read it once before writing a model; it's short.
- `examples/game_piece_box.py`: a full worked example (pocket tray plus a friction-fit hood lid with
  finger notches). Copy its structure.

Facts that save time:
- CADCraft MCP is **2D only**: no extrude, no solids, no STL. Use it only for the reference drawing.
- The OpenSCAD Homebrew cask was disabled (Gatekeeper, Sep 2026). Don't try it; manifold3d replaces it.
- Bambu Studio and Orca are installed: `open -a BambuStudio part.stl` for the user to inspect and slice.

## Workflow

1. **Pin down requirements.** Ask with AskUserQuestion, and give a recommended option each time.
   Ask only what the request leaves open:
   - the objects to hold: exact dimensions and count (ask the user to measure the widest point with calipers)
   - orientation and layout (grid shape, grouping)
   - clearances (see the table below)
   - closure type, wall/floor thickness, print bed size
   - finishing: chamfers, corner radii, finger notches, labels
2. **Write `model.py` in the user's project folder.**
   - All dimensions go in named constants at the top, and derived sizes are computed (never hand-typed) with a comment.
   - Model each part in assembly coordinates, so fit checks are meaningful.
   - Model the contents (pieces, cards, tools) as simple solids, and `assert_clear` them against every part.
     Also check the lid against the box when closed.
   - Assert the agreed outer dimensions and the item count.
   - Export with `on_bed(part, flip=...)` in the orientation that prints without supports.
3. **Run it:** `~/.claude/skills/stl-print/run.sh model.py`. The asserts must pass.
4. **Look at it.** Call `preview(part, "preview.png")` and Read the PNG. Fix anything that looks wrong.
5. **Optional 2D drawing in CADCraft** (if the user wants one): a top view and a section, with dimensions, saved as DXF/PDF/PNG.
6. **Report** the files, sizes and volumes, any deviations from what was agreed (with the reason), and
   which constants to tweak after a test print. Recommend printing a small fit-test slice first.

## Printability rules (FDM, 0.4mm nozzle)

| Thing | Value |
|---|---|
| Hole for an object to drop in | +0.5mm per side (snug +0.25, loose +1.0) |
| Friction-fit lid/lip gap | 0.2mm per side (loose 0.3) |
| Sliding fit | 0.3–0.4mm per side |
| Min wall | 1.2mm; 1.6–2mm sturdy |
| Floor/top | ≥ 1.6mm (2mm default) |
| Overhangs | ≤ 45°, otherwise flip the part or chamfer |
| Chamfer on adjacent pockets | ≤ (rib thickness / 2) − 0.5, otherwise the rib becomes a knife edge |

- Inner corner radius of a nested part = outer radius − wall thickness (`rrect(..., inset=...)` does this).
- Cut tools must overshoot the face they cut through (≥ 1mm) to avoid zero-thickness skins.
- Hood lids print top-down (`on_bed(lid, flip=True)`); trays print floor-down.

## CADCraft drawing tips

- Start with `new_drawing {metric: true}`, then use `layer.new {name, color, current: true}` per part (Tray, Lid, Contents, Dims).
- Use `script` for geometry without spaces in its arguments: `rectang f 4 0,0 97,143` (filleted rectangle), `circle x,y r`, `pline ... c`.
- Add text with `execute text {at, height, text}`. In `script`, spaces act as Enter and break text.
- Dimensions: `dimlinear {p1, p2, at}` and `dimdiameter {center, point}` (put `point` exactly on the circle).
- Before `erase {handles}`, confirm the handles with `query_entities`; handle numbers are easy to get off by one.
- Finish with `zoom {mode: "extents"}`, `save` (.dxf), `exportpdf {path, paper: "A4", landscape: true, fit: true}` and `render` (PNG) to check it.
