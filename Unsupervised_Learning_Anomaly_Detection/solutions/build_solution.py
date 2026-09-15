import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# Guided Exercise — SOLUTION

**Scenario:** The bank wants to identify customers whose transaction behaviour is
significantly different from the majority of customers.

This is the fully worked solution to `exercises/anomaly_detection_exercise.ipynb`. Try the
exercise yourself first — you'll learn more that way!"""))

cells.append(md("## Step 1 — Load the dataset"))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (9, 5.5)

df = pd.read_csv("../data/bank_transaction_anomaly_dataset_unlabeled.csv")
df.shape
"""))

cells.append(md("## Step 2 — Explore the data"))
cells.append(code("""
df.head()
"""))
cells.append(code("""
df.describe().round(1)
"""))

cells.append(md("""## Step 3 — Select appropriate features

We exclude `transaction_id` and `customer_id` — they're identifiers, not behaviour. Everything
else describes something meaningful about how the transaction happened."""))
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

cells.append(md("""## Step 4 — Preprocess: scale the features

This matters because `transaction_amount` (thousands to millions) and `transaction_hour`
(0-23) are on wildly different scales. Without scaling, `transaction_amount` would dominate
every distance calculation, and the model would effectively ignore the other features."""))
cells.append(code("""
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
"""))

cells.append(md("## Step 5 — Train Isolation Forest"))
cells.append(code("""
model = IsolationForest(
    n_estimators=100,
    contamination=0.03,
    random_state=42,
)
model.fit(X_scaled)
"""))

cells.append(md("## Step 6 — Generate anomaly predictions"))
cells.append(code("""
predictions = model.predict(X_scaled)
df["is_anomaly"] = (predictions == -1).astype(int)
df["is_anomaly"].value_counts()
"""))

cells.append(md("## Step 7 — Count anomalies"))
cells.append(code("""
n_flagged = df["is_anomaly"].sum()
print(f"Isolation Forest flagged {n_flagged} of {len(df)} transactions "
      f"({n_flagged / len(df) * 100:.1f}%).")
"""))

cells.append(md("## Step 8 — Visualize them"))
cells.append(code("""
fig, ax = plt.subplots(figsize=(9, 5.5))
normal = df[df["is_anomaly"] == 0]
anomaly = df[df["is_anomaly"] == 1]

ax.scatter(normal["transaction_amount"], normal["transaction_frequency"],
           s=18, alpha=0.4, color="#2563EB", label="Normal")
ax.scatter(anomaly["transaction_amount"], anomaly["transaction_frequency"],
           s=50, alpha=0.9, color="#DC2626", marker="x", label="Anomaly")
ax.set_xscale("log")
ax.set_xlabel("Transaction Amount (₦, log scale)")
ax.set_ylabel("Transaction Frequency")
ax.set_title("Flagged Transactions")
ax.legend()
plt.show()
"""))

cells.append(md("## Step 9 — Investigate the most unusual observations"))
cells.append(code("""
df["anomaly_score"] = model.score_samples(X_scaled)

top10 = df.sort_values("anomaly_score").head(10)
top10[["transaction_id", "customer_id", "transaction_amount", "transaction_frequency",
       "transaction_hour", "distance_from_usual_location_km", "anomaly_score"]]
"""))

cells.append(md("""## Step 10 — Explain and recommend

**1. What has the model identified?**
Looking at the top 10 most unusual transactions, we typically see a MIX: some with very large
`transaction_amount`, some with unusually high `transaction_frequency` (a burst of activity),
and some with an unusual combination of moderate amount + odd hour + large distance from the
customer's usual location. This matches the point / collective / contextual anomaly types from
the slides — the model didn't need to be told about these categories explicitly; they emerged
naturally from "what's easy to isolate."

**2. Does a flagged transaction automatically mean fraud?**
No. It means the transaction looks statistically UNUSUAL compared to the rest of the dataset.
It could be fraud, but it could also be a legitimate large purchase, a customer travelling, or
simply a data quirk. The model narrows down where to look — it doesn't make the final call.

**3. What should the bank do next?**
- Route the lowest-scoring (most unusual) transactions to a fraud analyst first — that's where
  investigative time has the highest expected payoff.
- For clearly high-amount point anomalies, consider a quick automated verification step
  (e.g. an SMS confirmation) rather than an outright block, to avoid frustrating legitimate
  customers.
- Log the outcome of each investigation (fraud / legitimate / other) and feed it back into
  future model tuning — over time this can turn today's unsupervised problem into a partially
  supervised one."""))

nb["cells"] = cells
save(nb, "anomaly_detection_exercise_solution.ipynb")
