"""Small statistical helpers used by the exploratory hypothesis view."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def two_proportion_z_test(success_a: int, size_a: int, success_b: int, size_b: int):
    if size_a <= 0 or size_b <= 0:
        return np.nan, np.nan
    pooled = (success_a + success_b) / (size_a + size_b)
    standard_error = np.sqrt(pooled * (1 - pooled) * ((1 / size_a) + (1 / size_b)))
    if standard_error == 0:
        return np.nan, np.nan
    statistic = ((success_a / size_a) - (success_b / size_b)) / standard_error
    return statistic, 2 * (1 - stats.norm.cdf(abs(statistic)))


def cramers_v(contingency: pd.DataFrame) -> float:
    chi_squared = stats.chi2_contingency(contingency)[0]
    observations = contingency.to_numpy().sum()
    if observations == 0:
        return np.nan
    rows, columns = contingency.shape
    denominator = min(columns - 1, rows - 1)
    return np.nan if denominator <= 0 else np.sqrt((chi_squared / observations) / denominator)


def cohens_d(group_a: pd.Series, group_b: pd.Series) -> float:
    size_a, size_b = len(group_a), len(group_b)
    if size_a < 2 or size_b < 2:
        return np.nan
    variance_a, variance_b = group_a.std(ddof=1), group_b.std(ddof=1)
    pooled = np.sqrt(
        ((size_a - 1) * variance_a**2 + (size_b - 1) * variance_b**2)
        / (size_a + size_b - 2)
    )
    return 0.0 if pooled == 0 else (group_a.mean() - group_b.mean()) / pooled

