# %% Imports
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xgboost
from sklearn import model_selection, metrics
import pickle
from src.io_ops import load_sf_dataset, save_figure
from src.shared_ressources import logger, pfa_red, pfa_blue, seaborn_context, case_root

sns.set(**seaborn_context)

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
)
logger.info(f"Loaded dataset ({df.shape=}) with columns {df.columns}")
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


# Modified param grid, borrowed from here:
# https://gist.github.com/wrwr/3f6b66bf4ee01bf48be965f60d14454d
param_grid = {
    "max_depth": [3, 6, 8, 10],
    "learning_rate": [0.001, 0.01, 0.1, 0.2, 0, 3],
    "subsample": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "colsample_bytree": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "colsample_bylevel": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "min_child_weight": [0.5, 1.0, 3.0, 5.0, 7.0, 10.0],
    "gamma": [0, 0.25, 0.5, 1.0],
    "reg_lambda": [0.1, 1.0, 5.0, 10.0, 50.0, 100.0],
    "reg_alpha": [0.1, 1.0, 5.0, 10.0, 50.0, 100.0],
    "n_estimators": [100],
    "use_label_encoder": [False],
    "objective": ["binary:logistic"],
    "eval_metric": ["auc"],
}

# Paralellization happens on the hyerparameter search level, as it's an embarassingly parallel task.
# This minimizes the rather slow inter-thread communication which would otherwise occur in XGBoost.
clf = xgboost.XGBClassifier(n_jobs=1)
rs_clf = model_selection.RandomizedSearchCV(
    clf,
    param_grid,
    n_iter=20,
    n_jobs=4,
    verbose=2,
    cv=3,
    scoring="neg_log_loss",
    refit=True,
    random_state=42,
    return_train_score=True,
)

logger.info("Grid search started")
search_report = rs_clf.fit(X_train, y_train)
logger.info("Grid search done")
logger.debug(f"{rs_clf.best_params_=}")
logger.debug(f"{rs_clf.best_score_=}")
logger.debug(f"{rs_clf.best_estimator_=}")

clf = rs_clf.best_estimator_

# Save the estimator
best_estimator_save_path = (
    case_root / "artifacts" / "best_estimator_xgboost_violent_crime_prediction.pkl"
)
with best_estimator_save_path.open("bw") as fid:
    pickle.dump(clf, fid)

# %%
p_train = clf.predict_proba(X_train)[:, 1]
p_holdout = clf.predict_proba(X_holdout)[:, 1]

roc_train = metrics.roc_auc_score(y_train, p_train)
roc_holdout = metrics.roc_auc_score(y_holdout, p_holdout)

logger.info(f"{roc_train=}")
logger.info(f"{roc_holdout=}")

fig, ax = plt.subplots(figsize=(5.5, 5.5))
viz = metrics.RocCurveDisplay.from_estimator(
    clf,
    X_train,
    y_train,
    name=f"ROC train",
    ax=ax,
    color=pfa_red,
)

viz = metrics.RocCurveDisplay.from_estimator(
    clf,
    X_holdout,
    y_holdout,
    name=f"ROC holdout",
    ax=ax,
    color=pfa_blue,
)
# xlim, ylim = ax.get_xlim(), ax.get_ylim()
ax.plot([-0.1, 1.1], [-0.1, 1.1], "k--", lw=1.5)
# ax.set_xlim(xlim), ax.set_ylim(ylim)
ax.set_xlim([0, 1]), ax.set_ylim([0, 1])
save_figure(fig, "roc_curve_crime_violent_prediction")

# %%
