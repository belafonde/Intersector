# Copyright (c) 2025 Yannis Arapakis
# Licensed under the MIT License. See LICENSE file for details.
"""Geometric operations for CAD shapes.

This package provides modules for performing geometric operations
on CAD shapes, such as intersections.
"""

from .intersect import intersect_with_plane

__all__ = ["intersect_with_plane"]
