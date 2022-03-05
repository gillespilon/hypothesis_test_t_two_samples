#! /usr/bin/env python3
"""
Two-sample t test. Four scenarios.

Scenario 1
Is the average of sample one different from the average of sample two?

Scenario 2
Is the average of sample one less than the average of sample two?

Scenario 3
Is the average of sample one greater than the average of sample two?

Scenario 4
Is the average of sample one different from the average of sample two by a
hypothesized difference?

If you read a data file:
- first row is column labels: x y
- first column is sample number: 1 2
- second column is data

Requires datasense https://github.com/gillespilon/datasense
"""

from typing import List, Tuple
from pathlib import Path
import time

import datasense as ds
import pandas as pd


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
    ds.script_summary(
        script_path=Path(__file__),
        action='started at'
    )
    # create DataFrames
    # df, sample_one, sample_two = create_dataframe_examples()
    df, sample_one, sample_two = create_dataframes(
        title=path_in_title, filetypes=filetypes
    )
    start_time = time.perf_counter()
    # scenario 1
    print("Scenario 1")
    print(
        "Is the average of sample one different from the average of sample "
        "two?\n"
    )
    ds.two_sample_t(
        df=df, xlabel='x', ylabel='y', alternative_hypothesis='unequal',
        significance_level=0.05
    )
    print("========== end of scenario ==========")
    print()
    # scenario 2
    print("Scenario 2")
    print(
        "Is the average of sample one less than the average of sample "
        "two?\n"
    )
    ds.two_sample_t(
        df=df, xlabel='x', ylabel='y', alternative_hypothesis='less than',
        significance_level=0.05
    )
    print("========== end of scenario ==========")
    print()
    # scenario 3
    print("Scenario 3")
    print(
        "Is the average of sample one greater than the average of sample "
        "two?\n"
    )
    ds.two_sample_t(
        df=df, xlabel='x', ylabel='y', alternative_hypothesis='greater than',
        significance_level=0.05
    )
    print("========== end of scenario ==========")
    print()
    stop_time = time.perf_counter()
    ds.script_summary(
        script_path=Path(__file__),
        action='finished at'
    )
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
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


if __name__ == "__main__":
    main()
