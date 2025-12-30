from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils import AppError, COLUMNS


def load_applications_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise AppError(f"CSV not found at {path}. Create it first (Day 1).")

    try:
        df = pd.read_csv(path, dtype=str).fillna("")
    except Exception as e:
        raise AppError(f"Failed to read CSV at {path}: {e}")

    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise AppError(f"CSV schema mismatch. Missing columns: {missing}")

    return df[COLUMNS]


def save_applications_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)
