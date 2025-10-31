"""Utility functions for parsing user input strings into structured data.

This module provides helpers for safely converting command-line arguments
(such as plane definitions) into numerical representations that can be used
in geometric operations.
"""

import logging
from typing import Tuple

log = logging.getLogger(__name__)


def parse_plane_input(
    plane_str: str,
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """Parse a plane definition string into numeric point and normal tuples.

    The expected format is ``"x,y,z:nx,ny,nz"`` where:
        * ``x,y,z`` are the coordinates of a point on the plane.
        * ``nx,ny,nz`` are the components of the plane’s normal vector.

    Example:
    >>> parse_plane_input("0,0,100:0,0,1")
    ((0.0, 0.0, 100.0), (0.0, 0.0, 1.0))

    Args:
        plane_str (str): Plane definition in the format ``"x,y,z:nx,ny,nz"``.

    Raises:
        ValueError: If the input string cannot be parsed or does not contain
            exactly three numeric values for both the point and the normal.

    Returns:
        Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
            A pair of 3-tuples: (point, normal).

    """
    EXPECTED_VECTOR_LEN = 3
    try:
        point_str, normal_str = plane_str.split(":")
        point = tuple(float(v) for v in point_str.split(","))
        normal = tuple(float(v) for v in normal_str.split(","))

        if len(point) != EXPECTED_VECTOR_LEN or len(normal) != EXPECTED_VECTOR_LEN:
            raise ValueError()

    except (ValueError, AttributeError) as exc:
        log.error("❌ Invalid plane input '%s': %s", plane_str, exc)
        raise ValueError(
            "Plane format must be 'x,y,z:nx,ny,nz' (e.g., 0,0,100:0,0,1)"
        ) from exc

    return point, normal
