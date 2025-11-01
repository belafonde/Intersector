# Copyright (c) 2025 Yannis Arapakis
# Licensed under the MIT License. See LICENSE file for details.
"""Intersection operations between shapes and planes.

Provides functionality to compute intersections using OpenCascade.
Supports plane definitions via point-normal form.
"""

import logging

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
from OCC.Core.gp import gp_Dir, gp_Pln, gp_Pnt
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Extend.ShapeFactory import make_face

log = logging.getLogger("__name__")


def is_intersection_valid(intersection_shape: TopoDS_Shape) -> bool:
    """Return whether an intersection result contains valid geometry.

    Verify that the supplied intersection shape (typically the result of a
    `BRepAlgoAPI_Section` operation) includes at least one edge. An
    intersection with no edges is considered empty/invalid.

    Args:
        intersection_shape (TopoDS_Shape): The shape returned by a section or
            boolean operation to be inspected.

    Returns:
        bool: True if the intersection result contains at least one edge,
            False otherwise.

    """
    if intersection_shape is None:
        return False

    explorer = TopExp_Explorer(intersection_shape, TopAbs_EDGE)
    return explorer.More()


def intersect_with_plane(shape, plane_point, plane_normal):
    """Compute intersection between a TopoDS_Shape and a plane (point + normal).

    Creates a plane from the given point and normal vector, then performs a
    section operation between the input `TopoDS_Shape` and that plane using
    OpenCascade’s `BRepAlgoAPI_Section`. Returns the resulting intersection
    edges as a `TopoDS_Shape`.

    Args:
        shape (TopoDS_Shape): The input 3D solid or surface.
        plane_point (tuple[float, float, float]): A point on the plane.
        plane_normal (tuple[float, float, float]): The plane's normal vector.

    Raises:
        ValueError: shape is none.
        RuntimeError: If the intersection operation fails.

    Returns:
        TopoDS_Shape: The resulting intersection edges (TopoDS_Compound).

    """
    if shape is None:
        raise ValueError("Shape cannot be None")

    px, py, pz = plane_point
    nx, ny, nz = plane_normal

    point = gp_Pnt(px, py, pz)
    normal = gp_Dir(nx, ny, nz)
    plane = gp_Pln(point, normal)

    log.info(
        f"✂️  Intersecting shape with plane at ({px},{py},{pz}) normal ({nx},{ny},{nz})"
    )

    section = BRepAlgoAPI_Section(shape, make_face(plane))
    section.Build()

    if not section.IsDone():
        raise RuntimeError("Intersection operation failed: section not completed.")

    return section.Shape()
