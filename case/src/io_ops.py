import pandas as pd

from src.shared_ressources import case_root


def load_sf_dataset(cache_as_parquet_if_no_cached_file_exists: bool = True):
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
    crimes = crimes.drop(["date", "time"], axis=1)
    if cache_as_parquet_if_no_cached_file_exists:
        crimes.to_parquet(parquet_path)
    return crimes
