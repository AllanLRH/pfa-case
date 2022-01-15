#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt

# %% Imports and constants
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
import streamlit as st
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

from src.io_ops import load_sf_csv
from src.shared_ressources import case_root
from src.shared_ressources import streamlit_keplergl_config as config

st.set_page_config(layout="wide")

sns.set(context="paper", style="whitegrid", color_codes=True, font_scale=1.8)

# %% Load data
@st.cache()
def load_data(path):
    return load_sf_csv(path)


df = load_data(case_root / "data" / "sf_data.csv").sample(10_000)

# %% Filter the data
st.header("Crime incidents mapped")
st.text("Chose what you want to see")

col1, col2, col3, col4 = st.columns(4)
mask = np.ones_like(df["category"], dtype=bool)

with col1:
    options = [
        "larceny/theft",
        "other offenses",
        "non-criminal",
        "assault",
        "vehicle theft",
        "drug/narcotic",
        "vandalism",
        "warrants",
        "burglary",
        "suspicious occ",
        "robbery",
        "missing person",
        "fraud",
        "forgery/counterfeiting",
        "secondary codes",
        "weapon laws",
        "trespass",
        "prostitution",
        "stolen property",
        "disorderly conduct",
        "drunkenness",
        "sex offenses, forcible",
        "recovered vehicle",
        "driving under the influence",
        "kidnapping",
        "arson",
        "embezzlement",
        "liquor laws",
        "loitering",
        "suicide",
        "bad checks",
        "bribery",
        "extortion",
        "gambling",
        "pornography/obscene mat",
        "sex offenses, non forcible",
    ]
    selected_categories = st.multiselect("Category", options)
    if selected_categories:
        mask &= df["category"].isin(selected_categories)
with col2:
    filtered_keywords = (
        st.text_input("Search any of these words from the description field")
        .lower()
        .split()
    )
    mask_wordfilter = np.zeros_like(mask, dtype=bool)
    for word in filtered_keywords:
        mask_wordfilter |= df["description"].str.contains(word)
        mask &= mask_wordfilter
with col3:
    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    date_span = (df["datetime"].min().date(), df["datetime"].max().date())
    timestamps = df["datetime"].dt.time
    time_of_day_span = (
        datetime.time(hour=0, minute=0, second=0),
        datetime.time(hour=23, minute=59, second=59),
    )

    chosen_weekdays = st.multiselect("Select weekdays", weekdays)
    d_min, d_max = st.slider("Select date span", *date_span, value=date_span)
    t_min, t_max = st.slider(
        "Select time of day", *time_of_day_span, value=time_of_day_span
    )
    if chosen_weekdays:
        mask &= df["weekday"].isin(chosen_weekdays)
    mask &= (df.datetime >= pd.to_datetime(d_min)) & (
        df.datetime <= pd.to_datetime(d_max)
    )
    mask &= (df.datetime.dt.time >= t_min) & (df.datetime.dt.time <= t_max)
with col4:
    n_max_points = 100, 1_000, 5_000, 10_000, 25_000, 50_000, 100_000
    n_chosen = st.select_slider(
        "Select max number of points to show",
        n_max_points,
        value=10_000,
        format_func=lambda n: f"{n:,}",
    )
    if n_chosen < mask.sum():
        sub = df.loc[mask, :].sample(n_chosen)
    else:
        sub = df.loc[mask, :]


# %% Draw the map
sub["datetime"] = sub["datetime"].astype(str)
map_1 = KeplerGl(height=900, data={"Crimes": sub}, config=config)
keplergl_static(map_1, width=1200)
