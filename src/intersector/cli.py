# Copyright (c) 2025 Yannis Arapakis
# Licensed under the MIT License. See LICENSE file for details.
"""Command-line interface for simple OpenCascade CAD operations."""

import click
from rich.console import Console

from intersector.operations.intersect import intersect_with_plane, is_intersection_valid
from intersector.utils.file_handler import export_step, read_step
from intersector.utils.logger import setup_logging
from intersector.utils.parsing import parse_plane_input
from intersector.utils.visualization import show_shapes

console = Console()


@click.group()
@click.option("--verbose", is_flag=True, help="Enable verbose logging.")
@click.pass_context
def intersector(ctx, verbose):
    """Define the main CAD command group."""
    ctx.ensure_object(dict)
    ctx.obj["log"] = setup_logging(verbose)


@intersector.command()
@click.option(
    "--in-step",
    type=click.Path(exists=True),
    required=True,
    help="Path to the input STEP file.",
)
@click.option(
    "--in-plane",
    required=True,
    help="Plane definition in point-normal form 'x,y,z:nx,ny,nz'.",
)
@click.pass_context
def intersect(ctx, in_step: str, in_plane: str):
    """Compute the intersection between a 3D shape and a plane.

    This command loads a 3D model from a STEP file and computes its intersection
    with a user-defined plane. The plane is defined using a point and a normal
    vector in the form `'x,y,z:nx,ny,nz'`. The resulting intersection is exported
    to a new file called `intersection.stp` and optionally visualized.

    Example:
        intersector intersect --in-step box.step --in-plane "0,0,0:0,0,1"

    Args:
        ctx (click.Context): Click context object containing configuration.
        in_step (str): Path to the input STEP file.
        in_plane (str): Plane definition in `'x,y,z:nx,ny,nz'` format.

    Raises:
        click.ClickException: If the input plane format is invalid.
        click.ClickException: If the STEP file cannot be read.
        click.ClickException: If the intersection computation fails.
        click.ClickException: If exporting the result to a STEP file fails.
        click.ClickException: If visualization of shapes fails.

    """
    output_step = "intersection.stp"

    # ---- STEP file reading ----
    shape = read_step(in_step)
    if shape is None:
        raise click.ClickException(f"Failed to read STEP file: '{in_step}'")

    console.print("✅  [green]Input file successfully loaded![/green]")

    # ---- Plane parsing ----
    try:
        point, normal = parse_plane_input(in_plane)
    except ValueError as e:
        raise click.ClickException(f"Invalid plane definition: {e}") from None

    # ---- Intersection operation ----
    try:
        result = intersect_with_plane(shape, point, normal)
    except ValueError as e:
        raise click.ClickException(f"Invalid input to intersection: {e}") from None
    except RuntimeError as e:
        raise click.ClickException(f"Intersection computation failed: {e}") from None

    # ---- Validate intersection ----
    if is_intersection_valid(result):
        # ---- Export result ----
        if not export_step(result, output_step):
            raise click.ClickException(
                "Failed to export intersection result."
            ) from None

        console.print(
            "✅ [green]Intersection computed successfully. [/green]"
            f"[green]Result saved to '{output_step}'.[/green]"
        )

        # ---- Visualization (optional) ----
        if not show_shapes([shape, result]):
            raise click.ClickException("Error displaying shapes")
    else:
        console.print(
            "✅ [red]❌ No intersection between the input shape "
            "and the given plane.[/red]"
        )


def main():
    """Entry point for the CLI tool."""
    intersector()


if __name__ == "__main__":
    main()
