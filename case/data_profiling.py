# %% Imports and constants
import pandas as pd
from pandas_profiling import ProfileReport

from src.io_ops import load_sf_csv
from src.shared_ressources import case_root

print(f"{case_root=}")

# %% Load data
data_path = case_root / "data" / "sf_data.csv"
df = load_sf_csv(data_path)


# %% Examine data, generate and dsave report
print(f"{df.shape=}")

report = ProfileReport(df, explorative=True, lazy=False)
with (outfile := case_root / "artifacts" / "profiling_report.html").open("w") as fid:
    fid.write(report.to_html())

print(f"Profiling done, file saved to {outfile}")
