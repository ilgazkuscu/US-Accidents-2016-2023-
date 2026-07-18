"""Filesystem configuration without machine-specific repository paths."""

from __future__ import annotations

import os
from pathlib import Path


DEFAULT_KAGGLE_CACHE = (
    Path.home()
    / ".cache"
    / "kagglehub"
    / "datasets"
    / "sobhanmoosavi"
    / "us-accidents"
    / "versions"
    / "13"
)


def resolve_dataset_csv(explicit_path: str | Path | None = None) -> Path:
    configured = explicit_path or os.getenv("US_ACCIDENTS_CSV")
    if configured:
        path = Path(configured).expanduser()
        if path.is_file():
            return path
        raise FileNotFoundError(f"Configured US accidents CSV does not exist: {path}")

    candidates = sorted(DEFAULT_KAGGLE_CACHE.glob("*.csv"))
    if candidates:
        return candidates[0]

    raise FileNotFoundError(
        "US Accidents CSV not found. Set US_ACCIDENTS_CSV or follow data/README.md."
    )


def cache_dir() -> Path:
    return Path(os.getenv("US_ACCIDENTS_CACHE_DIR", "data_cache")).expanduser()


def export_dir() -> Path:
    return Path(os.getenv("US_ACCIDENTS_EXPORT_DIR", "tableau_exports")).expanduser()

