from pathlib import Path

import pandas as pd

from us_accidents import build_master_extract, export_dir, resolve_dataset_csv


def export_tables(df: pd.DataFrame, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)

    master_columns = [
        "ID", "Source", "Severity", "Severity_Group", "Severe_Flag", "Start_Time",
        "Year", "Month", "Month_Name", "Hour", "Weekday", "State", "County",
        "Timezone", "Start_Lat", "Start_Lng", "Temperature(F)", "Wind_Chill(F)",
        "Humidity(%)", "Pressure(in)", "Visibility(mi)", "Wind_Speed(mph)",
        "Precipitation(in)", "Weather_Condition", "Weather_Group", "Wind_Direction",
        "Wind_Group", "Amenity", "Crossing", "Junction", "Day_Night",
    ]
    df[master_columns].to_csv(output / "01_master_sample.csv", index=False)

    grouped_exports = {
        "02_accidents_by_hour.csv": df.groupby("Hour").size().reset_index(name="Accident_Count"),
        "03_hour_by_severity.csv": df.groupby(["Hour", "Severity_Group"]).size().reset_index(name="Accident_Count"),
        "04_accidents_by_month.csv": df.groupby(["Month", "Month_Name"]).size().reset_index(name="Accident_Count").sort_values("Month"),
        "05_weather_by_severity.csv": df.groupby(["Weather_Group", "Severity_Group"]).size().reset_index(name="Accident_Count"),
        "08_daynight_by_severity.csv": df.groupby(["Day_Night", "Severity_Group"]).size().reset_index(name="Accident_Count"),
        "09_source_by_severity.csv": df.groupby(["Source", "Severity_Group"]).size().reset_index(name="Accident_Count"),
    }
    for filename, table in grouped_exports.items():
        table.to_csv(output / filename, index=False)

    state_summary = (
        df.groupby("State")
        .agg(
            Accident_Count=("ID", "count"),
            Severe_Rate=("Severe_Flag", "mean"),
            Avg_Visibility=("Visibility(mi)", "mean"),
            Avg_Precipitation=("Precipitation(in)", "mean"),
        )
        .reset_index()
        .sort_values("Accident_Count", ascending=False)
    )
    state_summary.to_csv(output / "06_state_summary.csv", index=False)

    numeric = [
        "Visibility(mi)", "Pressure(in)", "Wind_Chill(F)",
        "Precipitation(in)", "Humidity(%)", "Wind_Speed(mph)",
    ]
    df[numeric].corr(numeric_only=True).reset_index().rename(
        columns={"index": "Feature"}
    ).to_csv(output / "07_numeric_correlation.csv", index=False)

    df[["Start_Lat", "Start_Lng", "Severity_Group"]].sample(
        min(40_000, len(df)), random_state=42
    ).to_csv(output / "10_map_sample.csv", index=False)


def main() -> None:
    output = export_dir()
    export_tables(build_master_extract(resolve_dataset_csv()), output)
    print(f"Tableau exports created in: {output}")


if __name__ == "__main__":
    main()
