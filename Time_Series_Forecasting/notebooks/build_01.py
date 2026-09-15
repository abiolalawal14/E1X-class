import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# 01 — Time Series Exploration

**Hour 2, 60–80 min: Load and explore the dataset**

We're picking up the story from the slides: a bank wants to forecast daily ATM cash
withdrawals. Before we build anything, we need to load the data correctly, make sure it's in
the right time order, and actually LOOK at it.

**Remember the first rule of time series: visualize before you forecast.**

By the end of this notebook you will have:
- Loaded the withdrawal dataset
- Inspected its structure
- Converted the date column and sorted by time
- Visualized the series and started spotting trend, seasonality, and spikes with your own eyes"""))

cells.append(md("## Step 1 — Import Libraries"))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (11, 5)
"""))

cells.append(md("""## Step 2 — Load Dataset

`bank_cash_withdrawal_timeseries.csv` is a **synthetic** two-year daily series built to feel
like real bank ATM data. It does not represent any real bank."""))
cells.append(code("""
df = pd.read_csv("../data/bank_cash_withdrawal_timeseries.csv")
df.shape
"""))

cells.append(md("""## Step 3 — Inspect the Dataset

Here's what each column means:

| Column | Meaning |
|---|---|
| `Date` | The calendar date of this row |
| `WithdrawalAmount` | Total ATM withdrawals that day, in ₦ |
| `DayOfWeek` | Name of the day (Monday, Tuesday, ...) |
| `IsWeekend` | 1 if Saturday/Sunday, else 0 |
| `Month` | Calendar month number (1–12) |
| `IsHolidayIndicator` | 1 if this date is a public holiday, else 0 |"""))
cells.append(code("""
df.head()
"""))
cells.append(code("""
df.info()
"""))
cells.append(md("**What are we checking?** Data types — notice `Date` loaded as a plain object/string, "
                 "not a real date yet. We fix that next."))

cells.append(md("""## Step 4 — Convert Date Column

**What are we doing?** Converting the `Date` column from plain text into an actual datetime type.

**Why?** Pandas can only do date-aware things (plotting on a time axis, extracting day-of-week,
resampling, etc.) once it knows a column IS a date, not just a string that looks like one."""))
cells.append(code("""
df["Date"] = pd.to_datetime(df["Date"])
df.dtypes
"""))

cells.append(md("""## Step 5 — Sort Data by Time

> **Time must be in the correct order.**

This is one of the most important habits in time series work. A CSV file could easily have
rows in the wrong order (e.g. if it was exported from a system that sorted by customer ID
instead of date) — always sort explicitly rather than assuming."""))
cells.append(code("""
df = df.sort_values("Date").reset_index(drop=True)
df.head()
"""))
cells.append(code("""
# Sanity check: are there any duplicate or missing dates?
full_range = pd.date_range(df["Date"].min(), df["Date"].max(), freq="D")
missing_dates = full_range.difference(df["Date"])
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print(f"Expected days: {len(full_range)}, Actual rows: {len(df)}, Missing dates: {len(missing_dates)}")
"""))

cells.append(md("""## Step 6 — Visualize the Time Series

Now the fun part — let's actually look at it."""))
cells.append(code("""
fig, ax = plt.subplots()
ax.plot(df["Date"], df["WithdrawalAmount"] / 1e6, color="#2563EB", linewidth=0.9)
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Daily ATM Withdrawals")
plt.show()
"""))

cells.append(md("""**Look at the chart above and ask yourself:**
- Is there a trend? (Does the general level rise or fall over the two years?)
- Is there seasonality? (Does a pattern repeat at a regular interval?)
- Are there unusual spikes? (Any points that jump far above or below their neighbours?)

Try to form your own answer before reading on."""))

cells.append(md("""### A closer look: trend

Let's smooth the series with a 30-day rolling average to make the underlying trend easier to see
through the day-to-day noise."""))
cells.append(code("""
fig, ax = plt.subplots()
ax.plot(df["Date"], df["WithdrawalAmount"] / 1e6, color="#9CA3AF", linewidth=0.7, alpha=0.6, label="Daily")
trend = df["WithdrawalAmount"].rolling(30, center=True, min_periods=1).mean() / 1e6
ax.plot(df["Date"], trend, color="#DC2626", linewidth=2.5, label="30-day trend")
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Trend: The General Direction Over Time")
ax.legend()
plt.show()
"""))
cells.append(md("**What do we see?** A gentle, fairly steady upward trend — the bank's cash demand is growing "
                 "over the two years."))

cells.append(md("### A closer look: weekly seasonality"))
cells.append(code("""
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_avg = df.groupby("DayOfWeek")["WithdrawalAmount"].mean().reindex(dow_order) / 1e6

fig, ax = plt.subplots()
ax.bar(dow_order, dow_avg, color="#2563EB")
ax.set_ylabel("Average Withdrawal (₦ millions)")
ax.set_title("Average Withdrawal by Day of Week")
plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
plt.show()

dow_avg.round(1)
"""))
cells.append(md("**What do we see?** A clear, consistent weekly pattern — Fridays and Saturdays are the "
                 "busiest, and Sundays are by far the quietest (most branches closed). This is seasonality: a "
                 "pattern that repeats at a REGULAR interval, every 7 days."))

cells.append(md("""### Recap
- We loaded the raw CSV and converted `Date` to a real datetime column.
- We explicitly sorted the data by time — never assume a file is already in order.
- We visualized the full series and confirmed, with our own eyes, both a trend AND weekly
  seasonality before writing a single line of modeling code.

**Next: `02_Moving_Averages_and_Lags.ipynb`** — where we turn these patterns into features a
model can actually use."""))

nb["cells"] = cells
save(nb, "01_Time_Series_Exploration.ipynb")
