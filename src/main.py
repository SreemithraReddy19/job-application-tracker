from __future__ import annotations

import argparse
import logging

from commands import cmd_add, cmd_list, cmd_update, cmd_summary
from utils import AppError, setup_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Job Application Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new job application")
    add_parser.add_argument("--company", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--location")
    add_parser.add_argument("--source")
    add_parser.add_argument("--notes")
    add_parser.add_argument("--status")
    add_parser.add_argument("--date_applied")
    add_parser.set_defaults(func=cmd_add)

    # list
    list_parser = subparsers.add_parser("list", help="List job applications")
    list_parser.add_argument("--company")
    list_parser.add_argument("--status")
    list_parser.set_defaults(func=cmd_list)

    # update
    update_parser = subparsers.add_parser("update", help="Update a job application")
    update_parser.add_argument("--company", required=True)
    update_parser.add_argument("--role", required=True)
    update_parser.add_argument("--status")
    update_parser.add_argument("--notes")
    update_parser.set_defaults(func=cmd_update)

    # summary
    summary_parser = subparsers.add_parser("summary", help="Show application statistics")
    summary_parser.set_defaults(func=cmd_summary)

    return parser


def main() -> None:
    setup_logging()
    parser = build_parser()

    try:
        args = parser.parse_args()
        args.func(args)

    except AppError as e:
        logging.warning("AppError: %s", e)
        print(f"Error: {e}")

    except Exception:
        logging.exception("Unhandled exception")
        print("Error: unexpected failure. Check output/job_tracker.log")


if __name__ == "__main__":
    main()
