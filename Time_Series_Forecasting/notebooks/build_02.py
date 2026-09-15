import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# 02 — Moving Averages and Lags

**Hour 2, 80–90 min: Turning patterns into features**

In Notebook 01 we SAW trend and seasonality. Now we build the two most important beginner
tools for actually USING that information: moving averages (for smoothing/understanding) and
lag features (for feeding time-dependency into a model)."""))

cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (11, 5)

df = pd.read_csv("../data/bank_cash_withdrawal_timeseries.csv", parse_dates=["Date"])
df = df.sort_values("Date").reset_index(drop=True)
df.head()
"""))

cells.append(md("""## Moving Average

**What are we doing?** Computing a 7-day moving average — each day's smoothed value is the
average of that day and the 6 days before it.

**Why?** To smooth out short-term, day-to-day fluctuations so the bigger pattern (trend +
weekly rhythm) is easier to see."""))
cells.append(code("""
df["MA_7"] = df["WithdrawalAmount"].rolling(window=7).mean()
df[["Date", "WithdrawalAmount", "MA_7"]].head(10)
"""))

cells.append(md("""**What does `rolling()` do?** It creates a "window" that slides one row at a time down the
column, and `window=7` tells it to include the current row plus the 6 rows before it.

**Why are the first few rows of `MA_7` missing (`NaN`)?** For the very first row, there aren't
6 previous days to average yet — pandas can't compute a full 7-day window until day 7. This is
completely normal and expected."""))
cells.append(code("""
missing = df["MA_7"].isna().sum()
print(f"{missing} rows have a missing MA_7 value (exactly window - 1 = 6, as expected).")
"""))

cells.append(md("### Visualize: original vs. moving average"))
cells.append(code("""
recent = df.iloc[-120:]

fig, ax = plt.subplots()
ax.plot(recent["Date"], recent["WithdrawalAmount"] / 1e6, color="#9CA3AF", alpha=0.6, linewidth=1, label="Original (daily)")
ax.plot(recent["Date"], recent["MA_7"] / 1e6, color="#2563EB", linewidth=2.4, label="7-day moving average")
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Original Series vs. 7-Day Moving Average")
ax.legend()
plt.show()
"""))
cells.append(md("**Business perspective:** A moving average is great for UNDERSTANDING the data — spotting the "
                 "trend, communicating it to non-technical stakeholders — but on its own it does not "
                 "automatically forecast the future. It only tells us about the past."))

cells.append(md("""## Lag Features

**What are we doing?** Creating columns that hold PREVIOUS values of `WithdrawalAmount`,
lined up next to today's row.

**Why?** Yesterday's withdrawal total (and last week's) may contain useful clues about today's
total — this is called TIME DEPENDENCY. A lag feature is how we hand that information to an
ordinary regression model, which otherwise has no concept of "time" at all."""))
cells.append(code("""
df["Lag_1"] = df["WithdrawalAmount"].shift(1)
df["Lag_7"] = df["WithdrawalAmount"].shift(7)

df[["Date", "WithdrawalAmount", "Lag_1", "Lag_7"]].head(10)
"""))

cells.append(md("""**What does `shift()` do?** It moves every value DOWN by the given number of rows.
`shift(1)` means "yesterday's value, placed on today's row." `shift(7)` means "the value from
exactly 7 days ago, placed on today's row."

- **Lag_1** = yesterday's value.
- **Lag_7** = the value from 7 days ago (same day of the week last week — useful given our strong weekly seasonality!).

Notice the first row(s) are `NaN` for the same reason as the moving average — there's no "yesterday" for the very first row in our dataset."""))

cells.append(md("### Let's also add simple calendar features\n\nThese are free — we already know the date, so day-of-week and month cost nothing to compute."))
cells.append(code("""
df["DayOfWeekNum"] = df["Date"].dt.dayofweek  # Monday=0 ... Sunday=6
df["MonthNum"] = df["Date"].dt.month

df[["Date", "WithdrawalAmount", "Lag_1", "Lag_7", "DayOfWeekNum", "MonthNum", "IsWeekend"]].tail(10)
"""))

cells.append(md("""### Recap
- `rolling(window=7).mean()` smooths the series for understanding.
- `shift(1)` / `shift(7)` create lag features that capture time dependency for modeling.
- Both introduce missing values at the start of the series — that's expected, not a bug.
- We now have a feature-rich table: lag values + calendar features, ready for a model.

**Next: `03_Time_Series_Forecasting.ipynb`** — where we split this data correctly by time, build a naive baseline, and train our first real forecasting model."""))

nb["cells"] = cells
save(nb, "02_Moving_Averages_and_Lags.ipynb")
