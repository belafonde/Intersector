"""Logging utilities for task1.

Provides centralized configuration for logging across CLI commands.
"""

import logging

from rich.logging import RichHandler


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure and return the root logger.

    Args:
        verbose (bool, optional): If True, sets logging level to DEBUG.
            Defaults to INFO.

    Returns:
        logging.Logger: Configured logger instance.

    """
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
    )

    rich_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_path=True,
        log_time_format="[%X]",
    )

    logger = logging.getLogger("intersector")
    logger.handlers.clear()
    logger.addHandler(rich_handler)
    logger.setLevel(level)
    logger.propagate = False

    return logger
