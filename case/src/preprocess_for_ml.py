#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

# %% Imports and constants
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from prophet import Prophet
from sklearn import preprocessing, model_selection
from src.shared_ressources import case_root, seaborn_context, weekdays

sns.set(sns.set(**seaborn_context))

# %%


def convert_to_prophet_format(
    df: pd.DataFrame, time_rounding: str = "24h"
) -> pd.DataFrame:
    formatted_data = (
        df.groupby(df["datetime"].dt.round(time_rounding))["category"]
        .count()
        .rename("y")
        .rename_axis(index="ds")
        .reset_index()
    )
    return formatted_data


def preprocess_for_clustering_coordinates_only(df: pd.DataFrame) -> pd.DataFrame:
    """Simply apply a standard scaling to the coordinates"""
    cols = ["longitude", "latitude"]
    coords = df[cols]
    scaled = pd.DataFrame(
        preprocessing.StandardScaler().fit_transform(coords),
        columns=cols,
    )
    return scaled


def preprocess_for_clustering(df: pd.DataFrame) -> pd.DataFrame:
    X = df[["longitude", "latitude", "datetime", "category"]].reset_index()

    coords_scaled = preprocess_for_clustering_coordinates_only(df)

    total_seconds_offset = (
        (df.datetime - df.datetime.min()).dt.total_seconds().to_numpy()
    )
    n_seconds_a_day, n_seconds_a_week = 86_400, 604_800
    t_sin_daily = pd.Series(
        np.sin(2 * np.pi * total_seconds_offset / n_seconds_a_day), name="t_sin_daily"
    )
    t_cos_daily = pd.Series(
        np.cos(2 * np.pi * total_seconds_offset / n_seconds_a_day), name="t_cos_daily"
    )
    t_sin_weekly = pd.Series(
        np.sin(2 * np.pi * total_seconds_offset / n_seconds_a_week), name="t_sin_weekly"
    )
    t_cos_weekly = pd.Series(
        np.cos(2 * np.pi * total_seconds_offset / n_seconds_a_week), name="t_cos_weekly"
    )
    cat_dummies = pd.get_dummies(X["category"])
    transformed = pd.concat(
        [
            cat_dummies,
            coords_scaled,
            t_sin_daily,
            t_cos_daily,
            t_sin_weekly,
            t_cos_weekly,
        ],
        axis="columns",
    ).set_index(X.index)
    return transformed


if __name__ == "__main__":
    # This only runs if this file is executed as a script.
    # The code below is intended as debugging code / an explanation for the sine and cosine transform of the time variables
    fig, ax = plt.subplots(figsize=(12, 7))
    ss = np.arange(0, 24 * 3600)
    y1 = np.sin(2 * np.pi * ss / (24 * 3600))
    y2 = np.cos(2 * np.pi * ss / (24 * 3600))
    ax.plot(ss, y1, label="sin")
    ax.plot(ss, y2, label="cos")
    ax.legend()

# %%
