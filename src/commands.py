from __future__ import annotations

import argparse
import logging

import pandas as pd

from storage import load_applications_csv, save_applications_csv
from utils import DATA_PATH, require_non_empty, normalize_status, today_iso, AppError


def cmd_add(args: argparse.Namespace) -> None:
    company = require_non_empty(args.company, "company")
    role = require_non_empty(args.role, "role")

    status = "applied" if not args.status else normalize_status(args.status)
    date_applied = (args.date_applied or today_iso()).strip() or today_iso()

    logging.info("ADD company=%s role=%s status=%s", company, role, status)

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
    # Prevent duplicates: company + role must be unique
    dup_mask = (df["company"] == company) & (df["role"] == role)
    if dup_mask.any():
        raise AppError(
            f"Duplicate entry: company='{company}' and role='{role}' already exists. Use update instead."
        )

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    save_applications_csv(df, DATA_PATH)

    print("Added application:")
    print(row)


def cmd_list(args: argparse.Namespace) -> None:
    # Validate filters FIRST (even if dataset is empty)
    status = None
    if args.status:
        status = normalize_status(args.status)

    df = load_applications_csv(DATA_PATH)

    if df.empty:
        logging.info("LIST: empty dataset")
        print("No applications found.")
        return

    if status:
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

    if not args.status and not args.notes:
        print("Nothing to update. Provide --status and/or --notes.")
        return

    if args.status:
        df.loc[mask, "status"] = normalize_status(args.status)

    if args.notes:
        df.loc[mask, "notes"] = args.notes.strip()

    save_applications_csv(df, DATA_PATH)

    logging.info("UPDATE company=%s role=%s status=%s", company, role, args.status)
    print("Application updated:")
    print(df[mask].to_string(index=False))


def cmd_summary(args: argparse.Namespace) -> None:
    df = load_applications_csv(DATA_PATH)

    if df.empty:
        logging.info("SUMMARY: empty dataset")
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
