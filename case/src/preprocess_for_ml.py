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
