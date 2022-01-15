#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

# %% Imports and constants
import numpy as np
import matplotlib as mpl
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from typing import Union
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


class PrettyKey:
    def __init__(self, key: str, count: int) -> None:
        self.key = key
        self.count = count

    def __str__(self) -> str:
        return f"{self.key} ({self.count})"

    def __lt__(self, other) -> bool:
        return self.count < other.count


col1, col2, col3 = st.columns(3)
mask = np.ones_like(df["category"], dtype=bool)

with col1:
    options = sorted(
        (PrettyKey(k, v) for (k, v) in df["category"].value_counts().iteritems()),
        reverse=True,
    )
    selected_categories = [el.key for el in st.multiselect("Category", options)]
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

map_1 = KeplerGl(height=900, data={"Crimes": sub}, config=config)
keplergl_static(map_1, width=1200)
