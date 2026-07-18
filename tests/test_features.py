from pathlib import Path

import pandas as pd

from us_accidents.features import build_master_extract, collapse_categories, load_profile_sample


def _fixture() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ID": ["A", "B", "C"],
            "Source": ["MapQuest", "Bing", "Bing"],
            "Severity": [2, 3, 4],
            "Start_Time": ["2023-01-01 08:00", "2023-01-02 20:00", None],
            "Start_Lat": [38.9, 39.0, 40.0],
            "Start_Lng": [-77.0, -77.1, -78.0],
            "State": ["DC", "MD", "VA"],
            "County": ["District", "Montgomery", "Fairfax"],
            "Timezone": ["US/Eastern"] * 3,
            "Temperature(F)": [40.0, 35.0, 30.0],
            "Wind_Chill(F)": [38.0, 32.0, 25.0],
            "Humidity(%)": [60.0, 70.0, 80.0],
            "Pressure(in)": [30.0, 29.8, 29.5],
            "Visibility(mi)": [10.0, 5.0, 2.0],
            "Wind_Direction": ["N", "S", "S"],
            "Wind_Speed(mph)": [5.0, 10.0, 12.0],
            "Precipitation(in)": [0.0, 0.1, 0.2],
            "Weather_Condition": ["Clear", "Rain", "Rain"],
            "Amenity": [False, True, False],
            "Crossing": [True, False, False],
            "Junction": [False, True, True],
            "Sunrise_Sunset": ["Day", "Night", None],
        }
    )


def test_collapse_categories_preserves_only_top_labels():
    collapsed = collapse_categories(pd.Series(["A", "A", "B", "C", None]), top_n=1)
    assert collapsed.tolist() == ["A", "A", "Other", "Other", "Other"]


def test_master_extract_derives_time_and_severity_fields(tmp_path: Path):
    path = tmp_path / "fixture.csv"
    _fixture().to_csv(path, index=False)
    result = build_master_extract(path)
    assert len(result) == 2
    assert result["Severe_Flag"].tolist() == [0, 1]
    assert result["Hour"].tolist() == [8, 20]


def test_profile_sample_uses_requested_contract(tmp_path: Path):
    path = tmp_path / "fixture.csv"
    frame = _fixture()
    frame.to_csv(path, index=False)
    columns = ["Source", "Severity", "Start_Time"]
    result = load_profile_sample(path, columns)
    assert {"Hour", "Month", "Weekday", "Severe"}.issubset(result.columns)

