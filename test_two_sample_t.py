import warnings

import datasense as ds
import pandas as pd


warnings.filterwarnings("ignore")
series1_two_sample_t = pd.Series(
    data=[32, 37, 35, 38, 41, 44, 35, 31, 34, 38, 42],
    name="y1"
)
series2_two_sample_t = pd.Series(
    data=[36, 31, 30, 31, 34, 36, 39, 32, 31],
    name="y2"
)


def test_two_sample_t():
    result = ds.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis="two-sided",
        significance_level=0.05,
    )
    # expected = (
    # t statistic, t p value, t power,
    # Shapiro-Wilk statistic sample 1, Shapiro-Wilk p value sample 1,
    # Shapiro-Wilk statistic sample 2, Shapiro-Wilk p value sample 2
    # )
    expected = (
        2.206697123558633, 0.040563312956175504, 0.5510566836848744,
        0.9662597179412842, 0.8464781045913696,
        0.8837727308273315, 0.17198464274406433
    )
    assert result == expected
    result = ds.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis="less",
        significance_level=0.05,
    )
    expected = (
        2.206697123558633, 0.9797183435219122, 8.068361761393895e-05,
        0.9662597179412842, 0.8464781045913696,
        0.8837727308273315, 0.17198464274406433
    )
    assert result == expected
    result = ds.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis="greater",
        significance_level=0.05,
    )
    expected = (
        2.206697123558633, 0.020281656478087752, 0.6835840521967709,
        0.9662597179412842, 0.8464781045913696,
        0.8837727308273315, 0.17198464274406433
    )
    assert result == expected
