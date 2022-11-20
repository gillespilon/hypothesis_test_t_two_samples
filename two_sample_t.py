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

from pathlib import Path
import time

import matplotlib.pyplot as plt
import datasense as ds
import pandas as pd


def main():
    filetypes = [("csv and feather files", ".csv .CSV .feather .FEATHER")]
    path_in_title = "Select csv or feather file to read"
    initialdir = Path(__file__).parent.resolve()
    output_url = "two_sample_t.html"
    header_title = "Two-sample t test"
    header_id = "two-sample-t-test"
    significance_level = 0.05
    colour = "#0077bb"
    decimals = 16
    width = 7
    # path_in = ds.ask_open_file_name_path(
    #     title=path_in_title,
    #     initialdir=initialdir,
    #     filetypes=filetypes
    # )
    start_time = time.perf_counter()
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    ds.script_summary(
        script_path=Path(__file__),
        action="started at"
    )
    ds.style_graph()
    series1 = pd.Series(
        data=[32, 37, 35, 28, 41, 44, 35, 31, 34, 38, 42],
        name="y1"
    )
    series2 = pd.Series(
        data=[36, 31, 30, 31, 34, 36, 29, 32, 31],
        name="y2"
    )
    # print("Data file", path_in)
    # print()
    # df = ds.read_file(file_name=path_in)
    # series1 = df[df.columns[0]].dropna()
    # series2 = df[df.columns[1]].dropna()
    levels = [1, 2]
    for level in levels:
        if level == 1:
            series = series1
        else:
            series = series2
        parametric_statistics = ds.parametric_summary(
            series=series,
            decimals=decimals
        ).to_string()
        print(f"Parametric statistics for y level {level}")
        print(parametric_statistics)
        print()
    for level in levels:
        if level == 1:
            series = series1
        else:
            series = series2
        nonparametric_statistics = ds.nonparametric_summary(
            series=series,
            alphap=1/3,
            betap=1/3,
            decimals=decimals
        ).to_string()
        print(f"Non-parametric statistics for y level {level}")
        print(nonparametric_statistics)
        print()
    print("Scenario 1")
    print(
        "Is the average of sample one different from the average of sample "
        "two?"
    )
    print()
    ds.two_sample_t(
        series1=series1,
        series2=series2,
        alternative_hypothesis="two-sided",
        significance_level=significance_level,
        width=width,
        decimals=decimals
    )
    print("Scenario 2")
    print("Is the average of sample one less than the average of sample two?")
    print()
    ds.two_sample_t(
        series1=series1,
        series2=series2,
        alternative_hypothesis="less",
        significance_level=significance_level,
        width=width,
        decimals=decimals
    )
    print("Scenario 3")
    print(
        "Is the average of sample one greater than the average of sample "
        "two?"
    )
    print()
    ds.two_sample_t(
        series1=series1,
        series2=series2,
        alternative_hypothesis="greater",
        significance_level=significance_level,
        width=width,
        decimals=decimals
    )
    fig, ax = ds.plot_histogram(series=series1)
    ax.set_xlabel("Y (units)")
    ax.set_ylabel("Count")
    ax.set_title(label="Histogram of sample one")
    fig.savefig(
        fname="histogram_sample_one.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="histogram_sample_one.svg",
        caption="histogram_sample_one.svg"
    )
    fig, ax = ds.plot_histogram(series=series2)
    ax.set_xlabel("Y (units)")
    ax.set_ylabel("Count")
    ax.set_title(label="Histogram of sample two")
    fig.savefig(
        fname="histogram_sample_two.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="histogram_sample_two.svg",
        caption="histogram_sample_two.svg"
    )
    # two row, one column histograms sample one, sample two
    fig, (ax1, ax2) = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        sharey=True
    )
    mid = (fig.subplotpars.right + fig.subplotpars.left) / 2
    fig.suptitle(t="Histograms", x=mid)
    # ax1.hist(x=series1, bins=16)
    ax1.hist(x=series1)
    ax1.set_title(label="Sample one")
    ax1.set_ylabel("Count")
    # ax2.hist(x=series2, bins=16)
    ax2.hist(x=series2)
    ax2.set_title(label="Sample two")
    ax2.set_xlabel("Y (units)")
    ax2.set_ylabel("Count")
    ds.despine(ax=ax1)
    ds.despine(ax=ax2)
    fig.savefig(
        fname="histograms_sample_one_sample_two.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="histograms_sample_one_sample_two.svg",
        caption="histograms_sample_one_sample_two.svg"
    )
    # box and whisker plot sample one
    fig, ax = ds.plot_boxplot(
        series=series1,
        notch=True,
        showmeans=True
    )
    ax.set_title(label="Box and whisker plot\nSample one")
    ax.set_xticks(
        ticks=[1],
        labels=["Sample one"]
    )
    ax.set_ylabel("Y (units)")
    fig.savefig(
        fname="box_and_whisker_sample_one.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="box_and_whisker_sample_one.svg",
        caption="box_and_whisker_sample_one.svg"
    )
    # box and whisker plot sample two
    fig, ax = ds.plot_boxplot(
        series=series2,
        notch=True,
        showmeans=True
    )
    ax.set_title(label="Box and whisker plot\nSample two")
    ax.set_xticks(
        ticks=[1],
        labels=["Sample two"]
    )
    ax.set_ylabel("Y (units)")
    fig.savefig(
        fname="box_and_whisker_sample_two.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="box_and_whisker_sample_two.svg",
        caption="box_and_whisker_sample_two.svg"
    )
    # one row, two column box and whisker plots sample one, sample two
    fig, (ax1, ax2) = plt.subplots(
        nrows=1,
        ncols=2,
        sharey=True
    )
    ax1.boxplot(
        x=series1,
        notch=True,
        showmeans=True
    )
    ax2.boxplot(
        x=series2,
        notch=True,
        showmeans=True
    )
    ax1.set_xticks(
        ticks=[1],
        labels=["Sample one"]
    )
    ax2.set_xticks(
        ticks=[1],
        labels=["Sample two"]
    )
    ax1.set_title(label="Sample one")
    ax2.set_title(label="Sample two")
    ax1.set_ylabel("Y (units)")
    mid = (fig.subplotpars.right + fig.subplotpars.left) / 2
    fig.suptitle(
        t="Box-and-whisker plots",
        x=mid
    )
    ds.despine(ax=ax1)
    ds.despine(ax=ax2)
    fig.savefig(
        fname="box_and_whiskers_sample_one_sample_two.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="box_and_whiskers_sample_one_sample_two.svg",
        caption="box_and_whiskers_sample_one_sample_two.svg"
    )
    # scatter plot sample one
    fig, ax = ds.plot_scatter_y(y=series1)
    ax.set_title(label="Scatter plot\nSample one")
    ax.set_xlabel("X (Sample order)")
    ax.set_ylabel("Y (units)")
    fig.savefig(
        fname="scatter_sample_one.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="scatter_sample_one.svg",
        caption="scatter_sample_one.svg"
    )
    # scatter plot sample two
    fig, ax = ds.plot_scatter_y(y=series2)
    ax.set_title(label="Scatter plot\nSample two")
    ax.set_xlabel("X (Sample order)")
    ax.set_ylabel("Y (units)")
    fig.savefig(
        fname="scatter_sample_two.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="scatter_sample_two.svg",
        caption="scatter_sample_two.svg"
    )
    # one row, two column scatter plots sample one, sample two
    fig, (ax1, ax2) = plt.subplots(
        nrows=1,
        ncols=2,
        sharex=True,
        sharey=True
    )
    ax1.plot(
        series1,
        marker=".",
        markersize=8,
        linestyle="None",
        color=colour
    )
    fig.suptitle(t="Scatter plots")
    ax1.set_title(label="Sample one")
    ax1.set_ylabel(ylabel="Y (units)")
    ax1.set_xlabel(
        xlabel="X (Sample order)"
        )
    ax2.plot(
        series2,
        marker=".",
        markersize=8,
        linestyle="None",
        color=colour
    )
    ax2.set_xlabel(xlabel="X (Sample order)")
    ax2.set_title(label="Sample two")
    ds.despine(ax=ax1)
    ds.despine(ax=ax2)
    fig.savefig(
        fname="scatter_sample_one_sample_two.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="scatter_sample_one_sample_two.svg",
        caption="scatter_sample_one_sample_two.svg"
    )
    # normal probability plot sample one
    fig, ax = ds.probability_plot(
        data=series1,
        plot=ax
    )
    ax.set_title(label="Normal Probability Plot\nSample one")
    ax.set_xlabel(xlabel="Theoretical Quantiles")
    fig.savefig(
        fname="normal_probability_plot_sample_one.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="normal_probability_plot_sample_one.svg",
        caption="normal_probability_plot_sample_one.svg"
    )
    # normal probability plot sample two
    fig, ax = ds.probability_plot(
        data=series2,
        plot=ax
    )
    ax.set_title(label="Normal Probability Plot\nSample two")
    ax.set_xlabel(xlabel="Theoretical Quantiles")
    fig.savefig(
        fname="normal_probability_plot_sample_two.svg",
        format="svg"
    )
    ds.html_figure(
        file_name="normal_probability_plot_sample_two.svg",
        caption="normal_probability_plot_sample_two.svg"
    )
    stop_time = time.perf_counter()
    ds.script_summary(
        script_path=Path(__file__),
        action="finished at"
    )
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == "__main__":
    main()
