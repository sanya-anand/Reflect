"""Structured logging configuration for the application."""

import logging
import sys


def setup_logger() -> logging.Logger:
    """Configure and return the application logger."""
    logger = logging.getLogger("reflect")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers on reload
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
