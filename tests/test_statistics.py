import numpy as np
import pandas as pd

from us_accidents.statistics import cohens_d, cramers_v, two_proportion_z_test


def test_two_proportion_test_handles_invalid_group_size():
    statistic, p_value = two_proportion_z_test(0, 0, 1, 2)
    assert np.isnan(statistic)
    assert np.isnan(p_value)


def test_cramers_v_detects_perfect_association():
    table = pd.DataFrame([[10, 0], [0, 10]])
    assert cramers_v(table) > 0.8


def test_cohens_d_is_zero_for_equal_groups():
    group = pd.Series([1.0, 2.0, 3.0])
    assert cohens_d(group, group) == 0.0
