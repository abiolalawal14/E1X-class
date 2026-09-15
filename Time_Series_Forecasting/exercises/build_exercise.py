import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# Guided Exercise — Cash Demand Forecasting

**Scenario:** The bank's operations team wants a working forecast of daily ATM withdrawals so
they can plan cash-loading schedules more efficiently.

You'll use the same `bank_cash_withdrawal_timeseries.csv` dataset from class. Cells marked
`# TODO` need you to fill something in — everywhere else is provided to keep things moving. If
you get stuck, the fully worked version is in
`solutions/forecasting_exercise_solution.ipynb`, but try this yourself first!

**Estimated time: 30-45 minutes.**"""))

cells.append(md("## Step 1 — Load the dataset"))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, mean_absolute_percentage_error

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (11, 5)

# TODO: load "../data/bank_cash_withdrawal_timeseries.csv", parsing the Date column as a date
df = ...  # YOUR CODE HERE

df.shape
"""))

cells.append(md("## Step 2 — Sort by date\n\nRemember: never assume a file is already in time order."))
cells.append(code("""
# TODO: sort df by Date and reset the index
df = ...  # YOUR CODE HERE
df.head()
"""))

cells.append(md("## Step 3 — Visualize the series\n\nPlot `WithdrawalAmount` over `Date`. Look for trend, seasonality, and spikes."))
cells.append(code("""
# TODO: create a line plot of WithdrawalAmount over Date
fig, ax = plt.subplots()

# YOUR CODE HERE

plt.show()
"""))

cells.append(md("## Step 4 — Create lag features\n\nCreate `Lag_1` (yesterday's value) and `Lag_7` (the value from 7 days ago)."))
cells.append(code("""
# TODO
df["Lag_1"] = ...  # YOUR CODE HERE
df["Lag_7"] = ...  # YOUR CODE HERE
"""))

cells.append(md("## Step 5 — Create calendar features\n\nCreate `DayOfWeekNum` (0=Monday...6=Sunday) and `MonthNum` (1-12) from the `Date` column."))
cells.append(code("""
# TODO
df["DayOfWeekNum"] = ...  # YOUR CODE HERE
df["MonthNum"] = ...      # YOUR CODE HERE

# Drop rows with missing lag values
df = df.dropna().reset_index(drop=True)
df.shape
"""))

cells.append(md("## Step 6 — Time-based train/test split\n\nUse the LAST 45 days as the test set. Do NOT shuffle."))
cells.append(code("""
TEST_DAYS = 45

# TODO: compute split_index, then create train and test DataFrames
split_index = ...  # YOUR CODE HERE
train = ...          # YOUR CODE HERE
test = ...            # YOUR CODE HERE

print(f"Train: {len(train)} rows, Test: {len(test)} rows")
"""))

cells.append(md("## Step 7 — Build a naive baseline\n\nThe naive forecast for each test-set day is simply `Lag_1` (yesterday's actual value)."))
cells.append(code("""
# TODO: compute naive_mae using mean_absolute_error(actual, Lag_1 for the test set)
naive_mae = ...  # YOUR CODE HERE
print(f"Naive baseline MAE: {naive_mae:,.0f}")
"""))

cells.append(md("## Step 8 — Train a forecasting model\n\nUse `LinearRegression` with features: `Lag_1`, `Lag_7`, `DayOfWeekNum`, `MonthNum`, `IsWeekend`."))
cells.append(code("""
feature_cols = ["Lag_1", "Lag_7", "DayOfWeekNum", "MonthNum", "IsWeekend"]

# TODO: create and fit a LinearRegression model on the training set
model = ...  # YOUR CODE HERE

# TODO: generate predictions on the test set
forecast = ...  # YOUR CODE HERE
"""))

cells.append(md("## Step 9 — Evaluate: MAE, RMSE, MAPE"))
cells.append(code("""
# TODO: compute model_mae, model_rmse, model_mape using the sklearn metrics imported above
model_mae = ...   # YOUR CODE HERE
model_rmse = ...  # YOUR CODE HERE
model_mape = ...  # YOUR CODE HERE

print(f"Model MAE: {model_mae:,.0f}   RMSE: {model_rmse:,.0f}   MAPE: {model_mape*100:.1f}%")
print(f"Naive MAE: {naive_mae:,.0f}")
"""))

cells.append(md("## Step 10 — Visualize actual vs. forecast"))
cells.append(code("""
# TODO: plot test["WithdrawalAmount"] (actual) and forecast on the same chart, over test["Date"]
fig, ax = plt.subplots(figsize=(11, 5.5))

# YOUR CODE HERE

plt.show()
"""))

cells.append(md("""## Step 11 — Answer these questions

1. Did your model beat the naive baseline? By how much?
2. Is there a visible trend and/or weekly seasonality in this data?
3. Where does the forecast track the actual values well? Where does it struggle?
4. What should the bank's cash operations team do with this forecast?"""))
cells.append(md("_Your answers here._"))

nb["cells"] = cells
save(nb, "forecasting_exercise.ipynb")
