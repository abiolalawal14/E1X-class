"""
Generates every matplotlib chart used in the Time Series Forecasting slide
deck and notebooks. Run from this folder:  python generate_visuals.py
Reads ../data/bank_cash_withdrawal_timeseries.csv, writes PNGs here.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, mean_absolute_percentage_error

plt.rcParams.update({
    "font.family": "Segoe UI" if "Segoe UI" in [f.name for f in matplotlib.font_manager.fontManager.ttflist] else "DejaVu Sans",
    "font.size": 13,
    "axes.edgecolor": "#9CA3AF",
    "axes.labelcolor": "#1F2937",
    "text.color": "#1F2937",
    "xtick.color": "#4B5563",
    "ytick.color": "#4B5563",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})

INK = "#1F2937"
MUTED = "#6B7280"
GRID = "#E5E7EB"
BLUE = "#2563EB"
AMBER = "#D97706"
TEAL = "#0D9488"
PURPLE = "#7C3AED"
RED = "#DC2626"
GREEN = "#16A34A"

def style_ax(ax, grid=True):
    if grid:
        ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

def save(fig, name, dpi=220):
    fig.tight_layout()
    fig.savefig(f"{name}.png", dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)

df = pd.read_csv("../data/bank_cash_withdrawal_timeseries.csv", parse_dates=["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# =====================================================================
# 1. FULL SERIES — trend + seasonality visible (Slide 13 / 6)
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df["Date"], df["WithdrawalAmount"] / 1e6, color=BLUE, linewidth=0.9)
style_ax(ax)
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Daily ATM Withdrawals — Two Years of History", fontsize=15, weight="bold", color=INK, loc="left")
save(fig, "01_full_series")

# =====================================================================
# 2. TREND ILLUSTRATION (Slide 8) — full series + rolling trend line
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df["Date"], df["WithdrawalAmount"] / 1e6, color=MUTED, linewidth=0.7, alpha=0.6, label="Daily withdrawals")
trend_line = df["WithdrawalAmount"].rolling(30, center=True, min_periods=1).mean() / 1e6
ax.plot(df["Date"], trend_line, color=RED, linewidth=2.6, label="30-day trend")
style_ax(ax)
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("A Trend: The General Direction Over Time", fontsize=15, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "02_trend")

# =====================================================================
# 3. SEASONALITY — weekly pattern (Slide 9)
# =====================================================================
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_means = df.groupby("DayOfWeek")["WithdrawalAmount"].mean().reindex(dow_order) / 1e6
fig, ax = plt.subplots(figsize=(9, 5))
colors = [BLUE if d not in ("Friday", "Saturday") else AMBER for d in dow_order]
colors = [RED if d == "Sunday" else c for d, c in zip(dow_order, colors)]
ax.bar(dow_order, dow_means, color=colors, zorder=3)
style_ax(ax)
ax.set_ylabel("Average Withdrawal (₦ millions)")
ax.set_title("Seasonality: The Weekly Pattern Repeats", fontsize=15, weight="bold", color=INK, loc="left")
plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
save(fig, "03_seasonality_weekly")

# =====================================================================
# 4. ZOOMED-IN 6 WEEKS — see the repeating weekly shape clearly (Slide 9 support)
# =====================================================================
zoom = df.iloc[100:142]
fig, ax = plt.subplots(figsize=(10.5, 5))
ax.plot(zoom["Date"], zoom["WithdrawalAmount"] / 1e6, color=BLUE, marker="o", markersize=4, linewidth=1.6)
for _, row in zoom[zoom["DayOfWeek"] == "Sunday"].iterrows():
    ax.axvline(row["Date"], color=RED, alpha=0.15, linewidth=8, zorder=1)
style_ax(ax)
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Six Weeks, Zoomed In — Sundays Highlighted", fontsize=14.5, weight="bold", color=INK, loc="left")
save(fig, "04_zoomed_weekly_pattern")

# =====================================================================
# 5. NOISE illustration (Slide 11) — holiday spike/dip example
# =====================================================================
window = df[(df["Date"] >= "2023-09-20") & (df["Date"] <= "2023-10-10")]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(window["Date"], window["WithdrawalAmount"] / 1e6, color=BLUE, marker="o", markersize=5, linewidth=1.8)
holiday_pt = window[window["IsHolidayIndicator"] == 1]
ax.scatter(holiday_pt["Date"], holiday_pt["WithdrawalAmount"] / 1e6, color=RED, s=120, zorder=5, label="Public holiday (Oct 1)")
style_ax(ax)
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Unpredictable Events Create Noise", fontsize=15, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper right")
save(fig, "05_noise_holiday")

# =====================================================================
# 6. TREND + SEASONALITY + NOISE decomposition-style panel (Slide 7)
# =====================================================================
fig, axes = plt.subplots(3, 1, figsize=(10, 7.5), sharex=True)
axes[0].plot(df["Date"], trend_line, color=RED, linewidth=2)
axes[0].set_title("Trend", fontsize=12.5, weight="bold", loc="left")
weekly_component = df["WithdrawalAmount"] / 1e6 - trend_line
axes[1].plot(df["Date"].iloc[100:170], weekly_component.iloc[100:170], color=AMBER, linewidth=1.4)
axes[1].set_title("Seasonality (zoomed in)", fontsize=12.5, weight="bold", loc="left")
resid = weekly_component - weekly_component.rolling(7, center=True, min_periods=1).mean()
axes[2].plot(df["Date"], resid, color=MUTED, linewidth=0.7)
axes[2].set_title("Noise (what's left over)", fontsize=12.5, weight="bold", loc="left")
for ax in axes:
    style_ax(ax)
axes[2].set_xlabel("Date")
save(fig, "06_decomposition_panel")

# =====================================================================
# 7. MOVING AVERAGE comparison (Slide 16)
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 5.2))
recent = df.iloc[-180:]
ax.plot(recent["Date"], recent["WithdrawalAmount"] / 1e6, color=MUTED, alpha=0.5, linewidth=1, label="Original (daily)")
ma7 = recent["WithdrawalAmount"].rolling(7).mean() / 1e6
ax.plot(recent["Date"], ma7, color=BLUE, linewidth=2.4, label="7-day moving average")
style_ax(ax)
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Moving Average Smooths Out Short-Term Noise", fontsize=14.5, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "07_moving_average")

# =====================================================================
# 8. TIME-BASED TRAIN/TEST SPLIT diagram (Slide 22)
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 4.4))
split_idx = len(df) - 60
train_d, test_d = df.iloc[:split_idx], df.iloc[split_idx:]
ax.plot(train_d["Date"], train_d["WithdrawalAmount"] / 1e6, color=BLUE, linewidth=1.1, label="Training data (the past)")
ax.plot(test_d["Date"], test_d["WithdrawalAmount"] / 1e6, color=AMBER, linewidth=1.5, label="Test data (the \"future\")")
ax.axvline(train_d["Date"].iloc[-1], color=INK, linestyle="--", linewidth=1.3)
style_ax(ax)
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Train on the Past, Test on the Future", fontsize=15, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "08_train_test_split")

# =====================================================================
# 9. ACTUAL VS FORECAST (Slide 24) — baseline vs model
# =====================================================================
work = df.copy()
work["Lag_1"] = work["WithdrawalAmount"].shift(1)
work["Lag_7"] = work["WithdrawalAmount"].shift(7)
work["DoW"] = work["Date"].dt.dayofweek
work["MonthNum"] = work["Date"].dt.month
work = work.dropna().reset_index(drop=True)

split = len(work) - 60
train, test = work.iloc[:split], work.iloc[split:]
feats = ["Lag_1", "Lag_7", "DoW", "MonthNum", "IsWeekend"]
model = LinearRegression().fit(train[feats], train["WithdrawalAmount"])
pred = model.predict(test[feats])

naive_mae = mean_absolute_error(test["WithdrawalAmount"], test["Lag_1"])
naive_rmse = root_mean_squared_error(test["WithdrawalAmount"], test["Lag_1"])
naive_mape = mean_absolute_percentage_error(test["WithdrawalAmount"], test["Lag_1"]) * 100
model_mae = mean_absolute_error(test["WithdrawalAmount"], pred)
model_rmse = root_mean_squared_error(test["WithdrawalAmount"], pred)
model_mape = mean_absolute_percentage_error(test["WithdrawalAmount"], pred) * 100

print(f"Naive  -> MAE {naive_mae:,.0f}  RMSE {naive_rmse:,.0f}  MAPE {naive_mape:.1f}%")
print(f"Model  -> MAE {model_mae:,.0f}  RMSE {model_rmse:,.0f}  MAPE {model_mape:.1f}%")

fig, ax = plt.subplots(figsize=(11, 5.4))
ax.plot(test["Date"], test["WithdrawalAmount"] / 1e6, color=INK, linewidth=2, label="Actual")
ax.plot(test["Date"], pred / 1e6, color=BLUE, linewidth=2, linestyle="--", label="Forecast (model)")
style_ax(ax)
ax.set_xlabel("Date")
ax.set_ylabel("Withdrawal Amount (₦ millions)")
ax.set_title("Actual vs. Forecast on the Test Period", fontsize=15, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "09_actual_vs_forecast")

# =====================================================================
# 10. BASELINE VS MODEL error comparison bar chart (Slide 19 / 25 support)
# =====================================================================
fig, ax = plt.subplots(figsize=(8.5, 5.2))
metrics = ["MAE (₦m)", "RMSE (₦m)"]
naive_vals = [naive_mae / 1e6, naive_rmse / 1e6]
model_vals = [model_mae / 1e6, model_rmse / 1e6]
x = np.arange(len(metrics))
w = 0.32
ax.bar(x - w/2, naive_vals, width=w, color=MUTED, label="Naive baseline", zorder=3)
ax.bar(x + w/2, model_vals, width=w, color=BLUE, label="Lag-feature model", zorder=3)
style_ax(ax)
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylabel("Error (₦ millions)")
ax.set_title("Does the Model Beat the Baseline?", fontsize=15, weight="bold", color=INK, loc="left")
ax.legend(frameon=False)
for i, (n, m) in enumerate(zip(naive_vals, model_vals)):
    ax.text(i - w/2, n + 0.15, f"{n:.1f}", ha="center", fontsize=10.5, color=MUTED)
    ax.text(i + w/2, m + 0.15, f"{m:.1f}", ha="center", fontsize=10.5, color=BLUE)
save(fig, "10_baseline_vs_model")

# =====================================================================
# 11. LAG CONCEPT diagram data (Slide 14) — small table-like strip chart
# =====================================================================
sample = df.iloc[200:210].copy()
sample["Lag_1"] = df["WithdrawalAmount"].shift(1).iloc[200:210]
fig, ax = plt.subplots(figsize=(10, 4.6))
xpos = np.arange(len(sample))
ax.bar(xpos - 0.17, sample["WithdrawalAmount"] / 1e6, width=0.32, color=BLUE, label="Today's value", zorder=3)
ax.bar(xpos + 0.17, sample["Lag_1"] / 1e6, width=0.32, color=AMBER, label="Lag_1 (yesterday's value)", zorder=3)
style_ax(ax)
ax.set_xticks(xpos)
ax.set_xticklabels(sample["Date"].dt.strftime("%b %d"), rotation=30, ha="right")
ax.set_ylabel("₦ millions")
ax.set_title("A Lag Feature = A Previous Value, Shifted Forward", fontsize=14, weight="bold", color=INK, loc="left")
ax.legend(frameon=False)
save(fig, "11_lag_concept")

print("\nAll visuals generated.")
