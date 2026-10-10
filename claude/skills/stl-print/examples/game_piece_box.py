"""Example: 24 game pieces (D20 x 35) in a 4x6 tray with a friction-fit hood lid.
Run: ~/.claude/skills/stl-print/run.sh game_piece_box.py -> box.stl, lid.stl, preview_*.png
"""
from manifold3d import Manifold

from stlkit import assert_clear, grid, hole, on_bed, preview, rrect, slab, union, write_stl

# --- parameters (mm) ---
POCKET_D, POCKET_DEPTH, CHAMFER = 21.0, 15.0, 0.5
PITCH, COLS, ROWS = 23.0, 4, 6
FLOOR, WALL, CORNER_R = 2.0, 3.5, 4.0
SEAM_Z = 11.0                    # tray/hood seam; lip runs from here to tray top (17)
HOOD_WALL, HOOD_TOP, GAP = 1.7, 2.0, 0.2
PIECE_D, PIECE_H, HEADROOM = 20.0, 35.0, 1.0
NOTCH_R, NOTCH_H = 8.0, 6.0

W = COLS * PITCH - (PITCH - POCKET_D) + 2 * WALL     # 97
L = ROWS * PITCH - (PITCH - POCKET_D) + 2 * WALL     # 143
TRAY_H = FLOOR + POCKET_DEPTH                         # 17
TOTAL_H = FLOOR + PIECE_H + HEADROOM + HOOD_TOP       # 40
CENTERS = grid(COLS, ROWS, PITCH, WALL + POCKET_D / 2, WALL + POCKET_D / 2)

lip = HOOD_WALL + GAP
box = slab(rrect(W, L, CORNER_R), 0, SEAM_Z) + slab(rrect(W, L, CORNER_R, lip), SEAM_Z, TRAY_H)
box -= union(hole(POCKET_D, FLOOR, TRAY_H, CHAMFER).translate((x, y, 0)) for x, y in CENTERS)

lid = slab(rrect(W, L, CORNER_R), SEAM_Z, TOTAL_H) - slab(rrect(W, L, CORNER_R, HOOD_WALL), SEAM_Z - 1, TOTAL_H - HOOD_TOP)
# finger notches: arc cut into the bottom edge of both long sides
lid -= Manifold.cylinder(W + 2, NOTCH_R).rotate((0, 90, 0)).translate((-1, L / 2, SEAM_Z + NOTCH_H - NOTCH_R))

# self-check: contents fit, closed lid clears everything
pieces = union(Manifold.cylinder(PIECE_H, PIECE_D / 2).translate((x, y, FLOOR)) for x, y in CENTERS)
assert_clear(pieces, box, "piece vs tray")
assert_clear(pieces, lid, "piece vs lid")
assert_clear(box, lid, "lid vs tray")
assert len(CENTERS) == 24 and (W, L, TOTAL_H) == (97, 143, 40), (W, L, TOTAL_H)

write_stl(box, "box.stl")
write_stl(on_bed(lid, flip=True), "lid.stl")
preview(box + lid.translate((W + 15, 0, 0)), "preview_parts.png")
print(f"box {W}x{L}x{TRAY_H} {box.volume()/1000:.1f} cm3 | lid {W}x{L}x{TOTAL_H-SEAM_Z} {lid.volume()/1000:.1f} cm3 | OK")
