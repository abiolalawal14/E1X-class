"""
Generates every matplotlib chart used in the Anomaly Detection slide deck
and notebooks. Run from this folder:  python generate_visuals.py
Reads ../data/bank_transaction_anomaly_dataset.csv, writes PNGs here.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

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

df = pd.read_csv("../data/bank_transaction_anomaly_dataset.csv")
features = ["transaction_amount", "transaction_frequency", "transaction_hour",
            "distance_from_usual_location_km", "account_age_days"]
Xs = StandardScaler().fit_transform(df[features].values)

model = IsolationForest(n_estimators=100, contamination=0.03, random_state=42).fit(Xs)
df["predicted_anomaly"] = (model.predict(Xs) == -1).astype(int)
df["anomaly_score"] = model.score_samples(Xs)

# =====================================================================
# 1. NORMAL VS ANOMALOUS DISTRIBUTION (Slide 5)
# =====================================================================
fig, ax = plt.subplots(figsize=(9, 5))
normal = df[df["is_actual_anomaly"] == 0]["transaction_amount"]
anom = df[df["is_actual_anomaly"] == 1]["transaction_amount"]
bins = np.logspace(np.log10(1000), np.log10(10_000_000), 60)
ax.hist(normal, bins=bins, color=BLUE, alpha=0.75, label="Normal transactions", zorder=3)
ax.hist(anom, bins=bins, color=RED, alpha=0.85, label="Unusual transactions", zorder=4)
ax.set_xscale("log")
style_ax(ax)
ax.set_xlabel("Transaction Amount (₦, log scale)")
ax.set_ylabel("Number of Transactions")
ax.set_title("Most Transactions Cluster Together — A Few Stand Apart", fontsize=15, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper right")
save(fig, "01_normal_vs_anomalous")

# =====================================================================
# 2. POINT ANOMALY (Slide 9)
# =====================================================================
fig, ax = plt.subplots(figsize=(8.5, 4.8))
sample_normal = df[(df["is_actual_anomaly"] == 0)]["transaction_amount"].sample(300, random_state=1)
ax.scatter(range(len(sample_normal)), sample_normal, s=22, color=BLUE, alpha=0.6, label="Typical transactions (₦5k–₦500k)", zorder=3)
one_point = df[(df["is_actual_anomaly"] == 1) & (df["transaction_amount"] > 2_000_000)]["transaction_amount"].iloc[0]
ax.scatter([150], [one_point], s=220, color=RED, marker="*", zorder=5, label=f"One transaction: ₦{one_point:,.0f}")
style_ax(ax)
ax.set_xlabel("Transaction (sample)")
ax.set_ylabel("Amount (₦)")
ax.set_title("Point Anomaly — One Value Far Outside the Norm", fontsize=15, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "02_point_anomaly")

# =====================================================================
# 3. DISTANCE-BASED APPROACH (Slide 15)
# =====================================================================
rng = np.random.default_rng(5)
cluster = rng.normal(0, 0.6, (60, 2))
far_point = np.array([[5.2, 4.6]])
fig, ax = plt.subplots(figsize=(7, 5.4))
ax.scatter(cluster[:, 0], cluster[:, 1], s=32, color=BLUE, alpha=0.7, edgecolor="white", linewidth=0.4, zorder=3, label="Normal observations")
ax.scatter(far_point[:, 0], far_point[:, 1], s=200, color=RED, marker="*", zorder=5, label="Far from the group")
for pt in cluster[rng.choice(60, 6, replace=False)]:
    ax.plot([far_point[0,0], pt[0]], [far_point[0,1], pt[1]], color=MUTED, linewidth=0.7, alpha=0.5, zorder=2)
style_ax(ax)
ax.set_xlabel("Feature A"); ax.set_ylabel("Feature B")
ax.set_title("Distance-Based: Far From Everyone Else = Unusual", fontsize=14.5, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "03_distance_based")

# =====================================================================
# 4. DENSITY-BASED APPROACH (Slide 16)
# =====================================================================
dense1 = rng.normal([-2, 0], 0.35, (70, 2))
dense2 = rng.normal([2, 0.5], 0.35, (70, 2))
sparse_pt = np.array([[0.3, 3.2]])
fig, ax = plt.subplots(figsize=(7, 5.4))
ax.scatter(dense1[:, 0], dense1[:, 1], s=30, color=BLUE, alpha=0.7, edgecolor="white", linewidth=0.3, zorder=3, label="Dense region")
ax.scatter(dense2[:, 0], dense2[:, 1], s=30, color=TEAL, alpha=0.7, edgecolor="white", linewidth=0.3, zorder=3, label="Dense region")
ax.scatter(sparse_pt[:, 0], sparse_pt[:, 1], s=200, color=RED, marker="*", zorder=5, label="Sits in a sparse region")
style_ax(ax)
ax.set_xlabel("Feature A"); ax.set_ylabel("Feature B")
ax.set_title("Density-Based: Sparse Surroundings = Unusual", fontsize=14.5, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "04_density_based")

# =====================================================================
# 5. ISOLATION VISUAL — random splits isolate an outlier fast (Slide 18-19)
# =====================================================================
rng2 = np.random.default_rng(11)
normal_pts = rng2.normal(0, 1, (40, 2))
outlier_pt = np.array([4.3, 4.0])
all_pts = np.vstack([normal_pts, outlier_pt])

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
splits_outlier = [
    [(-6, 6, 2.1, "v")],
    [(-6, 6, 2.1, "v"), (2.1, 6, 1.9, "h")],
    [(-6, 6, 2.1, "v"), (2.1, 6, 1.9, "h"), (2.1, 6, 3.0, "v")],
]
titles = ["Split 1", "Split 2", "Split 3 — already isolated!"]
for ax, splits, title in zip(axes, splits_outlier, titles):
    ax.scatter(normal_pts[:, 0], normal_pts[:, 1], s=26, color=BLUE, alpha=0.55, zorder=3)
    ax.scatter([outlier_pt[0]], [outlier_pt[1]], s=170, color=RED, marker="*", zorder=5)
    for s in splits:
        lo, hi, pos, orient = s
        if orient == "v":
            ax.axvline(pos, color=AMBER, linewidth=2, zorder=4)
        else:
            ax.axhline(pos, color=AMBER, linewidth=2, zorder=4)
    ax.set_xlim(-6, 6); ax.set_ylim(-6, 6)
    style_ax(ax)
    ax.set_title(title, fontsize=13.5, weight="bold")
    ax.set_xticks([]); ax.set_yticks([])
save(fig, "05_isolation_outlier")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
normal_pt = np.array([-0.3, 0.2])
splits_normal = [
    [(-6, 6, 0.6, "v")],
    [(-6, 6, 0.6, "v"), (-6, 0.6, 0.1, "h")],
    [(-6, 6, 0.6, "v"), (-6, 0.6, 0.1, "h"), (-6, 0.6, -0.5, "v")],
]
titles2 = ["Split 1", "Split 2", "Split 3 — still surrounded by neighbours"]
for ax, splits, title in zip(axes, splits_normal, titles2):
    ax.scatter(normal_pts[:, 0], normal_pts[:, 1], s=26, color=BLUE, alpha=0.55, zorder=3)
    ax.scatter([normal_pt[0]], [normal_pt[1]], s=170, color=TEAL, marker="o", zorder=5, edgecolor=INK, linewidth=1.2)
    for s in splits:
        lo, hi, pos, orient = s
        if orient == "v":
            ax.axvline(pos, color=AMBER, linewidth=2, zorder=4)
        else:
            ax.axhline(pos, color=AMBER, linewidth=2, zorder=4)
    ax.set_xlim(-6, 6); ax.set_ylim(-6, 6)
    style_ax(ax)
    ax.set_title(title, fontsize=13.5, weight="bold")
    ax.set_xticks([]); ax.set_yticks([])
save(fig, "06_isolation_normal")

# =====================================================================
# 6. ANOMALY SCORE DISTRIBUTION (Slide 24)
# =====================================================================
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df[df["is_actual_anomaly"]==0]["anomaly_score"], bins=50, color=BLUE, alpha=0.75, label="Normal transactions", zorder=3)
ax.hist(df[df["is_actual_anomaly"]==1]["anomaly_score"], bins=50, color=RED, alpha=0.85, label="Unusual transactions", zorder=4)
style_ax(ax)
ax.set_xlabel("Anomaly Score (score_samples) — lower = more unusual")
ax.set_ylabel("Number of Transactions")
ax.set_title("Anomaly Scores: Normal vs. Unusual Transactions", fontsize=15, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "07_anomaly_score_distribution")

# =====================================================================
# 7. SCATTER: AMOUNT vs FREQUENCY, ANOMALIES HIGHLIGHTED (used in notebook + slide 27ish / visuals folder)
# =====================================================================
fig, ax = plt.subplots(figsize=(8.5, 5.6))
normal_rows = df[df["predicted_anomaly"] == 0]
anom_rows = df[df["predicted_anomaly"] == 1]
ax.scatter(normal_rows["transaction_amount"], normal_rows["transaction_frequency"], s=20, color=BLUE, alpha=0.45, zorder=3, label="Predicted normal")
ax.scatter(anom_rows["transaction_amount"], anom_rows["transaction_frequency"], s=45, color=RED, alpha=0.85, zorder=4, marker="x", label="Predicted anomaly")
ax.set_xscale("log")
style_ax(ax)
ax.set_xlabel("Transaction Amount (₦, log scale)")
ax.set_ylabel("Transaction Frequency (tx/hour)")
ax.set_title("Isolation Forest Output — Flagged Transactions", fontsize=14.5, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper right")
save(fig, "08_flagged_scatter")

# =====================================================================
# 8. CONTAMINATION COMPARISON (mini challenge, Slide 23 support)
# =====================================================================
contams = [0.01, 0.03, 0.05, "auto"]
flagged, tp, fp = [], [], []
for c in contams:
    m = IsolationForest(n_estimators=100, contamination=c, random_state=42).fit(Xs)
    pred = (m.predict(Xs) == -1).astype(int)
    flagged.append(pred.sum())
    tp.append(((pred==1)&(df["is_actual_anomaly"]==1)).sum())
    fp.append(((pred==1)&(df["is_actual_anomaly"]==0)).sum())

fig, ax = plt.subplots(figsize=(9, 5.2))
x = np.arange(len(contams))
w = 0.35
ax.bar(x - w/2, tp, width=w, color=GREEN, label="True positives (real anomalies caught)", zorder=3)
ax.bar(x + w/2, fp, width=w, color=RED, label="False positives (flagged normal transactions)", zorder=3)
style_ax(ax)
ax.set_xticks(x)
ax.set_xticklabels([f"contamination=\n{c}" for c in contams])
ax.set_ylabel("Number of Transactions")
ax.set_title("Changing contamination Changes What Gets Flagged", fontsize=14.5, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
for i, v in enumerate(flagged):
    ax.text(i, max(tp[i], fp[i]) + 8, f"{v} flagged", ha="center", fontsize=10.5, color=MUTED)
save(fig, "09_contamination_comparison")

# =====================================================================
# 9. HOUR / DISTANCE scatter highlighting contextual anomalies
# =====================================================================
fig, ax = plt.subplots(figsize=(8.5, 5.4))
normal_rows2 = df[df["is_actual_anomaly"] == 0]
anom_rows2 = df[df["is_actual_anomaly"] == 1]
ax.scatter(normal_rows2["transaction_hour"], normal_rows2["distance_from_usual_location_km"],
           s=20, color=BLUE, alpha=0.4, zorder=3, label="Normal")
ax.scatter(anom_rows2["transaction_hour"], anom_rows2["distance_from_usual_location_km"],
           s=45, color=RED, alpha=0.85, marker="x", zorder=4, label="Actual anomaly")
style_ax(ax)
ax.set_xlabel("Transaction Hour (0–23)")
ax.set_ylabel("Distance From Usual Location (km)")
ax.set_title("Contextual Anomalies: Late-Night + Far From Home", fontsize=14, weight="bold", color=INK, loc="left")
ax.legend(frameon=False, loc="upper left")
save(fig, "10_contextual_scatter")

print("\nAll visuals generated.")
print("Contamination sweep:", list(zip(contams, flagged, tp, fp)))
