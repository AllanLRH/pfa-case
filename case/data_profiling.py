# %% Imports and constants
import pandas as pd
from pandas_profiling import ProfileReport

from src.io_ops import load_sf_dataset
from src.shared_ressources import case_root

print(f"{case_root=}")

# %% Load data
df = load_sf_dataset()


# %% Examine data, generate and dsave report
print(f"{df.shape=}")

report = ProfileReport(df, explorative=True, lazy=False)
with (outfile := case_root / "artifacts" / "profiling_report.html").open("w") as fid:
    fid.write(report.to_html())

print(f"Profiling done, file saved to {outfile}")
