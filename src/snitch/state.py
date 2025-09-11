"""Manages the state of the Snitch application."""

import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "snitch"
STATE_FILE = CONFIG_DIR / "state.json"


def load_state():
    """Load the last saved state."""
    if not STATE_FILE.exists():
        return None
    try:
        with STATE_FILE.open("r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def save_state(state_data):
    """Save the current state."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w") as f:
        json.dump(state_data, f, indent=4)
