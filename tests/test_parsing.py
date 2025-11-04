# Copyright (c) 2025 Yannis Arapakis
# Licensed under the MIT License. See LICENSE file for details.
"""Unit tests for parse_plane_input in parsing.py."""

import pytest

from intersector.utils import parsing
from intersector.utils.logger import setup_logging


class TestParsePlaneInput:
    """Unit tests for the parse_plane_input() function."""

    @staticmethod
    def test_parse_plane_input_valid():
        """Test that a valid plane string is correctly parsed."""
        plane_str = "0,0,100:0,0,1"
        point, normal = parsing.parse_plane_input(plane_str)
        assert point == (0.0, 0.0, 100.0)
        assert normal == (0.0, 0.0, 1.0)

    @staticmethod
    @pytest.mark.parametrize(
        "plane_str",
        [
            "0,0,100-0,0,1",  # missing colon
            "0,0,100:",  # missing normal
            ":0,0,1",  # missing point
            "0,0,100:0,0",  # incomplete normal
            "0,0,100:0,0,1,2",  # too many values in normal
            "0,0:0,0,1",  # incomplete point
            "0,0,100,5:0,0,1",  # too many values in point
            "a,b,c:d,e,f",  # non-numeric values
            "",  # empty string
        ],
    )
    def test_parse_plane_input_invalid_formats(plane_str):
        """Test that invalid plane strings raise ValueError and log an error."""
        setup_logging()  # Ensure logging is set up for the test
        with pytest.raises(ValueError, match="Plane format must be 'x,y,z:nx,ny,nz'"):
            parsing.parse_plane_input(plane_str)
