import pandas as pd

from src.shared_ressources import case_root


def load_sf_dataset():
    # Ensure that the data exists on disk
    parquet_path = case_root / "data" / "sf_data.parquet"
    csv_path = case_root / "data" / "sf_data.csv"
    if not (csv_path.exists() or parquet_path.exists(())):
        raise FileNotFoundError(
            f"Can't find the data file under the name {parquet_path} or {csv_path}."
        )
    # Load parquet file of possible (fast), otherwise do the slow CSV parsing and data munging
    if parquet_path.exists():
        return pd.read_parquet(parquet_path)
    df = pd.read_csv(csv_path, sep=";", index_col="id")
    df["datetime"] = pd.to_datetime(
        df.date.astype(str) + " " + df.time.astype(str), format="%m/%d/%Y %H:%M"
    )
    df = df.drop(["date", "time"], axis=1)
    return df
