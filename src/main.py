import argparse
import sys
from datetime import date
from pathlib import Path

import pandas as pd


DATA_PATH = Path("data") / "applications.csv"
ALLOWED_STATUS = {"applied", "interview", "rejected", "offer"}
COLUMNS = ["company", "role", "location", "date_applied", "status", "source", "notes"]


def require_non_empty(value: str, field_name: str) -> str:
    if value is None:
        print(f"Error: --{field_name} is required")
        sys.exit(1)
    cleaned = value.strip()
    if cleaned == "":
        print(f"Error: --{field_name} cannot be empty")
        sys.exit(1)
    return cleaned


def load_applications_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        print(f"Error: CSV not found at {path}. Did you create it on Day 1?")
        sys.exit(1)

    df = pd.read_csv(path, dtype=str).fillna("")
    # Basic safety: ensure expected columns exist
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        print(f"Error: CSV is missing columns: {missing}")
        sys.exit(1)

    # Keep only expected columns (in case someone added extras)
    return df[COLUMNS]


def save_applications_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def cmd_add(args: argparse.Namespace) -> None:
    company = require_non_empty(args.company, "company")
    role = require_non_empty(args.role, "role")

    status = (args.status or "applied").strip().lower()
    if status not in ALLOWED_STATUS:
        print(f"Error: invalid status '{status}'. Allowed: {sorted(ALLOWED_STATUS)}")
        sys.exit(1)

    date_applied = (args.date_applied or date.today().isoformat()).strip()
    if date_applied == "":
        date_applied = date.today().isoformat()

    row = {
        "company": company,
        "role": role,
        "location": (args.location or "").strip(),
        "date_applied": date_applied,
        "status": status,
        "source": (args.source or "").strip(),
        "notes": (args.notes or "").strip(),
    }

    df = load_applications_csv(DATA_PATH)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    save_applications_csv(df, DATA_PATH)

    print("Added application:")
    print(row)

def cmd_list(args: argparse.Namespace) -> None:
    df = load_applications_csv(DATA_PATH)

    if df.empty:
        print("No applications found.")
        return

    if args.status:
        status = args.status.strip().lower()
        df = df[df["status"] == status]

    if args.company:
        company = args.company.strip()
        df = df[df["company"] == company]

    if df.empty:
        print("No applications match the given filters.")
        return

    print(df.to_string(index=False))

def cmd_update(args: argparse.Namespace) -> None:
    company = require_non_empty(args.company, "company")
    role = require_non_empty(args.role, "role")

    df = load_applications_csv(DATA_PATH)

    mask = (df["company"] == company) & (df["role"] == role)
    matches = df[mask]

    if matches.empty:
        print(f"No application found for company='{company}' and role='{role}'.")
        return

    if len(matches) > 1:
        print("Error: multiple matching applications found. Refusing to update.")
        return

    if args.status:
        status = args.status.strip().lower()
        if status not in ALLOWED_STATUS:
            print(f"Error: invalid status '{status}'. Allowed: {sorted(ALLOWED_STATUS)}")
            return
        df.loc[mask, "status"] = status

    if args.notes:
        df.loc[mask, "notes"] = args.notes.strip()

    save_applications_csv(df, DATA_PATH)

    print("Application updated:")
    print(df[mask].to_string(index=False))

def cmd_summary(args: argparse.Namespace) -> None:
    df = load_applications_csv(DATA_PATH)

    if df.empty:
        print("No applications found.")
        return

    total = len(df)

    print("Summary")
    print("-" * 20)
    print(f"Total applications: {total}")
    print()

    print("By status:")
    status_counts = df["status"].value_counts()
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    print()

    print("By source:")
    source_counts = df["source"].replace("", "Unknown").value_counts()
    for source, count in source_counts.items():
        print(f"  {source}: {count}")


def main():
    parser = argparse.ArgumentParser(description="Job Application Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new job application")
    add_parser.add_argument("--company", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--location")
    add_parser.add_argument("--source")
    add_parser.add_argument("--notes")
    add_parser.add_argument("--status")        # optional; defaults to applied
    add_parser.add_argument("--date_applied")  # optional; defaults to today
    add_parser.set_defaults(func=cmd_add)

    # list (placeholder for Day 4)
    list_parser = subparsers.add_parser("list", help="List job applications")
    list_parser.add_argument("--company")
    list_parser.add_argument("--status")
    list_parser.set_defaults(func=cmd_list)


    # update (placeholder for Day 5)
    update_parser = subparsers.add_parser("update", help="Update a job application")
    update_parser.add_argument("--company", required=True)
    update_parser.add_argument("--role", required=True)
    update_parser.add_argument("--status")
    update_parser.add_argument("--notes")
    update_parser.set_defaults(func=cmd_update)

    summary_parser = subparsers.add_parser(
        "summary", help="Show application statistics"
    )
    summary_parser.set_defaults(func=cmd_summary)



    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        # Day 3: only add is real; others are still plumbing
        print("Parsed arguments:")
        print(args)


if __name__ == "__main__":
    main()