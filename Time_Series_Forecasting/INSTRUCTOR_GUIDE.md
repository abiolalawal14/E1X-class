# Instructor Guide — 2-Hour Delivery Plan

**Course:** Time Series Forecasting — Predicting the Future Using Historical Data
**Audience:** Beginner Data Scientists (comfortable with Python, Pandas, basic ML/regression)
**Format:** Hour 1 conceptual (slides), Hour 2 hands-on (Jupyter notebooks)

The whole session is one connected story: *"We have historical data. Can we predict what
happens next?"* Keep returning to the bank ATM cash-withdrawal example throughout — this is
not a tour of separate techniques.

---

## Before class

- Open `Time_Series_Forecasting_Beginner_Course.pptx` in Google Slides or PowerPoint and skim
  speaker notes once.
- Confirm `data/bank_cash_withdrawal_timeseries.csv` exists (regenerate with
  `python data/generate_data.py` if needed — it's deterministic, `random_state=42`).
- Have `notebooks/01` through `04` open and pre-run once so you're not debugging live.
- Decide whether students code along in real time or watch you build 01-04 and then do
  `exercises/forecasting_exercise.ipynb` themselves — the timing below assumes the latter.

---

## Hour 1 — Concepts (Slides 1–33)

| Time | Slides | Focus |
|---|---|---|
| 0–10 min | 1–4 | Title, learning objectives, the real business question, why time order matters |
| 10–20 min | 5–6 | What is Time Series data? Real-life examples across industries |
| 20–35 min | 7–11 | Trend, seasonality, cycles, noise |
| 35–45 min | 12–17 | Visualize first, lags, moving averages |
| 45–52 min | 18–22 | Forecasting definition, baseline, the workflow, train/test split |
| 52–58 min | 23–29 | Evaluation metrics, actual vs. forecast, simple models, business interpretation, common mistakes, recap |
| 58–60 min | 30 | Transition to coding |

**Pacing notes:**
- Slide 4 (what makes this different) and Slides 21–22 (time-based splitting) are the two
  concepts worth slowing down for — they're the strongest, most distinctive ideas in the whole
  course. Don't rush them.
- If you're behind schedule, the safest slides to compress are 6 (industry examples table) and
  10 (cycles) — read briskly, since they're supporting context rather than core mechanics.
- Slides 31–32 (misconceptions table, quiz) can be run as a quick group call-and-response
  rather than individual writing, to protect time. Full answer key is in the quiz slide's
  speaker notes.

---

## Hour 2 — Hands-On Coding

| Time | Activity | Notebook |
|---|---|---|
| 60–70 min | Load and explore data | `notebooks/01_Time_Series_Exploration.ipynb` |
| 70–80 min | Visualize the series, spot trend/seasonality | `notebooks/01` (Step 6) |
| 80–90 min | Moving averages and lag features | `notebooks/02_Moving_Averages_and_Lags.ipynb` |
| 90–100 min | Train/test split and baseline | `notebooks/03_Time_Series_Forecasting.ipynb` (through the naive baseline section) |
| 100–110 min | Train forecasting model | `notebooks/03` (model training + evaluation) |
| 110–116 min | Evaluate and visualize forecast | `notebooks/03` (actual vs. forecast section) |
| 116–120 min | Mini challenge and recap | `notebooks/04_Cash_Demand_Forecasting_Project.ipynb` (mini challenge section) |

**Delivery notes:**
- All four main notebooks have been executed end-to-end with no errors under the current
  pandas/scikit-learn versions — you should not hit install or environment surprises live.
- Real numbers on this dataset to anchor discussion: naive baseline MAE ≈ ₦8.2M; the simple
  lag-feature regression model MAE ≈ ₦4.7M (about a 43% reduction) — a strong, honest
  demonstration that the model earns its complexity over the baseline.
- The mini challenge (Notebook 04) adds a `Lag_14` feature and compares it against the
  original 5-feature model. On this dataset it actually helps slightly (~8% further MAE
  reduction) — a good prompt for discussing WHY (two-week patterns vs. the already-strong
  one-week pattern captured by `Lag_7`), not just reporting the number.
- `exercises/forecasting_exercise.ipynb` is intentionally incomplete (`# TODO` cells with `...`
  placeholders) — it will NOT run as downloaded. That's by design: assign it as the 30–45
  minute capstone to complete after class, or as a guided in-class exercise if time allows.
  `solutions/forecasting_exercise_solution.ipynb` is the fully worked, executed reference,
  using a 45-day test split (slightly different from the 60-day split used in Notebooks 01-04,
  to keep the exercise recognizably its own task).
- Close Hour 2 by returning explicitly to the business-interpretation questions (Slide 27 /
  Notebook 04's final section): a forecast only matters once it changes what the bank actually
  does with it.

---

## Common questions to anticipate

- **"Why not just use the 7-day moving average as the forecast?"** — A moving average only
  describes the PAST; it has no mechanism for projecting forward or reacting to calendar
  effects (day of week, month). It's a descriptive/exploration tool, not a forecasting model —
  Slide 17 makes this distinction explicit.
- **"Why linear regression and not ARIMA/Prophet/LSTM?"** — Scope: this is a beginner's first
  exposure to forecasting. Reframing forecasting as regression-with-time-aware-features is the
  fastest path to a genuinely working, understandable pipeline. Slide 25 explicitly places
  advanced models as "later courses."
- **"Isn't a 60-day test period arbitrary?"** — Yes, deliberately illustrative. In practice the
  right test window depends on forecast horizon needs and how much history is available; the
  KEY constraint is only that the split respects chronological order, not shuffling.
- **"What if `Lag_14` had made things worse?"** — That would have been an equally valid, useful
  teaching outcome — more features are not automatically better (Misconception 3 on Slide 31).
  The mini challenge is designed to be a genuine open question, not a foregone conclusion.
