import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# 02 — Isolation Forest

**Hour 2, 70–105 min: Feature selection, preprocessing, and building the model**

In the last notebook we explored the data by eye. Now we teach a machine to do the same
thing — spot unusual transactions — without ever telling it what "fraud" looks like.

We'll follow these steps, matching the slides exactly:
1. Import libraries
2. Load data
3. Inspect data
4. Select features
5. Preprocess (scale)
6. Train Isolation Forest
7. Generate predictions
8. Identify anomalies
9. Visualize anomalies
10. Interpret results

All scikit-learn syntax below was verified against the current official documentation."""))

cells.append(md("## 1. Import libraries"))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (9, 5.5)
"""))

cells.append(md("## 2. Load data"))
cells.append(code("""
df = pd.read_csv("../data/bank_transaction_anomaly_dataset.csv")
df.shape
"""))

cells.append(md("## 3. Inspect data\n\nQuick sanity check before we do anything else: any missing values?"))
cells.append(code("""
df.isna().sum()
"""))
cells.append(md("No missing values — good, we can skip imputation for this dataset."))

cells.append(md("""## 4. Select features

**What are we doing?** Choosing which columns actually describe a transaction's BEHAVIOUR —
the things that could make it look unusual.

**Why?** `transaction_id` and `customer_id` are just labels/identifiers — they carry no
meaningful "distance" information for the model (two customer IDs being numerically close
means nothing). We exclude them, along with the ground-truth `is_actual_anomaly` column,
which a real unsupervised system would never have."""))
cells.append(code("""
feature_cols = [
    "transaction_amount",
    "transaction_frequency",
    "transaction_hour",
    "distance_from_usual_location_km",
    "account_age_days",
]

X = df[feature_cols].copy()
X.head()
"""))

cells.append(md("""## 5. Preprocess: scale the features

**Why does this matter?** `transaction_amount` ranges into the millions, while
`transaction_hour` only ranges from 0 to 23. Isolation Forest's random splits work directly on
these raw values — a feature with a huge numeric range can end up dominating how the trees
split, purely because of its scale, not because it's actually more informative.

`StandardScaler` puts every feature on a comparable scale (mean 0, standard deviation 1)."""))
cells.append(code("""
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Turn it back into a labelled DataFrame just for readability
X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)
X_scaled_df.describe().round(2)
"""))
cells.append(md("Every column now has mean ≈ 0 and standard deviation ≈ 1 — exactly what we wanted."))

cells.append(md("""## 6. Train Isolation Forest

**What are we doing?** Fitting the model on our scaled features.

**Parameters:**
- `n_estimators=100` — build 100 random trees (the ensemble from the slides).
- `contamination=0.03` — our estimate that roughly 3% of transactions are unusual (a
  reasonable starting guess for this dataset — we'll experiment with this value in
  Notebook 03).
- `random_state=42` — makes the results reproducible run to run."""))
cells.append(code("""
model = IsolationForest(
    n_estimators=100,
    contamination=0.03,
    random_state=42,
)

model.fit(X_scaled)
"""))

cells.append(md("""## 7. Generate predictions

**What are we doing?** Asking the fitted model for a normal/anomaly flag on every transaction.

**What should we expect?** An array of `1`s (normal) and `-1`s (anomaly), one per row —
verified against the current scikit-learn documentation."""))
cells.append(code("""
predictions = model.predict(X_scaled)
predictions[:20]
"""))

cells.append(code("""
df["predicted_label"] = predictions
df["is_anomaly"] = (predictions == -1).astype(int)

df["is_anomaly"].value_counts()
"""))

cells.append(md("""## 8. Identify anomalies

Let's also compute the continuous anomaly score for every transaction, using
`score_samples()`. **Lower scores = more unusual** (this was confirmed against the current
scikit-learn docs)."""))
cells.append(code("""
df["anomaly_score"] = model.score_samples(X_scaled)

flagged = df[df["is_anomaly"] == 1].sort_values("anomaly_score")
print(f"Isolation Forest flagged {len(flagged)} transactions out of {len(df)}.")
flagged[["transaction_id", "customer_id", "transaction_amount", "transaction_frequency",
         "transaction_hour", "distance_from_usual_location_km", "anomaly_score"]].head(10)
"""))

cells.append(md("""**Business perspective:** These are the transactions the model considers LEAST like the
rest of the data — the ones an investigator should look at first. Notice the mix: some have
huge amounts, some have unusual frequency, some are a combination — exactly matching the
point/contextual/collective anomaly types from the slides."""))

cells.append(md("""## 9. Visualize anomalies

### 9a. Anomaly score distribution"""))
cells.append(code("""
fig, ax = plt.subplots()
ax.hist(df["anomaly_score"], bins=60, color="#2563EB")
ax.axvline(df.loc[df["is_anomaly"] == 1, "anomaly_score"].max(), color="#DC2626",
           linestyle="--", label="Cutoff implied by contamination=0.03")
ax.set_xlabel("Anomaly Score (lower = more unusual)")
ax.set_ylabel("Number of Transactions")
ax.set_title("Distribution of Anomaly Scores")
ax.legend()
plt.show()
"""))

cells.append(md("### 9b. Flagged transactions on a scatter plot"))
cells.append(code("""
fig, ax = plt.subplots(figsize=(9, 5.8))
normal = df[df["is_anomaly"] == 0]
anomaly = df[df["is_anomaly"] == 1]

ax.scatter(normal["transaction_amount"], normal["transaction_frequency"],
           s=18, alpha=0.4, color="#2563EB", label="Predicted normal")
ax.scatter(anomaly["transaction_amount"], anomaly["transaction_frequency"],
           s=50, alpha=0.9, color="#DC2626", marker="x", label="Predicted anomaly")
ax.set_xscale("log")
ax.set_xlabel("Transaction Amount (₦, log scale)")
ax.set_ylabel("Transaction Frequency")
ax.set_title("Isolation Forest — Flagged Transactions")
ax.legend()
plt.show()
"""))

cells.append(md("""## 10. Interpret results

Let's compare our predictions against the ground-truth `is_actual_anomaly` column — remember,
we only have this because our dataset is synthetic and built for teaching. A real fraud system
usually doesn't get this feedback until much later, if at all."""))
cells.append(code("""
from sklearn.metrics import classification_report, confusion_matrix

print("Confusion matrix (rows = actual, columns = predicted):")
print(confusion_matrix(df["is_actual_anomaly"], df["is_anomaly"]))
print()
print(classification_report(df["is_actual_anomaly"], df["is_anomaly"], digits=2,
                             target_names=["Normal", "Anomaly"]))
"""))

cells.append(md("""**What does this mean in business terms?**
- **Precision** tells us: of everything we flagged, what fraction were REALLY unusual?
- **Recall** tells us: of everything that was REALLY unusual, what fraction did we catch?
- A model can be tuned to catch almost everything (high recall) at the cost of far more false
  alarms (lower precision), or vice versa — that trade-off is controlled largely by
  `contamination`, which is exactly what we experiment with next, in Notebook 03.

### Recap
- We selected meaningful features and excluded IDs and the ground-truth label.
- We scaled the features so no single column dominates the distance calculations.
- We trained an Isolation Forest and used `predict()` and `score_samples()` to flag and rank
  unusual transactions.
- We visualized the result and connected it back to precision/recall.

**Next: `03_Anomaly_Detection_Mini_Project.ipynb`** — the contamination mini-challenge, and
building the complete anomaly detection pipeline end to end."""))

nb["cells"] = cells
save(nb, "02_Isolation_Forest.ipynb")
