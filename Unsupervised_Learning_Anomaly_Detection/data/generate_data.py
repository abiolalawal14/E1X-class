"""
Generates a synthetic bank-transaction dataset used throughout the Anomaly
Detection course (slides, visuals, and notebooks).

The data is synthetic but designed so that:
  - The vast majority of transactions look "normal" (consistent with each
    customer's own typical behaviour).
  - A small minority (~3%) are injected anomalies of three different kinds
    (point, contextual, collective) mixed across multiple features — NOT
    obvious from a single column, so students can't just eyeball a threshold
    on one feature and be done.
  - A ground-truth `is_actual_anomaly` column is included ONLY for
    instructor/teaching use (e.g. to illustrate precision/recall in the
    evaluation section). The notebooks are explicit that this column would
    NOT exist in a real unlabeled fraud-detection problem.

Run:
    python generate_data.py
Produces:
    bank_transaction_anomaly_dataset.csv          (full, with label column)
    bank_transaction_anomaly_dataset_unlabeled.csv (no label column, for student exercises)
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

N_CUSTOMERS = 900
N_NORMAL_TX = 4850
N_ANOMALY_TX = 150  # ~3% of the final ~5000 rows

# ---------------------------------------------------------------- customers --
customer_ids = [f"CUST{20000+i}" for i in range(N_CUSTOMERS)]
# Each customer has their own typical spending level (lognormal mixture:
# most are everyday retail customers, a smaller group are small-business customers)
is_business = rng.random(N_CUSTOMERS) < 0.15
base_amount = np.where(
    is_business,
    rng.lognormal(mean=12.5, sigma=0.5, size=N_CUSTOMERS),   # business: larger typical amounts
    rng.lognormal(mean=10.2, sigma=0.6, size=N_CUSTOMERS),   # retail: smaller typical amounts
)
account_age = rng.integers(30, 4000, N_CUSTOMERS)

customer_table = pd.DataFrame({
    "customer_id": customer_ids,
    "typical_amount": base_amount,
    "account_age_days": account_age,
})

# ---------------------------------------------------------- normal transactions --
def make_normal_transactions(n):
    idx = rng.integers(0, N_CUSTOMERS, n)
    cust = customer_table.iloc[idx].reset_index(drop=True)
    amount = rng.lognormal(mean=np.log(cust["typical_amount"]), sigma=0.35)
    amount = amount.clip(2_000, 480_000)
    hour = rng.normal(14, 4, n)  # daytime-centred, mostly 7am-10pm
    hour = np.mod(hour, 24).round().astype(int)
    distance = rng.exponential(3.5, n).clip(0, 40)   # usually near "home" location
    frequency = rng.poisson(1.1, n).clip(1, 4)        # usually 1-4 tx/hour
    return pd.DataFrame({
        "customer_id": cust["customer_id"],
        "transaction_amount": amount.round(0),
        "transaction_frequency": frequency,
        "transaction_hour": hour,
        "distance_from_usual_location_km": distance.round(1),
        "account_age_days": cust["account_age_days"],
        "is_actual_anomaly": 0,
    })

normal_df = make_normal_transactions(N_NORMAL_TX)

# --------------------------------------------------------- anomalous transactions --
def make_point_anomalies(n):
    """Type 1: point anomaly — an extreme amount, far outside anything in the dataset."""
    idx = rng.integers(0, N_CUSTOMERS, n)
    cust = customer_table.iloc[idx].reset_index(drop=True)
    amount = rng.uniform(2_000_000, 9_500_000, n)
    hour = rng.integers(8, 21, n)
    distance = rng.exponential(3.5, n).clip(0, 20)
    frequency = rng.poisson(1.2, n).clip(1, 3)
    return pd.DataFrame({
        "customer_id": cust["customer_id"],
        "transaction_amount": amount.round(0),
        "transaction_frequency": frequency,
        "transaction_hour": hour,
        "distance_from_usual_location_km": distance.round(1),
        "account_age_days": cust["account_age_days"],
        "is_actual_anomaly": 1,
    })

def make_contextual_anomalies(n):
    """Type 2: contextual anomaly — nothing individually extreme, but an unusual
    COMBINATION: moderate-large amount, very late-night hour, and far from the
    customer's usual location all at once."""
    idx = rng.integers(0, N_CUSTOMERS, n)
    cust = customer_table.iloc[idx].reset_index(drop=True)
    amount = rng.uniform(150_000, 900_000, n)
    hour = rng.choice([1, 2, 3, 4], size=n)
    distance = rng.uniform(80, 400, n)
    frequency = rng.poisson(1.3, n).clip(1, 3)
    return pd.DataFrame({
        "customer_id": cust["customer_id"],
        "transaction_amount": amount.round(0),
        "transaction_frequency": frequency,
        "transaction_hour": hour,
        "distance_from_usual_location_km": distance.round(1),
        "account_age_days": cust["account_age_days"],
        "is_actual_anomaly": 1,
    })

def make_collective_anomalies(n_customers_affected):
    """Type 3: collective anomaly — a burst of many rapid transactions from the
    same customer in a short window (card-testing / account-takeover pattern).
    Each individual transaction amount is unremarkable."""
    rows = []
    idx = rng.integers(0, N_CUSTOMERS, n_customers_affected)
    cust = customer_table.iloc[idx].reset_index(drop=True)
    for i in range(n_customers_affected):
        burst_size = rng.integers(3, 6)  # a handful of rows share the same burst signature
        amount = rng.uniform(3_000, 60_000, burst_size)
        hour = np.full(burst_size, rng.integers(0, 24))
        distance = rng.uniform(0, 25, burst_size)
        frequency = np.full(burst_size, rng.integers(15, 35))  # the giveaway feature
        for j in range(burst_size):
            rows.append({
                "customer_id": cust["customer_id"].iloc[i],
                "transaction_amount": round(amount[j], 0),
                "transaction_frequency": int(frequency[j]),
                "transaction_hour": int(hour[j]),
                "distance_from_usual_location_km": round(distance[j], 1),
                "account_age_days": int(cust["account_age_days"].iloc[i]),
                "is_actual_anomaly": 1,
            })
    return pd.DataFrame(rows)

n_point = 55
n_contextual = 55
n_collective_customers = 10  # produces ~40 rows given burst_size 3-6

point_df = make_point_anomalies(n_point)
contextual_df = make_contextual_anomalies(n_contextual)
collective_df = make_collective_anomalies(n_collective_customers)

anomaly_df = pd.concat([point_df, contextual_df, collective_df], ignore_index=True)

# ------------------------------------------------------------------ combine --
df = pd.concat([normal_df, anomaly_df], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.insert(0, "transaction_id", [f"TXN{500000+i}" for i in range(len(df))])

df["transaction_amount"] = df["transaction_amount"].astype(int)
df["distance_from_usual_location_km"] = df["distance_from_usual_location_km"].round(1)

out_path = "bank_transaction_anomaly_dataset.csv"
df.to_csv(out_path, index=False)
print(f"Wrote {len(df)} rows to {out_path}")
print(f"  Actual anomalies: {df['is_actual_anomaly'].sum()} "
      f"({df['is_actual_anomaly'].mean()*100:.1f}% of rows)")
print(df.head())

df_unlabeled = df.drop(columns=["is_actual_anomaly"])
df_unlabeled.to_csv("bank_transaction_anomaly_dataset_unlabeled.csv", index=False)
print("Wrote bank_transaction_anomaly_dataset_unlabeled.csv (no label column) for student exercises")
