"""Deterministic feature preparation shared by the app and export jobs."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


TABLEAU_COLUMNS = [
    "ID",
    "Source",
    "Severity",
    "Start_Time",
    "Start_Lat",
    "Start_Lng",
    "State",
    "County",
    "Timezone",
    "Temperature(F)",
    "Wind_Chill(F)",
    "Humidity(%)",
    "Pressure(in)",
    "Visibility(mi)",
    "Wind_Direction",
    "Wind_Speed(mph)",
    "Precipitation(in)",
    "Weather_Condition",
    "Amenity",
    "Crossing",
    "Junction",
    "Sunrise_Sunset",
]


def collapse_categories(series: pd.Series, top_n: int = 8) -> pd.Series:
    normalized = series.fillna("Missing").astype(str)
    top = normalized.value_counts().head(top_n).index
    return normalized.where(normalized.isin(top), "Other")


def load_profile_sample(
    csv_path: Path,
    columns: Iterable[str],
    row_limit: int = 120_000,
) -> pd.DataFrame:
    frame = pd.read_csv(csv_path, usecols=list(columns), nrows=row_limit)
    frame["Start_Time"] = pd.to_datetime(frame["Start_Time"], errors="coerce", format="mixed")
    frame["Hour"] = frame["Start_Time"].dt.hour
    frame["Month"] = frame["Start_Time"].dt.month
    frame["Weekday"] = frame["Start_Time"].dt.day_name()
    frame["Severe"] = frame["Severity"] >= 3
    return frame


def build_master_extract(csv_path: Path, row_limit: int = 180_000) -> pd.DataFrame:
    frame = pd.read_csv(csv_path, usecols=TABLEAU_COLUMNS, nrows=row_limit)
    frame["Start_Time"] = pd.to_datetime(frame["Start_Time"], errors="coerce", format="mixed")
    frame = frame.dropna(subset=["Start_Time", "Severity", "Start_Lat", "Start_Lng"]).copy()
    frame["Year"] = frame["Start_Time"].dt.year
    frame["Month"] = frame["Start_Time"].dt.month
    frame["Month_Name"] = frame["Start_Time"].dt.month_name()
    frame["Hour"] = frame["Start_Time"].dt.hour
    frame["Weekday"] = frame["Start_Time"].dt.day_name()
    frame["Severe_Flag"] = (frame["Severity"] >= 3).astype(int)
    frame["Severity_Group"] = frame["Severe_Flag"].map({0: "Mild (1-2)", 1: "Severe (3-4)"})
    frame["Weather_Group"] = collapse_categories(frame["Weather_Condition"])
    frame["Wind_Group"] = collapse_categories(frame["Wind_Direction"])
    frame["Day_Night"] = frame["Sunrise_Sunset"].fillna("Unknown")
    return frame

