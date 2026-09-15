"""
Generates a synthetic daily bank-cash-withdrawal time series used throughout
the Time Series Forecasting course (slides, visuals, and notebooks).

The series is synthetic but designed to contain everything a beginner needs
to practice on:
  - A gradual upward TREND (the bank's customer base and cash usage grows
    over the two years of history).
  - Weekly SEASONALITY (Fridays/Saturdays are busiest, Sundays are quietest,
    banks being closed for public business).
  - A monthly "salary period" effect (elevated withdrawals in the first few
    and last few days of each month).
  - Public-holiday effects (a spike the day BEFORE a holiday, a dip ON the
    holiday itself).
  - Random NOISE, plus a small number of unexplained realistic spikes.

Run:
    python generate_data.py
Produces:
    bank_cash_withdrawal_timeseries.csv
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

START_DATE = "2023-01-01"
N_DAYS = 730  # 2 years of daily data

dates = pd.date_range(START_DATE, periods=N_DAYS, freq="D")

# ---------------------------------------------------------------- trend --
# Gradual, gently accelerating growth in cash demand over the two years.
t = np.arange(N_DAYS)
trend = 20_000_000 + t * 18_000  # linear growth, ~13M naira added over 2 years

# ------------------------------------------------------------ seasonality --
# Day-of-week multiplier: banks are quiet on Sunday, busiest Fri/Sat.
dow_multiplier = {
    0: 1.00,  # Monday
    1: 0.97,  # Tuesday
    2: 0.95,  # Wednesday
    3: 1.02,  # Thursday
    4: 1.18,  # Friday (weekend cash-out)
    5: 1.10,  # Saturday
    6: 0.55,  # Sunday (most branches closed)
}
dow = dates.dayofweek
dow_factor = np.array([dow_multiplier[d] for d in dow])

# Salary-period effect: elevated withdrawals in the first 3 and last 3 days
# of each month (paydays cluster around month-end/start in this scenario).
day_of_month = dates.day
days_in_month = dates.days_in_month
is_salary_period = (day_of_month <= 3) | (day_of_month >= days_in_month - 2)
salary_factor = np.where(is_salary_period, 1.28, 1.0)

# ------------------------------------------------------------- holidays --
holidays = []
for year in [2023, 2024, 2025]:
    holidays += [
        f"{year}-01-01",   # New Year's Day
        f"{year}-10-01",   # Independence Day
        f"{year}-12-25",   # Christmas Day
        f"{year}-12-26",   # Boxing Day
    ]
holidays = pd.to_datetime([h for h in holidays if h in dates.astype(str).tolist() or True])
holidays = pd.DatetimeIndex([h for h in holidays if h in dates])

is_holiday = dates.isin(holidays)
is_day_before_holiday = dates.isin(holidays - pd.Timedelta(days=1))

holiday_factor = np.ones(N_DAYS)
holiday_factor[is_day_before_holiday] *= 1.55   # pre-holiday cash-out spike
holiday_factor[is_holiday] *= 0.35              # most branches/ATMs quieter on the day itself

# ------------------------------------------------------------------ noise --
noise = rng.normal(0, 1, N_DAYS) * (trend * 0.045)

# A handful of unexplained realistic spikes (e.g. local events, cash-in-transit
# timing, unexpected demand) — sparse and not tied to any feature in the dataset.
spike_days = rng.choice(N_DAYS, size=8, replace=False)
spike_effect = np.zeros(N_DAYS)
spike_effect[spike_days] = trend[spike_days] * rng.uniform(0.25, 0.55, size=8)

withdrawal = trend * dow_factor * salary_factor * holiday_factor + noise + spike_effect
withdrawal = np.clip(withdrawal, 2_000_000, None).round(0)

df = pd.DataFrame({
    "Date": dates,
    "WithdrawalAmount": withdrawal.astype(int),
})
df["DayOfWeek"] = df["Date"].dt.day_name()
df["IsWeekend"] = df["Date"].dt.dayofweek.isin([5, 6]).astype(int)
df["Month"] = df["Date"].dt.month
df["IsHolidayIndicator"] = is_holiday.astype(int)

df.to_csv("bank_cash_withdrawal_timeseries.csv", index=False)
print(f"Wrote {len(df)} rows to bank_cash_withdrawal_timeseries.csv")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print(df.head(10))
print()
print(f"Mean withdrawal: {df['WithdrawalAmount'].mean():,.0f}")
print(f"Holiday days: {df['IsHolidayIndicator'].sum()}")
