"""Unit tests for the CLI intersect command."""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from intersector.cli import intersect


class TestCLIIntersect(TestCase):
    """Test suite for the `intersect` CLI command."""

    def setUp(self):
        """Set up the Click test runner."""
        self.runner = CliRunner()

    def test_intersect_successful(self):
        """Test a successful intersection between shape and plane."""
        with (
            patch("intersector.cli.read_step") as mock_read_step,
            patch("intersector.cli.parse_plane_input") as mock_parse_plane_input,
            patch("intersector.cli.intersect_with_plane") as mock_intersect_with_plane,
            patch("intersector.cli.is_intersection_valid") as mock_is_valid,
            patch("intersector.cli.export_step") as mock_export_step,
            patch("intersector.cli.show_shapes") as mock_show_shapes,
        ):
            mock_shape = MagicMock(name="TopoDS_Shape")
            mock_read_step.return_value = mock_shape
            mock_parse_plane_input.return_value = ((0, 0, 100), (0, 0, 1))
            mock_intersect_with_plane.return_value = mock_shape
            mock_is_valid.return_value = True

            with self.runner.isolated_filesystem():
                with open("dummy_shape.stp", "w", encoding="utf-8") as f:
                    f.write("FAKE STEP CONTENT")

                result = self.runner.invoke(
                    intersect,
                    ["--in-step", "dummy_shape.stp", "--in-plane", "0,0,100:0,0,1"],
                )

            assert result.exit_code == 0, result.output
            mock_export_step.assert_called_once()
            mock_show_shapes.assert_called_once()

    def test_intersect_file_not_found(self):
        """Test CLI behavior when STEP file cannot be read."""
        with patch("intersector.cli.read_step", return_value=None):
            with self.runner.isolated_filesystem():
                with open("missing_file.stp", "w", encoding="utf-8") as f:
                    f.write("FAKE")

                result = self.runner.invoke(
                    intersect,
                    ["--in-step", "dummy_shape.stp", "--in-plane", "0,0,100:0,0,1"],
                )

            assert result.exit_code != 0
            assert "Error" in result.output or "Invalid" in result.output

    def test_invalid_plane_definition(self):
        """Test CLI handling of invalid plane input."""
        with (
            patch("intersector.cli.read_step") as mock_read_step,
            patch("intersector.cli.parse_plane_input") as mock_parse_plane_input,
        ):
            mock_read_step.return_value = MagicMock(name="TopoDS_Shape")
            mock_parse_plane_input.side_effect = ValueError("Invalid format")

            with self.runner.isolated_filesystem():
                with open("dummy_shape.stp", "w", encoding="utf-8") as f:
                    f.write("FAKE")

                result = self.runner.invoke(
                    intersect,
                    ["--in-step", "dummy_shape.stp", "--in-plane", "0,0,100:0,0,1"],
                )

            assert result.exit_code != 0
            assert "Invalid plane definition" in result.output

    def test_intersect_value_error(self):
        """Test CLI when intersection raises a ValueError."""
        with (
            patch("intersector.cli.read_step") as mock_read,
            patch("intersector.cli.parse_plane_input") as mock_parse,
            patch("intersector.cli.intersect_with_plane") as mock_intersect,
        ):

            error_message = "Bad geometry"
            mock_shape = MagicMock(name="TopoDS_Shape")
            mock_read.return_value = mock_shape
            mock_parse.return_value = ((0, 0, 0), (0, 0, 1))
            mock_intersect.side_effect = ValueError(error_message)

            with self.runner.isolated_filesystem():
                with open("dummy_shape.stp", "w", encoding="utf-8") as f:
                    f.write("FAKE")

                result = self.runner.invoke(
                    intersect,
                    ["--in-step", "dummy_shape.stp", "--in-plane", "0,0,100:0,0,1"],
                )

            assert result.exit_code != 0
            assert error_message in result.output

    def test_intersection_failure(self):
        """Test CLI when intersection operation fails (raises RuntimeError)."""
        with (
            patch("intersector.cli.read_step") as mock_read_step,
            patch("intersector.cli.parse_plane_input") as mock_parse_plane_input,
            patch("intersector.cli.intersect_with_plane") as mock_intersect_with_plane,
        ):
            error_message = "Intersection operation failed"
            mock_shape = MagicMock(name="TopoDS_Shape")
            mock_read_step.return_value = mock_shape
            mock_parse_plane_input.return_value = ((0, 0, 0), (0, 0, 1))
            mock_intersect_with_plane.side_effect = RuntimeError(error_message)

            with self.runner.isolated_filesystem():
                with open("dummy_shape.stp", "w", encoding="utf-8") as f:
                    f.write("FAKE")

                result = self.runner.invoke(
                    intersect,
                    ["--in-step", "dummy_shape.stp", "--in-plane", "0,0,100:0,0,1"],
                )

            assert result.exit_code != 0
            assert error_message in result.output

    def test_intersect_invalid_result(self):
        """Test CLI when intersection result is invalid."""
        with (
            patch("intersector.cli.read_step") as mock_read,
            patch("intersector.cli.parse_plane_input") as mock_parse,
            patch("intersector.cli.intersect_with_plane") as mock_intersect,
            patch("intersector.cli.is_intersection_valid") as mock_valid,
        ):

            mock_shape = MagicMock(name="TopoDS_Shape")
            mock_read.return_value = mock_shape
            mock_parse.return_value = ((0, 0, 0), (0, 0, 1))
            mock_intersect.return_value = mock_shape
            mock_valid.return_value = False  # Simulate not intersection.

            with self.runner.isolated_filesystem():
                with open("dummy_shape.stp", "w", encoding="utf-8") as f:
                    f.write("FAKE")

                result = self.runner.invoke(
                    intersect,
                    ["--in-step", "dummy_shape.stp", "--in-plane", "0,0,100:0,0,1"],
                )

            assert result.exit_code == 0, result.output

    def test_intersect_export_step_failure(self):
        """Test CLI when STEP export fails."""
        with (
            patch("intersector.cli.read_step") as mock_read,
            patch("intersector.cli.parse_plane_input") as mock_parse,
            patch("intersector.cli.intersect_with_plane") as mock_intersect,
            patch("intersector.cli.is_intersection_valid") as mock_valid,
            patch("intersector.cli.export_step") as mock_export,
        ):

            mock_shape = MagicMock(name="TopoDS_Shape")
            mock_read.return_value = mock_shape
            mock_parse.return_value = ((0, 0, 0), (0, 0, 1))
            mock_intersect.return_value = mock_shape
            mock_valid.return_value = True
            mock_export.return_value = False  # Simulate no intersection.

            with self.runner.isolated_filesystem():
                with open("dummy_shape.stp", "w", encoding="utf-8") as f:
                    f.write("FAKE")

                result = self.runner.invoke(
                    intersect,
                    ["--in-step", "dummy_shape.stp", "--in-plane", "0,0,100:0,0,1"],
                )

            assert result.exit_code != 0
            assert "Failed to export intersection result." in result.output

    def test_intersect_show_shapes_failure(self):
        """Test CLI when visualization fails."""
        with (
            patch("intersector.cli.read_step") as mock_read,
            patch("intersector.cli.parse_plane_input") as mock_parse,
            patch("intersector.cli.intersect_with_plane") as mock_intersect,
            patch("intersector.cli.is_intersection_valid") as mock_valid,
            patch("intersector.cli.export_step") as mock_export,
            patch("intersector.cli.show_shapes") as mock_show,
        ):

            mock_shape = MagicMock(name="TopoDS_Shape")
            mock_read.return_value = mock_shape
            mock_parse.return_value = ((0, 0, 0), (0, 0, 1))
            mock_intersect.return_value = mock_shape
            mock_valid.return_value = True
            mock_export.return_value = True
            mock_show.return_value = False

            with self.runner.isolated_filesystem():
                with open("dummy_shape.stp", "w", encoding="utf-8") as f:
                    f.write("FAKE")

                result = self.runner.invoke(
                    intersect,
                    ["--in-step", "dummy_shape.stp", "--in-plane", "0,0,100:0,0,1"],
                )

            assert result.exit_code != 0
            assert "Error displaying shapes" in result.output
