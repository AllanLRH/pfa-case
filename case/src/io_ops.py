import pandas as pd
from pathlib import Path
from src.shared_ressources import case_root, settings
import matplotlib as mpl
from typing import Union
from copy import deepcopy


def load_sf_dataset():

    # Ensure that the data exists on disk
    parquet_path = case_root / "data" / "sf_data.parquet"
    csv_path_crimes = case_root / "data" / "sf_data.csv"
    csv_path_districts = case_root / "data" / "sf_districts.csv"

    if not (
        (csv_path_crimes.exists() and csv_path_districts.exists())
        or parquet_path.exists(())
    ):
        raise FileNotFoundError(
            f"Can't find the data file under the name {parquet_path} or {csv_path_crimes}."
        )

    # Load parquet file of possible (fast), otherwise do the slow CSV parsing and data munging
    if parquet_path.exists():
        return pd.read_parquet(parquet_path)

    districts = pd.read_csv(csv_path_districts, sep=";", index_col="id")
    crimes = pd.read_csv(csv_path_crimes, sep=";", index_col="id").join(districts)

    crimes["datetime"] = pd.to_datetime(
        crimes.date.astype(str) + " " + crimes.time.astype(str), format="%m/%d/%Y %H:%M"
    )

    crimes = crimes.drop(["date", "time"], axis=1).sort_values(
        "datetime", ascending=True
    )

    if settings.cache_as_parquet_if_no_cached_file_exists:
        crimes.to_parquet(parquet_path)
    return crimes


def save_figure(
    fig_or_ax: Union[mpl.figure.Figure, mpl.axes.Axes],
    name: str,
    directory: Path = case_root / "artifacts",
    pdf: bool = True,
    png: bool = True,
    use_format_subfolders: bool = True,
    tight_layout: bool = True,
) -> None:
    def _do_the_saving(fig, name, directory, fileformat, use_format_subfolders) -> None:
        savedir = directory / fileformat if use_format_subfolders else directory
        savedir.mkdir(exist_ok=True)
        save_path = savedir / f"{name}.{fileformat}"
        fig.savefig(save_path)

    if not directory.exists() and directory.is_dir():
        raise FileNotFoundError(f"Output directory does not exist ({directory})")
    if not (pdf or png):
        raise ValueError(
            f"At least one of `pdf` or `png` must be `True`, but both evalueate to `False`({pdf=}, {png=})"
        )
    if isinstance(fig_or_ax, mpl.axes.Axes):
        fig = fig_or_ax.get_figure()
    elif isinstance(fig_or_ax, mpl.figure.Figure):
        fig = fig_or_ax
    else:
        raise ValueError(
            f"`fig_or_ax` must be a matplotlib Figure or Axis instance, but {type(fig_or_ax)=}"
        )
    if tight_layout:
        fig = deepcopy(fig)  # don't modify the original figure (sideeffect)
        fig.tight_layout()
    if pdf:
        _do_the_saving(fig, name, directory, "pdf", use_format_subfolders)
    if png:
        _do_the_saving(fig, name, directory, "png", use_format_subfolders)
