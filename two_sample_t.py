#! /usr/bin/env python3
"""
Two-sample t test. Three scenarios.

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

Validate the data set for dtypes, NaNs, and length.

Check assumptions of normality, homogeneity of variance using parametric
and non-parametric methods.

Requires:
- datasense https://github.com/gillespilon/datasense
- Python 3.10 minimum
"""

from typing import IO, List, NoReturn, Tuple, Union
from pathlib import Path
import time

import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd


def main():
    start_time = time.perf_counter()
    # define parameters
    filetypes = [("csv and feather files", ".csv .CSV .feather .FEATHER")]
    path_in_title = "Select csv or feather file to read"
    colour_one = "#0077bb"
    output_url = "two_sample_t_test.html"
    header_title = "Two-sample t test"
    header_id = "two-sample-t-test"
    xlabel, ylabel = "x", "y"
    original_stdout = ds.html_begin(
        output_url=output_url, header_title=header_title, header_id=header_id
    )
    ds.script_summary(script_path=Path(__file__), action="started at")
    ds.style_graph()
    # create DataFrames
    df, path_in = create_dataframe(title=path_in_title, filetypes=filetypes)
    y_sample_one = df["y"][df["x"] == 1]
    y_sample_two = df["y"][df["x"] == 2]
    print("Data file", path_in)
    print()
    validate_data(
        df=df,
        path_in=path_in,
        xlabel=xlabel,
        ylabel=ylabel,
        original_stdout=original_stdout,
        output_url=output_url,
    )
    # scenario 1
    print("Scenario 1")
    print(
        "Is the average of sample one different from the average of sample "
        "two?"
    )
    print()
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
    print("Is the average of sample one less than the average of sample two?")
    print()
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
        "two?"
    )
    print()
    ds.two_sample_t(
        df=df,
        xlabel=xlabel,
        ylabel=ylabel,
        alternative_hypothesis="greater than",
        significance_level=0.05,
    )
    print("========== end of scenario ==========")
    print()
    # histogram sample one
    fig, ax = ds.plot_histogram(
        series=y_sample_one, number_bins=16, bin_range=(28, 44), bin_width=1
    )
    ax.set_xlabel("Y (units)")
    ax.set_ylabel("Count")
    ax.set_title(label="Histogram of sample one")
    fig.savefig(fname="histogram_sample_one.svg", format="svg")
    ds.html_figure(
        file_name="histogram_sample_one.svg",
        caption="histogram_sample_one.svg"
    )
    # histogram sample two
    fig, ax = ds.plot_histogram(
        series=y_sample_two, number_bins=16, bin_range=(28, 44), bin_width=1
    )
    ax.set_xlabel("Y (units)")
    ax.set_ylabel("Count")
    ax.set_title(label="Histogram of sample two")
    fig.savefig(fname="histogram_sample_two.svg", format="svg")
    ds.html_figure(
        file_name="histogram_sample_two.svg",
        caption="histogram_sample_two.svg"
    )
    # two row, one column histograms sample one, sample two
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
    mid = (fig.subplotpars.right + fig.subplotpars.left) / 2
    fig.suptitle(t="Histograms", x=mid)
    ax1.hist(x=y_sample_one, bins=16)
    ax1.set_title(label="Sample one")
    ax1.set_ylabel("Count")
    ax2.hist(x=y_sample_two, bins=16)
    ax2.set_title(label="Sample two")
    ax2.set_xlabel("Y (units)")
    ax2.set_ylabel("Count")
    ds.despine(ax=ax1)
    ds.despine(ax=ax2)
    fig.savefig(fname="histograms_sample_one_sample_two.svg", format="svg")
    ds.html_figure(
        file_name="histograms_sample_one_sample_two.svg",
        caption="histograms_sample_one_sample_two.svg"
    )
    # box and whisker plot sample one
    fig, ax = ds.plot_boxplot(series=y_sample_one, notch=True, showmeans=True)
    ax.set_title(label="Box and whisker plot\nSample one")
    ax.set_xticks(ticks=[1], labels=["Sample one"])
    ax.set_ylabel("Y (units)")
    fig.savefig(fname="box_and_whisker_sample_one.svg", format="svg")
    ds.html_figure(
        file_name="box_and_whisker_sample_one.svg",
        caption="box_and_whisker_sample_one.svg"
    )
    # box and whisker plot sample two
    fig, ax = ds.plot_boxplot(series=y_sample_two, notch=True, showmeans=True)
    ax.set_title(label="Box and whisker plot\nSample two")
    ax.set_xticks(ticks=[1], labels=["Sample two"])
    ax.set_ylabel("Y (units)")
    fig.savefig(fname="box_and_whisker_sample_two.svg", format="svg")
    ds.html_figure(
        file_name="box_and_whisker_sample_two.svg",
        caption="box_and_whisker_sample_two.svg"
    )
    # one row, two column box and whisker plots sample one, sample two
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
    ax1.boxplot(x=y_sample_one, notch=True, showmeans=True)
    ax2.boxplot(x=y_sample_two, notch=True, showmeans=True)
    ax1.set_xticks(ticks=[1], labels=["Sample one"])
    ax2.set_xticks(ticks=[1], labels=["Sample two"])
    ax1.set_title(label="Sample one")
    ax2.set_title(label="Sample two")
    ax1.set_ylabel("Y (units)")
    mid = (fig.subplotpars.right + fig.subplotpars.left) / 2
    fig.suptitle(t="Box-and-whisker plots", x=mid)
    ds.despine(ax=ax1)
    ds.despine(ax=ax2)
    fig.savefig(
        fname="box_and_whiskers_sample_one_sample_two.svg", format="svg"
    )
    ds.html_figure(
        file_name="box_and_whiskers_sample_one_sample_two.svg",
        caption="box_and_whiskers_sample_one_sample_two.svg"
    )
    # scatter plot sample one
    fig, ax = ds.plot_scatter_y(y=y_sample_one)
    ax.set_title(label="Scatter plot\nSample one")
    ax.set_xlabel("X (Sample order)")
    ax.set_ylabel("Y (units)")
    fig.savefig(fname="scatter_sample_one.svg", format="svg")
    ds.html_figure(
        file_name="scatter_sample_one.svg",
        caption="scatter_sample_one.svg"
    )
    # scatter plot sample two
    fig, ax = ds.plot_scatter_y(y=y_sample_two)
    ax.set_title(label="Scatter plot\nSample two")
    ax.set_xlabel("X (Sample order)")
    ax.set_ylabel("Y (units)")
    fig.savefig(fname="scatter_sample_two.svg", format="svg")
    ds.html_figure(
        file_name="scatter_sample_two.svg",
        caption="scatter_sample_two.svg"
    )
    # one row, two column scatter plots sample one, sample two
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
    ax1.plot(
        y_sample_one, marker=".", markersize=8, linestyle="None",
        color=colour_one
    )
    fig.suptitle(t="Scatter plots")
    ax1.set_title(label="Sample one")
    ax1.set_ylabel(ylabel="Y (units)")
    ax1.set_xlabel(
        xlabel="X (Sample order)"
        )
    ax2.plot(
        y_sample_two, marker=".", markersize=8, linestyle="None",
        color=colour_one
    )
    ax2.set_xlabel(xlabel="X (Sample order)")
    ax2.set_title(label="Sample two")
    ds.despine(ax=ax1)
    ds.despine(ax=ax2)
    fig.savefig(fname="scatter_sample_one_sample_two.svg", format="svg")
    ds.html_figure(
        file_name="scatter_sample_one_sample_two.svg",
        caption="scatter_sample_one_sample_two.svg"
    )
    # normal probability plot sample one
    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig, ax = ds.probability_plot(data=y_sample_one, plot=ax)
    ax.set_title(label="Normal Probability Plot\nSample one")
    ax.set_xlabel(xlabel="Theoretical Quantiles")
    fig.savefig(fname="normal_probability_plot_sample_one.svg", format="svg")
    ds.html_figure(
        file_name="normal_probability_plot_sample_one.svg",
        caption="normal_probability_plot_sample_one.svg"
    )
    # normal probability plot sample two
    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig, ax = ds.probability_plot(data=y_sample_two, plot=ax)
    ax.set_title(label="Normal Probability Plot\nSample two")
    ax.set_xlabel(xlabel="Theoretical Quantiles")
    fig.savefig(fname="normal_probability_plot_sample_two.svg", format="svg")
    ds.html_figure(
        file_name="normal_probability_plot_sample_two.svg",
        caption="normal_probability_plot_sample_two.svg"
    )
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

    Example
    -------
    >>> df, path_in = create_dataframe(
    >>>     title=path_in_title, filetypes=filetypes
    >>> )
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
    output_url: str,
) -> NoReturn:
    """
    Ensure that column x is integer.
    Ensure that column y is integer or float.
    Ensure there are no nans in columns x, y.
    Ensure that the lengths of columns x, y are the same.

    Parameters
    ----------
    df : pd.DataFrame,
        The DataFrame to validate.
    path_in : Union[Path, str],
        The Path of the input file.
    xlabel : str,
        The column label of the column with the sample identifications.
    ylabel : str,
        The column label of the column with the sample data.
    original_stdout : IO[str],
        A file object for the output of print().
    output_url : str,

    Example
    -------
    >>> validate_data(
    >>>     df=df,
    >>>     path_in=path_in,
    >>>     xlabel=xlabel,
    >>>     original_stdout=original_stdout,
    >>>     output_url=output_url,
    >>> )
    >>>     ylabel=ylabel,
    """
    # ensure column x is integer
    xlabel_type = df[xlabel].dtype
    if xlabel_type not in ["int64"]:
        print("Data in xlabel column are not of type integer.")
        ds.exit_script(original_stdout=original_stdout, output_url=output_url)
    # ensure column y is integer or float
    ylabel_type = df[ylabel].dtype
    if ylabel_type not in ["int64", "float64"]:
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
    # ensure columns x, y are of the same length
    length_x = df[xlabel].notnull().sum()
    length_y = df[ylabel].notnull().sum()
    if length_x != length_y:
        print(f"Columns {xlabel} and {ylabel} are not of the same length.")
        ds.exit_script(original_stdout=original_stdout, output_url=output_url)


if __name__ == "__main__":
    main()
