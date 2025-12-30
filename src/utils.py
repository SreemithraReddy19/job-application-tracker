from __future__ import annotations

import logging
from datetime import date
from pathlib import Path

# Project root = .../job-tracker
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "applications.csv"
LOG_PATH = BASE_DIR / "output" / "job_tracker.log"

ALLOWED_STATUS = {"applied", "interview", "rejected", "offer"}
COLUMNS = ["company", "role", "location", "date_applied", "status", "source", "notes"]


class AppError(Exception):
    """Expected, user-facing error (no stack trace)."""


def setup_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear handlers to avoid duplicates across runs
    logger.handlers.clear()

    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Suppress logs to terminal (users should see prints, not logs)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(fmt)
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def require_non_empty(value: str | None, field_name: str) -> str:
    if value is None:
        raise AppError(f"--{field_name} is required")
    cleaned = value.strip()
    if cleaned == "":
        raise AppError(f"--{field_name} cannot be empty")
    return cleaned


def normalize_status(value: str) -> str:
    status = (value or "").strip().lower()
    if status == "":
        raise AppError("Status cannot be empty")
    if status not in ALLOWED_STATUS:
        raise AppError(f"Invalid status '{status}'. Allowed: {sorted(ALLOWED_STATUS)}")
    return status


def today_iso() -> str:
    return date.today().isoformat()