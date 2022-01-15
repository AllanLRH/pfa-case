import pandas as pd
from dateutil.parser import parse as dtparse
import pathlib


def load_sf_csv(path: pathlib.Path):
    if not path:
        raise FileNotFoundError(f"Can't find the data file {path.absolute()}")
    df = pd.read_csv(path, sep=";", index_col="id")
    df["datetime"] = pd.to_datetime(
        df.date.astype(str) + " " + df.time.astype(str), format="%m/%d/%Y %H:%M"
    )
    df = df.drop(["date", "time"], axis=1)
    return df
