#! /usr/bin/env python3
"""
Two-sample t test. Four scenarios.

Scenario 1
Is the average of sample one different from the average of sample two?

Scenario 2
Is the average of sample one less than the average of sample two?

Scenario 3
Is the average of sample one greater than the average of sample two?

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
    ds.script_summary(script_path=Path(__file__), action="started at")
    # create DataFrames
    # df, sample_one, sample_two = create_dataframe_examples()
    df, path_in = create_dataframe(title=path_in_title, filetypes=filetypes)
    print("Data file", path_in)
    print()
    start_time = time.perf_counter()
    # scenario 1
    print("Scenario 1")
    print(
        "Is the average of sample one different from the average of sample "
        "two?\n"
    )
    ds.two_sample_t(
        df=df,
        xlabel="x",
        ylabel="y",
        alternative_hypothesis="unequal",
        significance_level=0.05,
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
        df=df,
        xlabel="x",
        ylabel="y",
        alternative_hypothesis="less than",
        significance_level=0.05,
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
        df=df,
        xlabel="x",
        ylabel="y",
        alternative_hypothesis="greater than",
        significance_level=0.05,
    )
    print("========== end of scenario ==========")
    print()
    stop_time = time.perf_counter()
    ds.script_summary(script_path=Path(__file__), action="finished at")
    ds.report_summary(start_time=start_time, stop_time=stop_time)
    ds.html_end(original_stdout=original_stdout, output_url=output_url)


def create_dataframe(
    title: str, filetypes: List[Tuple[str, str]]
) -> Tuple[pd.DataFrame, Path]:
    initialdir = Path(__file__).parent.resolve()
    path_in = ds.ask_open_file_name_path(
        title=title, initialdir=initialdir, filetypes=filetypes
    )
    df = ds.read_file(file_name=path_in)
    return (df, path_in)


if __name__ == "__main__":
    main()
