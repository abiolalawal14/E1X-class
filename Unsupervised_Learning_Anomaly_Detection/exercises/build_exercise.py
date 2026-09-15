import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# Guided Exercise — Customer Transaction Anomaly Detection

**Scenario:** The bank wants to identify customers whose transaction behaviour is
significantly different from the majority of customers.

You are given `bank_transaction_anomaly_dataset_unlabeled.csv` — the SAME dataset you've used
all session, but with the ground-truth label removed, exactly like a real unsupervised problem.

Work through the steps below. Cells marked `# TODO` need you to fill something in — everywhere
else is provided to keep things moving. If you get stuck, the fully worked version is in
`solutions/anomaly_detection_exercise_solution.ipynb`, but try this yourself first!

**Estimated time: 30-45 minutes.**"""))

cells.append(md("## Step 1 — Load the dataset"))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (9, 5.5)

# TODO: load "../data/bank_transaction_anomaly_dataset_unlabeled.csv" into a DataFrame called df
df = ...  # YOUR CODE HERE

df.shape
"""))

cells.append(md("## Step 2 — Explore the data\n\nLook at the first few rows, the column data types, and basic statistics."))
cells.append(code("""
# TODO: display the first 5 rows
...  # YOUR CODE HERE
"""))
cells.append(code("""
# TODO: use .describe() to see summary statistics for the numeric columns
...  # YOUR CODE HERE
"""))

cells.append(md("""## Step 3 — Select appropriate features

Which columns actually describe transaction BEHAVIOUR? (Hint: exclude ID columns — they carry
no meaningful distance information.)"""))
cells.append(code("""
# TODO: build a list called feature_cols containing the behavioural feature column names
feature_cols = [
    # YOUR CODE HERE
]

X = df[feature_cols].copy()
X.head()
"""))

cells.append(md("## Step 4 — Preprocess: scale the features\n\nWhy is this necessary before training Isolation Forest? (Answer in a markdown cell if you like.)"))
cells.append(code("""
# TODO: create a StandardScaler, fit it on X, and produce X_scaled
scaler = ...       # YOUR CODE HERE
X_scaled = ...      # YOUR CODE HERE
"""))

cells.append(md("## Step 5 — Train Isolation Forest\n\nUse `n_estimators=100`, `contamination=0.03`, and `random_state=42`."))
cells.append(code("""
# TODO: create and fit an IsolationForest model called `model`
model = ...  # YOUR CODE HERE
"""))

cells.append(md("## Step 6 — Generate anomaly predictions"))
cells.append(code("""
# TODO: use model.predict(X_scaled) to get predictions, then create a column
# df["is_anomaly"] that is 1 where the model predicted an anomaly (-1) and 0 otherwise
predictions = ...  # YOUR CODE HERE
df["is_anomaly"] = ...  # YOUR CODE HERE
"""))

cells.append(md("## Step 7 — Count anomalies\n\nHow many transactions were flagged?"))
cells.append(code("""
# TODO: print how many transactions were flagged as anomalies
...  # YOUR CODE HERE
"""))

cells.append(md("## Step 8 — Visualize them\n\nMake a scatter plot of `transaction_amount` (log scale) vs. `transaction_frequency`, colouring points by `is_anomaly`."))
cells.append(code("""
# TODO: create the scatter plot described above
fig, ax = plt.subplots(figsize=(9, 5.5))

# YOUR CODE HERE

plt.show()
"""))

cells.append(md("## Step 9 — Investigate the most unusual observations\n\nCompute `model.score_samples(X_scaled)`, store it as `df[\"anomaly_score\"]`, and show the 10 lowest-scoring (most unusual) transactions."))
cells.append(code("""
# TODO
df["anomaly_score"] = ...  # YOUR CODE HERE

top10 = ...  # YOUR CODE HERE — sort df by anomaly_score ascending and take the first 10 rows
top10
"""))

cells.append(md("""## Step 10 — Explain and recommend

Answer these in a markdown cell:
1. What has the model identified? Describe the flagged transactions in your own words —
   are they mostly large amounts, high frequency, unusual timing, or a mix?
2. Does a flagged transaction automatically mean fraud? Why or why not?
3. What should the bank do next with this list of flagged transactions?"""))
cells.append(md("_Your answer here._"))

nb["cells"] = cells
save(nb, "anomaly_detection_exercise.ipynb")
