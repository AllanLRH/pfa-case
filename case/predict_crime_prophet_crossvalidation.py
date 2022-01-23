#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

# %% Imports and constants

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from prophet import Prophet
from prophet.plot import plot_components_plotly, plot_plotly
from prophet.diagnostics import cross_validation, performance_metrics


from src.shared_ressources import seaborn_context
from src.preprocess_for_ml import convert_to_prophet_format
from src.io_ops import load_sf_dataset, save_figure
from src.shared_ressources import logger, pfa_red

sns.set(sns.set(**seaborn_context))

# %% Load and preprocess data into a the format expected by Probhet
# %% Load and preprocess data into a the format expected by Prophet

df = load_sf_dataset()
formatted_data = convert_to_prophet_format(df, time_rounding="4h")
formatted_data.head()

# %% Split into training and testing dataset
cutoff_point = pd.Timestamp("2017-01-03 12:00:00")
logger.info(f"Data after {cutoff_point} is set aside for a test dataset")
train_mask = formatted_data.ds <= cutoff_point
data_train, data_test = (
    formatted_data.loc[train_mask, :],
    formatted_data.loc[~train_mask, :],
)

logger.debug(f"{data_train.shape=}, {data_test.shape=}")

# %% Predict overall crime using Prophet
m = Prophet()
m.add_country_holidays(country_name="US")
m.fit(data_train)

# %%
forecast = pd.concat(
    [m.predict(formatted_data[["ds"]]), formatted_data["y"].reset_index(drop=True)],
    axis="columns",
)
forecast.loc[train_mask, "train_or_test"] = "train"
forecast.loc[~train_mask, "train_or_test"] = "test"
forecast.head()
# %%
forecast["rse"] = np.sqrt((forecast.yhat - forecast.y) ** 2)
fig, ax = plt.subplots(figsize=(12, 7))
forecast.query("train_or_test == 'train'").rse.plot(
    ax=ax, color="k", label="Root Square Error, Training data"
)
forecast.query("train_or_test == 'test'").rse.plot(
    ax=ax, color=pfa_red, label="Root Square Error, Test data"
)
# ax.axhline(forecast.rse.mean(), color="b")
(forecast.rse.cumsum() / np.arange(1, len(forecast) + 1)).plot(
    color="yellow", label="Running RMSE"
)
ax.legend()
save_figure(fig, "rmse_prophet_all_crime_4h_binning")

# %%
