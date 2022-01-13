import pandas as pd
import pathlib


def load_sf_csv(path: pathlib.Path):
    if not path:
        raise FileNotFoundError(f"Can't find the data file {path.absolute()}")
    df = pd.read_csv(path, sep=";", index_col="id")
    return df
