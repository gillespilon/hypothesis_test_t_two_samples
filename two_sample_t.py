#! /usr/bin/env python3
"""
Two-sample t test. Four scenarios.

Scenario 1
Is the average of sample one different from the average of sample two?

Scenario 2
Is the average of sample one less than the average of sample two?

Scenario 3
Is the average of sample one greater than the average of sample two?

Example of how a data file should look:
- first row is column labels: x y
- first column is sample number, must be integers: 1 2
- second column is data, int or float, no nan

    x   y
    1   30
    1   33
    1   37
    2   29
    2   31
    2   34

Requires datasense https://github.com/gillespilon/datasense
"""

from typing import IO, List, NoReturn, Tuple, Union
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
    xlabel = "x"
    ylabel = "y"
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
    validate_data(
        df=df, path_in=path_in, xlabel=xlabel, ylabel=ylabel,
        original_stdout=original_stdout, output_url=output_url
    )
    # scenario 1
    print("Scenario 1")
    print(
        "Is the average of sample one different from the average of sample "
        "two?\n"
    )
    ds.two_sample_t(
        df=df,
        xlabel=xlabel,
        ylabel=ylabel,
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
        xlabel=xlabel,
        ylabel=ylabel,
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
        xlabel=xlabel,
        ylabel=ylabel,
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
    """
    Helper function to request Path of data file and create DataFrame.

    Parameters
    ----------
    title : str
        The title for the GUI window.
    filetypes : List[Tuple[str, str]]
        The list of acceptable data file types.

    Returns
    -------
    df : pd.DataFrame
        The DataFrame of data.
    path_in : Path
        The Path of the input data file.
    """
    initialdir = Path(__file__).parent.resolve()
    path_in = ds.ask_open_file_name_path(
        title=title, initialdir=initialdir, filetypes=filetypes
    )
    df = ds.read_file(file_name=path_in)
    return (df, path_in)


def validate_data(
    df: pd.DataFrame,
    path_in: Union[Path, str],
    xlabel: str,
    ylabel: str,
    original_stdout: IO[str],
    output_url: str
) -> NoReturn:
    """
    Ensure that column x is integer.
    Ensure that column y is integer or float.
    Ensure there are no nans in columns x, y.
    Ensure that the lengths of columns x, y are the same.
    """
    # ensure column x is integer
    xlabel_type = df[xlabel].dtype
    if xlabel_type not in ['int64']:
        print("Data in xlabel column are not of type integer.")
        ds.exit_script(original_stdout=original_stdout, output_url=output_url)
    # ensure column y is integer or float
    ylabel_type = df[ylabel].dtype
    if ylabel_type not in ['int64', 'float64']:
        print("Data in ylabel column are not of type integer or float.")
        ds.exit_script(original_stdout=original_stdout, output_url=output_url)
    # ensure column x contains no nans
    count_x_nans = df[xlabel].isna().sum()
    if count_x_nans != 0:
        print(
            f"Column {xlabel} contains {count_x_nans} NaN. "
            "Fix this error or delete row(s)."
        )
        ds.exit_script(original_stdout=original_stdout, output_url=output_url)
    # ensure column y contains no nans
    count_y_nans = df[ylabel].isna().sum()
    if count_y_nans != 0:
        print(
            f"Column {ylabel} contains {count_y_nans} NaN. "
            "Fix this error or delete row(s)."
        )
        ds.exit_script(original_stdout=original_stdout, output_url=output_url)

if __name__ == "__main__":
    main()
