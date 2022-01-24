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

from src.shared_ressources import seaborn_context
from src.preprocess_for_ml import convert_to_prophet_format
from src.io_ops import load_sf_dataset, save_figure
from src.shared_ressources import logger, pfa_red, case_root

sns.set(sns.set(**seaborn_context))

# %% Load and preprocess data into a the format expected by Probhet
# %% Load and preprocess data into a the format expected by Prophet

df = load_sf_dataset()
formatted_data = convert_to_prophet_format(df, time_rounding="4h")
formatted_data.head()

# %% Split into training and testing dataset
n_test = len(formatted_data) // 10
logger.info(
    f"{n_test} data points set aside for a test dataset out of {len(formatted_data)} data points"
)
data_train, data_test = (
    formatted_data.iloc[n_test:, :],
    formatted_data.iloc[-n_test:, :],
)

logger.debug(f"{data_train.shape=}, {data_test.shape=}")
# save some precious memory, since this is a script and thus won't be garbage
# collected for the programs remaining lifetime
del formatted_data

# %% Predict overall crime using Prophet
m = Prophet()
m.add_country_holidays(country_name="US")
m.fit(data_train)

# %% Evalueate fit visually
forecast = m.predict(data_test[["ds"]])
forecast["y"] = data_test["y"].reset_index(drop=True)

pf1 = plot_plotly(m, forecast)
pf2 = plot_components_plotly(m, forecast)
pf1.write_html(case_root / "artifacts" / "prophet_forecast.html")
pf2.write_html(case_root / "artifacts" / "prophet_forecast_components.html")
pf1.show()
pf2.show()
# %% Same plots as above, but made in Matplotlib for export
prophet_crime_forecast = m.plot(forecast)
prophet_crime_forecast.gca().get_lines()[1].set_color(pfa_red)
save_figure(prophet_crime_forecast, "prophet_crime_forecast")

prophet_crime_forecast_components = m.plot_components(forecast, figsize=(8, 18))
for ax in prophet_crime_forecast_components.axes:
    ax.get_lines()[0].set_color(pfa_red)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=12)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
    ax.set_title("")
prophet_crime_forecast_components.tight_layout()
save_figure(prophet_crime_forecast_components, "prophet_crime_forecast_components")

# %%
