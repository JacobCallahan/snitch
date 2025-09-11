"""Provides logging functionality for the Snitch application."""

import logging
import sys


def setup_logger(log_file="/var/log/snitch.log"):
    """Set up the main logger for the application."""
    logger = logging.getLogger("snitch")
    logger.setLevel(logging.INFO)

    # Prevent logging from propagating to the root logger
    logger.propagate = False

    # If handlers are already configured, don't add them again
    if logger.hasHandlers():
        return logger

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler (to stderr)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    # File Handler
    try:
        # Use 'a' mode to append to the log file
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (PermissionError, FileNotFoundError) as e:
        # Use a standalone print here or a basic logger config, because the logger isn't fully set up.
        logging.warning(
            "Could not set up file logger at %s: %s. Logging to stderr only.", log_file, e
        )

    return logger


# Create a single logger instance to be used across the application
logger = setup_logger()
