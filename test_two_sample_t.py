import warnings

import datasense as ds
import pandas as pd


warnings.filterwarnings("ignore")
series1_two_sample_t = pd.Series(
    data=[32, 37, 35, 28, 41, 44, 35, 31, 34, 38, 42],
    name="y1"
)
series2_two_sample_t = pd.Series(
    data=[36, 31, 30, 31, 34, 36, 29, 32, 31],
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
    # Shapiro-Wilk statistic sample 2, Shapiro-Wilk p value sample 2,
    # Bartlett test statistic, Bartlett p value
    # Anderson-Darling test statistic, Anderson-Darling p value`
    # )
    expected = (
        2.1353336482435243, 0.0467302735601054, 0.5243039932709265,
        0.9785250425338745, 0.9574037790298462,
        0.8853150606155396, 0.17846621572971344,
        3.2744574205759416, 0.07036619072494953,
        0.15265397324961683, 0.68, 0.49940696863048295, 0.693,
        0.06234516845619442, 7.67502856891755
    )
    assert result == expected
    result = ds.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis="less",
        significance_level=0.05,
    )
    expected = (
        2.1353336482435243, 0.9766348632199473, 0.00010611922933969828,
        0.9785250425338745, 0.9574037790298462,
        0.8853150606155396, 0.17846621572971344,
        3.2744574205759416, 0.07036619072494953,
        0.15265397324961683, 0.68, 0.49940696863048295, 0.693,
        0.06234516845619442, 7.67502856891755
    )
    assert result == expected
    result = ds.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis="greater",
        significance_level=0.05,
    )
    expected = (
        2.1353336482435243, 0.0233651367800527, 0.6587984489683615,
        0.9785250425338745, 0.9574037790298462,
        0.8853150606155396, 0.17846621572971344,
        3.2744574205759416, 0.07036619072494953,
        0.15265397324961683, 0.68, 0.49940696863048295, 0.693,
        0.06234516845619442, 7.67502856891755
    )
    assert result == expected
