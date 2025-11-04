# Copyright (c) 2025 Yannis Arapakis
# Licensed under the MIT License. See LICENSE file for details.
"""Unit tests for the visualization utilities using pythonocc.

This test suite verifies the behavior of `show_shape` and `show_shapes`
functions in `visualization.py`, ensuring they properly initialize
the OCC display, visualize shapes, and handle errors gracefully.

All OCC dependencies are mocked, as these functions rely on GUI rendering.
"""

import logging
from unittest.mock import MagicMock, patch

from intersector.utils import visualization


class TestVisualization:
    """Test suite for 3D visualization utilities."""

    @staticmethod
    @patch("intersector.utils.visualization.init_display")
    def test_show_shape_calls_occ_display(mock_init_display):
        """Test that `show_shape` initializes display and calls correct OCC methods."""
        mock_display = MagicMock()
        mock_start_display = MagicMock()
        mock_init_display.return_value = (
            mock_display,
            mock_start_display,
            MagicMock(),
            MagicMock(),
        )

        dummy_shape = MagicMock()
        visualization.show_shape(dummy_shape)

        mock_display.DisplayShape.assert_called_once_with(dummy_shape, update=True)
        mock_display.View.SetProj.assert_called_once_with(1, 1, 1)
        mock_start_display.assert_called_once()

    @staticmethod
    @patch("intersector.utils.visualization.init_display")
    def test_show_shapes_multiple_valid_shapes(mock_init_display):
        """Test that `show_shapes` displays multiple shapes and returns True."""
        mock_display = MagicMock()
        mock_start_display = MagicMock()
        mock_init_display.return_value = (
            mock_display,
            mock_start_display,
            MagicMock(),
            MagicMock(),
        )

        shapes = [MagicMock(), MagicMock()]
        result = visualization.show_shapes(shapes)

        assert result is True
        assert mock_display.DisplayShape.call_count == len(shapes)
        mock_display.FitAll.assert_called_once()
        mock_start_display.assert_called_once()

    @staticmethod
    @patch("intersector.utils.visualization.init_display")
    def test_show_shapes_handles_runtime_error(mock_init_display, caplog):
        """Test that `show_shapes` logs and returns False on RuntimeError."""
        mock_init_display.side_effect = RuntimeError("OCC init failed")
        caplog.set_level(logging.ERROR)

        result = visualization.show_shapes([MagicMock()])

        assert result is False
        assert "Error visualizing the shapes" in caplog.text
        assert "OCC init failed" in caplog.text

    @staticmethod
    @patch("intersector.utils.visualization.init_display")
    def test_show_shapes_handles_type_error(mock_init_display, caplog):
        """Test that `show_shapes` logs and returns False on TypeError."""
        mock_display = MagicMock()
        mock_display.DisplayShape.side_effect = TypeError("Invalid shape type")
        mock_init_display.return_value = (
            mock_display,
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        caplog.set_level(logging.ERROR)
        result = visualization.show_shapes(["not_a_shape"])

        assert result is False
        assert "Invalid shape type" in caplog.text
        assert "Error visualizing the shapes" in caplog.text

    @staticmethod
    @patch("intersector.utils.visualization.init_display")
    def test_show_shapes_empty_list(mock_init_display):
        """Test that `show_shapes` handles an empty shape list gracefully."""
        mock_display = MagicMock()
        mock_start_display = MagicMock()
        mock_init_display.return_value = (
            mock_display,
            mock_start_display,
            MagicMock(),
            MagicMock(),
        )

        result = visualization.show_shapes([])

        # It should still open a display and return True, even if no shapes are shown
        assert result is True
        mock_display.DisplayShape.assert_not_called()
        mock_display.FitAll.assert_called_once()
        mock_start_display.assert_called_once()
