"""Unit tests for the logger setup utility."""

import logging
from unittest.mock import patch

from rich.logging import RichHandler

from intersector.utils.logger import setup_logging


class TestLoggingSetup:
    """Unit tests for the `setup_logging` function."""

    @staticmethod
    def test_setup_logging_default_level():
        """Test setup_logging() sets INFO level by default."""
        logger = setup_logging()
        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.INFO
        assert any(
            isinstance(h, logging.Handler) for h in logger.handlers
        ), "Logger should have at least one handler"
        assert not logger.propagate

    @staticmethod
    def test_setup_logging_verbose_level():
        """Test setup_logging() sets DEBUG level when verbose=True."""
        logger = setup_logging(verbose=True)
        assert logger.level == logging.DEBUG

    @staticmethod
    def test_setup_logging_replaces_handlers():
        """Test setup_logging() clears old handlers and adds RichHandler."""
        logger = logging.getLogger("intersector")
        logger.addHandler(logging.StreamHandler())  # add dummy handler

        new_logger = setup_logging()
        assert len(new_logger.handlers) == 1
        handler = new_logger.handlers[0]

        assert isinstance(handler, RichHandler)

    @staticmethod
    @patch("intersector.utils.logger.RichHandler")
    def test_setup_logging_creates_rich_handler(mock_rich_handler):
        """Test RichHandler is constructed with expected arguments."""
        setup_logging(verbose=True)
        mock_rich_handler.assert_called_once_with(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=True,
            log_time_format="[%X]",
        )
