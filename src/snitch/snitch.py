"""Contains the core logic for the Snitch application."""

import datetime
from pathlib import Path

from snitch.logging import logger
from snitch.plugins import load_plugins
from snitch.state import save_state

# --- Constants ---
DAYS_AGO_THRESHOLD = 5


def get_file_mtime(file_path):
    """Get last modification time of a file."""
    try:
        return datetime.datetime.fromtimestamp(Path(file_path).stat().st_mtime)
    except (FileNotFoundError, PermissionError):
        return None


def check_activity():
    """Check for system activity using loaded plugins and update the state file."""
    plugins = load_plugins()
    if not plugins:
        logger.warning("No plugins to run. Exiting.")
        return

    # For now, we just use the first plugin found.
    # A real implementation might select a plugin based on OS.
    plugin = plugins[0]
    logger.info(f"Using plugin: {plugin.name}")

    threshold = datetime.datetime.now() - datetime.timedelta(days=DAYS_AGO_THRESHOLD)
    latest_activity_time = None
    active_weight = 0
    total_weight = 0

    logger.info(
        f"--- Running Activity Check (Threshold: > {threshold.strftime('%Y-%m-%d %H:%M:%S')}) ---"
    )

    # 1. Process file-based checks
    logger.info("--- Checking files ---")
    files_to_check = getattr(plugin, "files", [])
    for file_info in files_to_check:
        path = file_info.get("path")
        weight = file_info.get("weight", 1)
        total_weight += weight

        logger.info(f"Checking: {path}...")
        mtime = get_file_mtime(path)
        if mtime:
            is_active = mtime > threshold
            logger.info(
                f"  -> Last modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')}. Active: {is_active}"
            )
            if is_active:
                active_weight += weight
                if latest_activity_time is None or mtime > latest_activity_time:
                    latest_activity_time = mtime
        else:
            logger.warning(f"  -> Not found or permission error for {path}.")

    # 2. Process function-based checks
    logger.info("--- Running function checks ---")
    for name in dir(plugin):
        attr = getattr(plugin, name)
        if callable(attr) and hasattr(attr, "_weight"):
            weight = attr._weight
            total_weight += weight
            logger.info(f"Running: {name} (Weight: {weight})...")

            is_active = attr()
            logger.info(f"  -> Active: {is_active}")
            if is_active:
                active_weight += weight

    # 3. Calculate final state
    system_is_active = active_weight > 0
    confidence = (active_weight / total_weight) * 100 if total_weight > 0 else 0

    state = {
        "is_active": system_is_active,
        "confidence_percent": round(confidence, 2),
        "last_file_activity_time": latest_activity_time.isoformat()
        if latest_activity_time
        else None,
        "last_checked_time": datetime.datetime.now().isoformat(),
        "check_threshold_days": DAYS_AGO_THRESHOLD,
    }

    save_state(state)
    logger.info("Activity check complete. State file updated.")
