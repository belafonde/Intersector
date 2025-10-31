"""Utilities for reading and writing CAD files.

This module handles file input and output for the Intersector application,
including loading STEP files into shapes and exporting shapes into STEP files.
"""

import logging
import os

from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.STEPControl import (
    STEPControl_AsIs,
    STEPControl_Reader,
    STEPControl_Writer,
)
from OCC.Core.TopoDS import TopoDS_Shape

log = logging.getLogger(__name__)


def export_step(shape: TopoDS_Shape, filename: str = "output.step") -> bool:
    """Export a TopoDS_Shape to a STEP file.

    Args:
        shape (TopoDS_Shape): The OpenCascade TopoDS_Shape to export.
        filename (str): Output filename (default is 'shape.step').

    Returns:
        bool: True if the export succeeded, False otherwise.

    """
    try:
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        status = writer.Write(filename)

        if status == IFSelect_RetDone:
            log.info(
                "[green]✅ A Shape successfully exported to [/green]"
                f"[green][bold]{filename}[/bold][/green]"
            )
            return True
        else:
            log.error(f"[red]❌ STEP export failed with status: {status}[/red]")
            return False

    except (OSError, RuntimeError) as e:
        log.error(f"[bold red]💥 Error exporting STEP file:[/bold red] {e}")
        return False


def read_step(filename: str) -> TopoDS_Shape | None:
    """Read a STEP file and return the corresponding TopoDS_Shape.

    Returns:
        TopoDS_Shape | None: The shape if successfully read, None otherwise.

    """
    if not os.path.exists(filename):
        log.error(f"[red]❌ File not found:[/red] {filename}")
        return None

    try:
        log.info(f"[cyan]📂 Reading STEP file:[/cyan] {filename}")
        reader = STEPControl_Reader()
        status = reader.ReadFile(filename)

        if status != IFSelect_RetDone:
            log.error(f"[red]❌ Failed to read STEP file. Status: {status}[/red]")
            return None

        reader.TransferRoots()
        shape = reader.OneShape()

        if shape.IsNull():
            log.error("[red]❌ No shape data found in the STEP file.[/red]")
            return None

        log.info("[green]✅ STEP file successfully loaded![/green]")
        return shape

    except (FileNotFoundError, RuntimeError) as e:
        log.error(f"[bold red]💥 Error reading STEP file:[/bold red] {e}")
        return None
