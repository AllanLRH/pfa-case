#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

# %% Imports and constants
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.io_ops import load_sf_dataset
from src.shared_ressources import case_root, weekdays

sns.set(context="paper", style="whitegrid", color_codes=True, font_scale=1.8)

# %% Load data
df = load_sf_dataset()

# %% Make sure that the artifacts folder exists
artifacts = case_root / "artifacts"
try:
    artifacts.mkdir(exist_ok=True)
except PermissionError as err:
    raise PermissionError("Lacking permission to create artifacts folder") from err
except OSError as err:
    raise OSError("Can't create artifacts folder") from err
except Exception as err:
    raise err("Unhandled exception creating artifacts folder") from err


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
df.groupby(["weekday"]).category.count()[weekdays].plot.bar()
# %%
start_at_5_index = np.roll(np.arange(24), -5)
df.groupby(["hour"]).category.count()[start_at_5_index].plot.bar()
# %%
cnt = (
    df.groupby(["weekday", "hour"])
    .category.count()
    .unstack()
    .loc[weekdays, start_at_5_index]
)
sns.heatmap(cnt)
# %%
norm = df.category.value_counts()
cnt = (
    df.groupby(["category", "hour"])
    .description.count()
    .unstack()
    .loc[:, start_at_5_index]
)
# sns.heatmap(cnt)

# %%
