# References / Sources

## Textbook

- Brockwell, P. J., & Davis, R. A. (2016). *Introduction to Time Series and Forecasting*
  (3rd ed.). Springer Texts in Statistics.
  Chapter 1 — foundational examples of time series with trend and seasonality (e.g. Australian
  red wine sales, U.S. accidental deaths), the random walk / naive-forecast intuition, and
  moving-average trend smoothing. Used as the primary conceptual reference for trend,
  seasonality, and moving averages in this course.
  Note: this textbook is written at a graduate statistics level (formal stationarity
  definitions, autocovariance functions, ARMA processes). Its mathematical treatment was
  deliberately NOT carried into this beginner course — only the intuitive examples and the
  moving-average smoothing concept were adapted. Autocorrelation, stationarity, and ARIMA-style
  modeling are flagged as out of scope for this session and left for a later course.

## Official Documentation (verified for current syntax during course development)

- pandas API Reference: `DataFrame.rolling()`
  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html
- pandas API Reference: `DataFrame.shift()`
  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html
- scikit-learn: `sklearn.linear_model.LinearRegression`
  https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
- scikit-learn: `sklearn.metrics.mean_absolute_error`
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html
- scikit-learn: `sklearn.metrics.root_mean_squared_error`
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html
- scikit-learn: `sklearn.metrics.mean_absolute_percentage_error`
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_percentage_error.html
- scikit-learn User Guide: Regression metrics
  https://scikit-learn.org/stable/modules/model_evaluation.html

Every code snippet in the slide deck and notebooks was checked against these pages during
course development (September 2026) to confirm current, non-deprecated behaviour — in
particular:
- `root_mean_squared_error()` is the current, dedicated scikit-learn function for RMSE (added
  in version 1.4), replacing the older `mean_squared_error(squared=False)` pattern still seen
  in some older tutorials.
- `mean_absolute_percentage_error()` can return very large values when `y_true` contains values
  at or near zero — not a concern for this course's data (withdrawal amounts are always
  positive and far from zero), but worth knowing for other datasets.
- `DataFrame.rolling(window=N).mean()` and `DataFrame.shift(periods=N)` behave as documented,
  including producing `NaN` for the first `N` rows where a full window/shift isn't yet available.

## Data

All withdrawal data used in this course (`data/bank_cash_withdrawal_timeseries.csv`) is
**synthetic**, generated for teaching purposes by `data/generate_data.py`. It does not
represent any real bank, customer, or transaction. Amounts are denominated in Nigerian Naira
(₦) purely for narrative consistency with the course's banking scenario.
