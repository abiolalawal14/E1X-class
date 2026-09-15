import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# 01 — Anomaly Detection: Introduction

**Hour 2, 0–10 min: Load and explore the dataset**

We're picking up the story from the slides: a bank has thousands of transactions and no
labels telling us which ones are fraudulent. Before we train any model, we need to actually
**look at the data** — get a feel for what "normal" looks like, so that later we can judge
whether Isolation Forest's idea of "unusual" matches our own.

By the end of this notebook you will have:
- Loaded the transaction dataset
- Looked at its structure and basic statistics
- Visualized transaction amount, frequency, and timing
- Formed your own first impression of what looks unusual — **before** any algorithm tells you"""))

cells.append(md("## 1. Import libraries\n\nJust the essentials — Pandas for tables, NumPy for numbers, Matplotlib for charts."))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (9, 5)
"""))

cells.append(md("""## 2. Load the data

`bank_transaction_anomaly_dataset.csv` is a **synthetic** dataset built to feel like real bank
transactions. It does not represent any real bank or customer."""))
cells.append(code("""
df = pd.read_csv("../data/bank_transaction_anomaly_dataset.csv")
df.shape
"""))

cells.append(md("""**What are we doing?** Loading the CSV into a Pandas DataFrame.
**What should we expect?** A table with one row per transaction and a handful of columns
describing that transaction."""))
cells.append(code("""
df.head()
"""))

cells.append(md("""## 3. Understand the data

Each row is one transaction. Here's what each column means:

| Column | Meaning |
|---|---|
| `transaction_id` | Unique ID for the transaction |
| `customer_id` | Which customer made it |
| `transaction_amount` | Amount in ₦ |
| `transaction_frequency` | How many transactions this customer made in the same hour |
| `transaction_hour` | Hour of day (0–23) the transaction happened |
| `distance_from_usual_location_km` | Distance (km) from where this customer usually transacts |
| `account_age_days` | How long the account has existed |
| `is_actual_anomaly` | **Ground truth** — 1 if we (the dataset creators) planted this as an anomaly, 0 otherwise |

> **Important:** In a REAL fraud problem, `is_actual_anomaly` would not exist — that's the whole
> point of unsupervised learning. We've included it here ONLY so that later in this course we
> can check how well our model actually did. Today, pretend you can't see it until we get to
> the evaluation section."""))
cells.append(code("""
df.info()
"""))

cells.append(md("## 4. Basic statistics\n\n`describe()` gives us mean, std, min, max, and quartiles for every numeric column at a glance."))
cells.append(code("""
df.describe().round(1)
"""))

cells.append(md("""**What does this tell us?**
- `transaction_amount`: the mean is much higher than the median (50%) would suggest — a classic
  sign that a few very large values are pulling the average up. That's often what anomalies look
  like in raw statistics, even before we build any model.
- `transaction_frequency`: mostly small numbers (1-4), but the max is far higher — worth a closer look.

Let's also check: how many transactions are actually planted anomalies?"""))
cells.append(code("""
df["is_actual_anomaly"].value_counts()
"""))
cells.append(code("""
pct = df["is_actual_anomaly"].mean() * 100
print(f"{pct:.1f}% of transactions are actual anomalies")
"""))

cells.append(md("""## 5. Visualize transaction behaviour

### 5a. Transaction amount distribution

We'll use a log scale on the x-axis — transaction amounts span from a few thousand naira to
several million, and a normal (linear) scale would squash everything interesting into an
unreadable sliver."""))
cells.append(code("""
fig, ax = plt.subplots()
ax.hist(df["transaction_amount"], bins=np.logspace(np.log10(1000), np.log10(1e7), 60), color="#2563EB")
ax.set_xscale("log")
ax.set_xlabel("Transaction Amount (₦, log scale)")
ax.set_ylabel("Number of Transactions")
ax.set_title("Transaction Amount Distribution")
plt.show()
"""))

cells.append(md("""**What do we see?** A big cluster of "everyday" transaction amounts, and a thin scatter of
much larger ones off to the right. Those large ones are candidates for point anomalies — but
remember, an anomaly isn't only about being large (see the slides on contextual and collective
anomalies)."""))

cells.append(md("### 5b. Transaction frequency\n\nHow many transactions does a customer typically make within the same hour?"))
cells.append(code("""
fig, ax = plt.subplots()
ax.hist(df["transaction_frequency"], bins=range(0, 36), color="#0D9488")
ax.set_xlabel("Transactions in the Same Hour")
ax.set_ylabel("Number of Rows")
ax.set_title("Transaction Frequency Distribution")
plt.show()
"""))

cells.append(md("""**What do we see?** Most rows show 1-4 transactions/hour. A small number show 15+ — that's
the signature of the "collective anomaly" pattern from the slides (a burst of rapid transactions)."""))

cells.append(md("### 5c. When do transactions happen?"))
cells.append(code("""
fig, ax = plt.subplots()
ax.hist(df["transaction_hour"], bins=range(0, 25), color="#D97706", align="left")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Number of Transactions")
ax.set_title("Transaction Timing")
ax.set_xticks(range(0, 24, 2))
plt.show()
"""))

cells.append(md("""**What do we see?** Activity peaks during the day and drops off at night — matching normal
human behaviour. A cluster of transactions in the very early hours (1am-4am) stands out as
unusual, which connects back to the "contextual anomaly" idea from the slides."""))

cells.append(md("""### 5d. Amount vs. frequency — a first (unaided) look

Let's plot amount against frequency and colour by the ground-truth label, JUST to build
intuition about how these injected anomalies actually look in the data. Remember: in a real
project we would not have this colour information yet."""))
cells.append(code("""
fig, ax = plt.subplots(figsize=(8.5, 5.5))
normal = df[df["is_actual_anomaly"] == 0]
anomaly = df[df["is_actual_anomaly"] == 1]
ax.scatter(normal["transaction_amount"], normal["transaction_frequency"],
           s=18, alpha=0.4, color="#2563EB", label="Normal")
ax.scatter(anomaly["transaction_amount"], anomaly["transaction_frequency"],
           s=45, alpha=0.85, color="#DC2626", marker="x", label="Actual anomaly (ground truth)")
ax.set_xscale("log")
ax.set_xlabel("Transaction Amount (₦, log scale)")
ax.set_ylabel("Transaction Frequency")
ax.legend()
ax.set_title("Amount vs. Frequency — Ground Truth (for learning purposes only)")
plt.show()
"""))

cells.append(md("""**Business perspective:** Notice the anomalies don't all sit in one obvious corner. Some are
just "big amount", some are just "high frequency", and some (the contextual ones — large
amount, very late at night, far from usual location) don't stand out on THIS chart at all. This
is exactly why we need an algorithm that considers **all the features together**, not just one
or two at a time — which is exactly what Isolation Forest does, coming up in the next notebook.

### Recap
- We loaded and explored a realistic (synthetic) transaction dataset.
- We saw that "unusual" shows up differently depending on which features you look at.
- We deliberately have NOT trained any model yet — that intuition-first step matters.

**Next: `02_Isolation_Forest.ipynb`** — where we actually train a model to find these patterns
automatically, without using the `is_actual_anomaly` column at all."""))

nb["cells"] = cells
save(nb, "01_Anomaly_Detection_Introduction.ipynb")
