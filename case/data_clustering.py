#!/usr/bin/env pythonw
# -*- coding: utf8 -*-

# %% Imports and constants

import hdbscan
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import cluster

from src.io_ops import load_sf_dataset, save_figure
from src.preprocess_for_ml import (
    preprocess_for_clustering,
    preprocess_for_clustering_coordinates_only,
)
from src.shared_ressources import logger

# %% supporting functions
def plot_cluster(df: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(9, 9))
    sns.scatterplot(
        data=df,
        x="longitude",
        y="latitude",
        hue="clst",
        ax=ax,
    )
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    return fig, ax


# %% Load the data, subsample for fast experimentation
df = load_sf_dataset()
sub = df.sample(35_000)

# %% Check for structure WITHOUT the coordinates... does crime label and timestamp correlate with an area? Spoiler: nope!
X = preprocess_for_clustering(sub).drop(["longitude", "latitude"], axis=1)
clf = cluster.AgglomerativeClustering(
    # manhattan distance becahse that's the relevant distance with this city planning
    linkage="complete",
    affinity="manhattan",
    n_clusters=5,
)
clst = clf.fit_predict(X)
sub["clst"] = clst
fig, ax = plot_cluster(sub)
save_figure(fig, "agglomrative_clustering_without_coordinates_visualize_coordinates")

# %% Make a version of X which includes the geographical information
X = preprocess_for_clustering(sub)
# %%  Use a density baserd clustering algorithm
clf = hdbscan.HDBSCAN(
    min_cluster_size=50, gen_min_span_tree=True, cluster_selection_epsilon=0.2
)
clst = clf.fit_predict(X)
sub["clst"] = clst
fig, ax = plot_cluster(sub)

# %%
for n_clusters in range(3, 8):
    clf = cluster.KMeans(n_clusters=n_clusters)
    clst = clf.fit_predict(X)
    sub["clst"] = clst
    fig, ax = plot_cluster(sub)
    save_figure(fig, f"kmeans_k_{n_clusters}_visualize_coordinates")

# %%
for n_clusters in range(3, 8):
    clf = cluster.AgglomerativeClustering(
        linkage="complete", affinity="manhattan", n_clusters=n_clusters
    )
    clst = clf.fit_predict(X)
    sub["clst"] = clst
    fig, ax = plot_cluster(sub)
    save_figure(
        fig, f"agglomerative_clustering_{n_clusters}_clusters_visualize_coordinates"
    )
