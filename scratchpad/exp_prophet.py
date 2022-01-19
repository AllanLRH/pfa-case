# %% imports
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

# %% read data
df = pd.read_csv(
    "https://github.com/facebook/prophet/raw/main/examples/example_wp_log_peyton_manning.csv"
)
df.head()

# %% fit
m = Prophet()
m.fit(df)

# %% make future
future = m.make_future_dataframe(periods=365)
future

# %% predict
forecast = m.predict(future)
forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()

fig1 = m.plot(forecast)

# Plot the predition components
fig2 = m.plot_components(forecast)

# %% Same, but in plotly
pf1 = plot_plotly(m, forecast)
pf2 = plot_components_plotly(m, forecast)

pf1.show()
pf2.show()

# %%
