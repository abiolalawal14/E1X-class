# References / Sources

## Textbook

- Aggarwal, C. C. (2015). *Data Mining: The Textbook*. Springer.
  Chapter 8, "Outlier Analysis" — extreme value analysis, distance-based outlier detection,
  and density-based methods (Local Outlier Factor). Used as the primary conceptual reference
  for the statistical, distance-based, and density-based approaches covered in this course.
  Note: this textbook (2015) predates widespread adoption of Isolation Forest in mainstream
  teaching materials and only cites it in the bibliography — the Isolation Forest content in
  this course was built from the original paper and current scikit-learn documentation instead.

## Original Research

- Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). *Isolation Forest*. IEEE International
  Conference on Data Mining (ICDM).

## Official Documentation (verified for current syntax during course development)

- scikit-learn: `sklearn.ensemble.IsolationForest`
  https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
- scikit-learn: `sklearn.neighbors.LocalOutlierFactor`
  https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html
- scikit-learn: `sklearn.svm.OneClassSVM`
  https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html
- scikit-learn: `sklearn.preprocessing.StandardScaler`
  https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
- scikit-learn User Guide: Novelty and Outlier Detection
  https://scikit-learn.org/stable/modules/outlier_detection.html

Every code snippet in the slide deck and notebooks was checked against these pages during
course development (September 2026) to confirm current, non-deprecated behaviour — in
particular:
- `IsolationForest(n_estimators=100, contamination="auto", random_state=42)` constructor
  defaults.
- `predict()` returns `1` for inliers (normal) and `-1` for outliers (anomalies) — consistent
  across `IsolationForest`, `LocalOutlierFactor`, and `OneClassSVM`.
- `decision_function()` and `score_samples()` — **lower values indicate more anomalous**
  observations.

## Data

All transaction data used in this course (`data/bank_transaction_anomaly_dataset.csv`) is
**synthetic**, generated for teaching purposes by `data/generate_data.py`. It does not
represent any real bank, customer, or transaction. Amounts are denominated in Nigerian Naira
(₦) purely for narrative consistency with the course's banking scenario.
