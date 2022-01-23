#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

# %% Imports and constants
import datetime

import hdbscan
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import cluster

from src.io_ops import load_sf_dataset
from src.preprocess_for_ml import (
    preprocess_for_clustering,
    preprocess_for_clustering_coordinates_only,
)
from src.shared_ressources import case_root
from src.shared_ressources import streamlit_keplergl_config as config
from src.shared_ressources import weekdays

# %%
df = load_sf_dataset()
# clusterer = hdbscan.HDBSCAN(
#     min_cluster_size=4, gen_min_span_tree=True, cluster_selection_epsilon=0.2
# )

# clusterer = cluster.AffinityPropagation(max_iter=200)
# clusterer = cluster.KMeans(4)

sub = df.sample(2500)
X = preprocess_for_clustering(sub).drop(["longitude", "latitude"], axis=1)
# X = preprocess_for_clustering_coordinates_only(sub).to_numpy()
# %%
clusterer = cluster.AgglomerativeClustering(
    linkage="complete", affinity="manhattan", n_clusters=5
)
clst = clusterer.fit_predict(X)
sub["clst"] = clst
set(clst)


# # %%
fig, ax = plt.subplots(figsize=(9, 9))
sns.scatterplot(
    data=sub,
    x="longitude",
    y="latitude",
    hue="clst",
    ax=ax,
    # palette=mpl.colormaps.get("Set3"),
)


# %%
# %%
# colors = np.array(list("rgbmcyk"))

color_palette = sns.color_palette("deep", 8)
cluster_colors = [
    color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in clusterer.labels_
]
cluster_member_colors = [
    sns.desaturate(x, p) for x, p in zip(cluster_colors, clusterer.probabilities_)
]
fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(
    *sub[["longitude", "latitude"]].to_numpy().T,
    s=10,
    linewidth=0,
    c=cluster_member_colors,
    alpha=0.75
)
