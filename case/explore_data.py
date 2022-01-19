#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

# %% Imports and constants
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.io_ops import load_sf_dataset, save_figure
from src.shared_ressources import case_root, weekdays

sns.set(context="paper", style="whitegrid", color_codes=True, font_scale=1.8)

pfa_red = "#990735"
# Make sure that the artifacts folder exists
artifacts = case_root / "artifacts"
try:
    artifacts.mkdir(exist_ok=True)
except PermissionError as err:
    raise PermissionError("Lacking permission to create artifacts folder") from err
except OSError as err:
    raise OSError("Can't create artifacts folder") from err
except Exception as err:
    raise err("Unhandled exception creating artifacts folder") from err

# %% Load data
df = load_sf_dataset()


# %% [markdown]
# ## Examine the data interactively

# %%
df.head()

# %% [markdown]
# Look for patterns wrt. time.
# This requires some enrichment of the data

# %%
df["time"] = df.datetime.dt.time
df["hour"] = df.datetime.dt.hour
# %%
ax = df.groupby(["weekday"]).category.count()[weekdays].plot.bar(color=pfa_red)
ax.set_ylabel("Number of arrests")
save_figure(ax, "arrests_by_weekday")
# %%
start_at_5_index = np.roll(np.arange(24), -5)
ax = df.groupby(["hour"]).category.count()[start_at_5_index].plot.bar(color=pfa_red)
ax.set_ylabel("Number of arrests")
save_figure(ax, "arrests_by_hour")
# %%
cnt = (
    df.groupby(["weekday", "hour"])
    .category.count()
    .unstack()
    .loc[weekdays, start_at_5_index]
)
ax = sns.heatmap(cnt)
save_figure(ax, "arrests_by_weekday_and_hour")
# %%
norm = df.category.value_counts()
cnt = (
    df.groupby(["category", "hour"])
    .description.count()
    .unstack()
    .loc[:, start_at_5_index]
    .divide(norm, axis="rows")
)
# Sort the rows for some resemblance of order
sidx = np.argsort((cnt ** 0.5).sum(axis=1).to_numpy())
cnt = cnt.iloc[sidx, :][::-1]

ax = sns.heatmap(cnt)
ax.set_ylabel("Arrest category")
save_figure(ax, "arrests_by_category_and_hour")

# %% [markdown]
# Examine the text-columns

# %% the "label" column
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
ax2.set_yscale("log")
for ax in (ax1, ax2):
    df.label.value_counts().plot.bar(ax=ax, color=pfa_red)
    ax.set_xlabel("Crime label")
ax1.set_ylabel("Count")
ax2.grid(which="minor")
save_figure(fig, "label_histogram")

# %% the "resolution" column
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
ax2.set_yscale("log")
for ax in (ax1, ax2):
    df.resolution.value_counts().plot.bar(ax=ax, color=pfa_red)
    ax.set_xlabel("Crime resolution")
ax1.set_ylabel("Count")
ax2.grid(which="minor")
save_figure(fig, "resolution_histogram")

# %% the "district" column
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
ax2.set_yscale("log")
for ax in (ax1, ax2):
    df.district.value_counts(dropna=False).plot.bar(ax=ax, color=pfa_red)
    ax.set_xlabel("Crime district")
ax1.set_ylabel("Count")
ax2.grid(which="minor")
save_figure(fig, "district_histogram")

# %%
