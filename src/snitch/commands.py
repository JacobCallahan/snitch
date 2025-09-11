"""Provides command-line functionality for Snitch."""

import argparse
import datetime

from snitch.logging import logger
from snitch.server import serve_api
from snitch.snitch import check_activity
from snitch.state import load_state


def display_status():
    """Display the current status from the state file."""
    state = load_state()
    if not state:
        # Use logger here since this is an unexpected state/error
        logger.warning("No state file found. Run 'check' first.")
        return

    # Use print for direct user-facing output
    print("\n--- System Activity Status ---")  # noqa: T201
    if state["is_active"]:
        print(f"Status: ACTIVE (within last {state['check_threshold_days']} days)")  # noqa: T201
    else:
        print(f"Status: INACTIVE (for at least {state['check_threshold_days']} days)")  # noqa: T201

    print(f"Confidence: {state['confidence_percent']}")  # noqa: T201
    last_active = state.get("last_file_activity_time")
    if last_active:
        print(  # noqa: T201
            f"Last File Activity: {datetime.datetime.fromisoformat(last_active).strftime('%Y-%m-%d %H:%M:%S')}"
        )
    else:
        print("Last File Activity: None within threshold")  # noqa: T201
    print(  # noqa: T201
        f"Last Checked: {datetime.datetime.fromisoformat(state['last_checked_time']).strftime('%Y-%m-%d %H:%M:%S')}"
    )


def main():
    """Parse arguments and execute commands."""
    parser = argparse.ArgumentParser(
        description="Snitch: A simple system activity monitor using a plugin-based approach."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Run an activity check and update state.")
    check_parser.set_defaults(func=lambda args: (check_activity(), display_status()))

    status_parser = subparsers.add_parser("status", help="Display the last known activity status.")
    status_parser.set_defaults(func=lambda args: display_status())

    serve_parser = subparsers.add_parser("serve", help="Serve the status via an HTTP API.")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to serve the API on.")
    serve_parser.set_defaults(func=lambda args: serve_api(args.port))

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
