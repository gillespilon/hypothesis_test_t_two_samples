#! /usr/bin/env python3
"""
Two-sample t test. Four scenarios.

Scenario 1
Is the average of sample one different from the average of sample two?

Scenario 2
Is the average of sample one greater than the average of sample two?

Scenario 3
Is the average of sample one less than the average of sample two?

Scenario 4
Is the average of sample one different from the average of sample two by a
hypothesized difference?

If you read a data file:
- first row is column labels: x y
- first column is sample number: 1 2
- second column is data

Requires datasense https://github.com/gillespilon/datasense
"""

from typing import List, NoReturn, Tuple
from pathlib import Path

import scipy.stats as stats
import datasense as ds
import pandas as pd
import numpy as np


def main():
    # define parameters
    filetypes = [("csv and feather files", ".csv .CSV .feather .FEATHER")]
    path_in_title = "Select csv or feather file to read"
    output_url = "two_sample_t_test.html"
    header_title = "Two-sample t test"
    header_id = "two-sample-t-test"
    original_stdout = ds.html_begin(
        output_url=output_url, header_title=header_title, header_id=header_id
    )
    # create DataFrames
    # df, sample_one, sample_two = create_dataframe_examples()
    df, sample_one, sample_two = create_dataframes(
        title=path_in_title, filetypes=filetypes
    )
    # print assumptions
    assumptions()
    # calculate parametric statistics
    levels = df['x'].sort_values().unique()
    for level in np.nditer(op=levels):
        print(level)
        series = df['y'][df['x'] == level]
        parametric_statistics = ds.parametric_summary(series=series)
        print(parametric_statistics)
        print()
    # calculate nonparametric statistics
    for level in np.nditer(op=levels):
        print(level)
        series = df['y'][df['x'] == level]
        nonparametric_statistics = ds.nonparametric_summary(series=series)
        print(nonparametric_statistics)
        print()
    # scenario one, equal variances
    print("Scenario 1")
    print(
        "Is the average of sample one different from the average of sample "
        "two?\n"
    )
    print("Assume the sample variances are equal.")
    test_statistic, p_value = scenario_one(
        sample_one=sample_one, sample_two=sample_two, equal_var=True
    )
    print()
    print("Assume the sample variances are unequal.")
    test_statistic, p_value = scenario_one(
        sample_one=sample_one, sample_two=sample_two, equal_var=False
    )
    print()
    ds.html_end(original_stdout=original_stdout, output_url=output_url)


def create_dataframe_examples() -> List[pd.DataFrame]:
    data = {
        "x": [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
        "y": [35, 28, 41, 44, 35, 31, 34, 38, 42, 36, 31, 30, 31, 34, 36, 29]
    }
    df = pd.DataFrame(data=data)
    sample_one = df[df["x"] == 1]
    sample_two = df[df["x"] == 2]
    return (df, sample_one, sample_two)


def create_dataframes(
    title: str,
    filetypes: List[Tuple[str, str]]
) -> List[pd.DataFrame]:
    initialdir = Path(__file__).parent.resolve()
    path_in = ds.ask_open_file_name_path(
        title=title, initialdir=initialdir, filetypes=filetypes
    )
    df = ds.read_file(file_name=path_in)
    sample_one = df[df["x"] == 1]
    sample_two = df[df["x"] == 2]
    return (df, sample_one, sample_two)


def scenario_one(
    sample_one: pd.DataFrame, sample_two: pd.DataFrame, equal_var: bool = True
) -> List[np.ndarray]:
    """
    Two-sample t test.
    Is the average of sample one different from the average of sample two?

    Parameters
    ----------
    sample_one : pd.DataFrame
        Sample one DataFrame.
    sample_two : pd.DataFrame
        Sample two DataFrame.

    Returns
    -------
    test_statistic : np.ndarray
        The calculated t statistics.
    p_value : np.ndarray
        The calculated p values.
    """
    test_statistic, p_value = stats.ttest_ind(
        a=sample_one, b=sample_two, equal_var=equal_var
    )
    print(f't: {test_statistic[-1]:7.3f}')
    print(f'p: {p_value[-1]:7.3f}')
    return (test_statistic, p_value)


def scenario_two():
    pass


def scenario_three():
    pass


def scenario_four():
    pass


def assumptions() -> NoReturn:
    print("ASSUMPTIONS")
    print()
    print("The data are continuous interval or ratio scales.")
    print()
    print(
        "The data in each sample follow a normal distribution with mean mu "
        "and variance sigma squared."
    )
    print()
    print(
        "The sample variances s squared follow a chi-squared distribution "
        "with rho degrees of freedom under the null hypothesis, where rho "
        "is a positive constant."
    )
    print()
    print(
        "(sample average - population averagee) and the sample standard "
        "deviations s are independent."
    )
    print("The size of each sample may be equal or unequal.")
    print()
    print("The variance of each sample may be equal or unequal.")
    print()
    print(
        "The data should be sampled independently from the two populations "
        "being compared."
    )
    print()


if __name__ == "__main__":
    main()
