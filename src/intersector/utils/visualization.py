"""Visualization utilities for 3D geometry using pythonocc.

This module provides helper functions to visualize one or more
OpenCascade (OCC) shapes in an interactive 3D window.
"""

import logging

from OCC.Display.SimpleGui import init_display

log = logging.getLogger("__name__")


def show_shape(shape) -> None:
    """Display a single OpenCascade shape in a 3D viewer.

    Args:
        shape (TopoDS_Shape): The shape object to be visualized.

    """
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(shape, update=True)
    display.View.SetProj(1, 1, 1)
    start_display()


def show_shapes(shapes) -> bool:
    """Display multiple OpenCascade shapes in a single 3D viewer.

    Args:
        shapes (TopoDS_Shape): A sequence of OCC shape objects to display.

    Returns:
        bool: True if visualization started successfully, False otherwise.

    """
    try:
        display, start_display, add_menu, add_function_to_menu = init_display()

        for shape in shapes:
            display.DisplayShape(shape, update=False)

        display.FitAll()
        start_display()
        return True
    except (RuntimeError, TypeError) as e:
        log.error(f"[bold red]💥 Error visualizing the shapes:[/bold red] {e}")
        return False
