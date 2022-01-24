#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

# %% Imports and constants
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.io_ops import load_sf_dataset, save_figure
from src.shared_ressources import case_root, weekdays, seaborn_context, pfa_red

sns.set(**seaborn_context)


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
df["day_of_year"] = df.datetime.dt.day_of_year
df["year"] = df.datetime.dt.year
df["day_of_month"] = df.datetime.dt.day
df["month_progress"] = df.datetime.dt.day / df.datetime.dt.days_in_month
# %%
ax = df.groupby(["weekday"]).category.count()[weekdays].plot.bar(color=pfa_red)
ax.set_ylabel("Number of arrests")
plt.tight_layout()
save_figure(ax, "arrests_by_weekday")
# %%
start_at_5_index = np.roll(np.arange(24), -5)
ax = df.groupby(["hour"]).category.count()[start_at_5_index].plot.bar(color=pfa_red)
ax.set_ylabel("Number of arrests")
plt.tight_layout()
save_figure(ax, "arrests_by_hour")
# %%
cnt = (
    df.groupby(["weekday", "hour"])
    .category.count()
    .unstack()
    .loc[weekdays, start_at_5_index]
)
ax = sns.heatmap(cnt)
plt.tight_layout()
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
plt.tight_layout()
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
plt.tight_layout()
save_figure(fig, "label_histogram")

# %% the "resolution" column
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
ax2.set_yscale("log")
for ax in (ax1, ax2):
    df.resolution.value_counts().plot.bar(ax=ax, color=pfa_red)
    ax.set_xlabel("Crime resolution")
ax1.set_ylabel("Count")
ax2.grid(which="minor")
plt.tight_layout()
save_figure(fig, "resolution_histogram")

# %% the "district" column
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
ax2.set_yscale("log")
for ax in (ax1, ax2):
    df.district.value_counts(dropna=False).plot.bar(ax=ax, color=pfa_red)
    ax.set_xlabel("Crime district")
ax1.set_ylabel("Count")
ax2.grid(which="minor")
plt.tight_layout()
save_figure(fig, "district_histogram")

# %% [markdown]
# ## Examine the yearly trend, weekly trend ect.


# %% Activity at each day of each year
fig, ax = plt.subplots(figsize=(9, 4.5))
activity_year_round = (
    df.groupby(["year", "day_of_year"])["datetime"]
    .count()
    .rename("n_observations")
    .reset_index()
)
activity_year_round.loc[:, "n_observations"] += (
    activity_year_round.year.max() - activity_year_round.year
) * 200
sns.lineplot(
    data=activity_year_round,
    x="day_of_year",
    y="n_observations",
    hue="year",
    legend="full",
    ax=ax,
)
# The yticks are meaningless, so get rid of them
ax.set_yticklabels([])

# Put the legend outside the main plot area
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
save_figure(ax, "observations_by_day_of_year_for_each_year")

# %% Activity at each day og each year
fig, ax = plt.subplots(figsize=(9, 4.5))
activity_year_round = (
    df.groupby(["day_of_month"])["datetime"]
    .count()
    .rename("n_observations")
    .reset_index()
)
sns.barplot(
    data=activity_year_round,
    x="day_of_month",
    y="n_observations",
    color=pfa_red,
    ax=ax,
)
# The yticks are meaningless, so get rid of them
ax.set_yticklabels([])

# Put the legend outside the main plot area
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
save_figure(ax, "observations_by_day_of_month")
# %%
