# %% Imports
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xgboost
from sklearn import model_selection, metrics

from src.io_ops import load_sf_dataset, save_figure
from src.shared_ressources import logger

# %% Load data and do basic data munging

df = (
    load_sf_dataset()
    .assign(
        hour=lambda x: x["datetime"].dt.hour,
        day_of_year=lambda x: x["datetime"].dt.day_of_year,
        day_of_week=lambda x: x["datetime"].dt.day_of_week,
        month_progress=lambda x: x["datetime"].dt.day / x["datetime"].dt.days_in_month,
        year=lambda x: x["datetime"].dt.year,
    )
    .drop(["district", "datetime", "description", "weekday"], axis=1)
    .reset_index(drop=True)
).sample(10_000)
# %% Let's try looking for these three targets
y_label = df.label == "violent"
y_resolution = df.resolution.str.contains("arrest")
y_category = df.category == "violent"
X = df.drop(["label", "resolution", "category"], axis=1)
del df  # save some memory

# %% Train holdout split
X_train, X_holdout, y_train, y_holdout = model_selection.train_test_split(
    X.to_numpy(), y_label.to_numpy(), test_size=0.3
)

# %% Fit it!

tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 100)

fig, ax = plt.subplots(figsize=(12, 7))
sfkf = model_selection.StratifiedKFold(n_splits=5)
for i, (train_idx, test_idx) in enumerate(sfkf.split(X_train, y_train)):
    X_tr, y_tr = X_train[train_idx], y_train[train_idx]
    X_te, y_te = X_train[test_idx], y_train[test_idx]
    clf = xgboost.XGBClassifier(
        use_label_encoder=False,
        objective="binary:logistic",
        eval_metric="auc",
        n_estimators=1500,
        max_depth=3,
        colsample_bytree=0.4,
    )
    clf.fit(X_tr, y_tr)
    p_tr, p_te = clf.predict_proba(X_tr)[:, 1], clf.predict_proba(X_te)[:, 1]
    roc_train = metrics.roc_auc_score(y_tr, p_tr)
    roc_test = metrics.roc_auc_score(y_te, p_te)
    print(f"{roc_train=}")
    print(f"{roc_test=}")
    viz = metrics.RocCurveDisplay.from_estimator(
        clf,
        X_te,
        y_te,
        name=f"ROC fold {i}",
        alpha=0.3,
        lw=1,
        ax=ax,
    )
    interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
    interp_tpr[0] = 0.0
    tprs.append(interp_tpr)
    aucs.append(viz.roc_auc)

# %%
