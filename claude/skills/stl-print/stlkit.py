"""Tiny helpers for parametric, 3D-printable parts on top of manifold3d.

Units are mm, z up, the bed is z=0. Import in a model script and run it with run.sh.
"""
import struct

import numpy as np
from manifold3d import CrossSection, JoinType, Manifold, OpType, set_circular_segments

set_circular_segments(96)


def rrect(w, l, r, inset=0.0):
    """Rounded rectangle w x l (corner radius r), shrunk by `inset` on every side; origin at the corner."""
    w, l, r = w - 2 * inset, l - 2 * inset, max(r - inset, 0.01)
    return CrossSection.square((w - 2 * r, l - 2 * r)).translate((inset + r, inset + r)).offset(r, JoinType.Round)


def slab(cs, z0, z1):
    """Extrude a 2D cross-section from z0 to z1."""
    return Manifold.extrude(cs, z1 - z0).translate((0, 0, z0))


def union(parts):
    """Fast union of many solids (use for arrays of holes)."""
    return Manifold.batch_boolean(list(parts), OpType.Add)


def grid(nx, ny, pitch, x0=0.0, y0=0.0):
    """Centers of an nx x ny grid with equal pitch."""
    return [(x0 + i * pitch, y0 + j * pitch) for i in range(nx) for j in range(ny)]


def hole(d, z_bottom, z_top, chamfer=0.0):
    """Vertical round pocket at the origin, optional chamfer at the top edge. Overshoots the top by 1mm."""
    r = d / 2
    m = Manifold.cylinder(z_top - z_bottom + 1, r).translate((0, 0, z_bottom))
    if chamfer:
        m += Manifold.cylinder(chamfer + 0.01, r, r + chamfer + 0.01).translate((0, 0, z_top - chamfer))
    return m


def assert_clear(a, b, what):
    """Fail if two solids overlap (fit check: part vs. contents, lid vs. box)."""
    v = (a ^ b).volume()
    assert v < 1e-6, f"{what}: overlap {v:.3f} mm3"


def on_bed(m, flip=False):
    """Optionally flip upside down (e.g. a lid printed top-down), then drop onto z=0."""
    if flip:
        m = m.rotate((180, 0, 0))
    return m.translate((0, 0, -m.bounding_box()[2]))


def write_stl(m, path):
    """Binary STL."""
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]
    t = np.asarray(mesh.tri_verts)
    a, b, c = v[t[:, 0]], v[t[:, 1]], v[t[:, 2]]
    n = np.cross(b - a, c - a)
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    rec = np.zeros(len(t), dtype=[("n", "<f4", 3), ("a", "<f4", 3), ("b", "<f4", 3), ("c", "<f4", 3), ("x", "<u2")])
    rec["n"], rec["a"], rec["b"], rec["c"] = n, a, b, c
    with open(path, "wb") as f:
        f.write(b"\0" * 80 + struct.pack("<I", len(t)) + rec.tobytes())


def preview(m, path, elev=30, azim=-60):
    """Shaded PNG of a solid, so the agent can look at the result (Read the PNG).
    ponytail: matplotlib painter's sort shows depth artifacts; good for spotting gross mistakes,
    open the STL in Bambu Studio/Orca for a true view."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]
    tris = v[np.asarray(mesh.tri_verts)]
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    light = np.array([0.3, -0.5, 0.8]) / np.linalg.norm([0.3, -0.5, 0.8])
    shade = 0.35 + 0.65 * np.clip((n * light).sum(1), 0, 1)
    fig = plt.figure(figsize=(8, 6), dpi=120)
    ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(Poly3DCollection(tris, facecolors=np.c_[shade * 0.3, shade * 0.6, shade * 0.9], linewidths=0))
    lo, hi = v.min(0), v.max(0)
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
    ax.set_box_aspect(hi - lo)
    ax.view_init(elev, azim)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
