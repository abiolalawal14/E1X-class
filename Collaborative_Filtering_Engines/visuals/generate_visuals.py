"""
Generates every matplotlib chart used in the Collaborative Filtering slide
deck and notebooks. Run from this folder:  python generate_visuals.py
Reads ../data/movie_ratings_dataset.csv, writes PNGs here.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

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
GENRE_COLORS = {"Action": RED, "Comedy": AMBER, "Drama": PURPLE, "Sci-Fi": BLUE,
                 "Romance": "#DB2777", "Horror": "#374151"}

def style_ax(ax, grid=True):
    if grid:
        ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

def save(fig, name, dpi=220):
    fig.tight_layout()
    fig.savefig(f"{name}.png", dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)

ratings = pd.read_csv("../data/movie_ratings_dataset.csv")
movies = pd.read_csv("../data/movies_catalog.csv")

uim = ratings.pivot_table(index="user_id", columns="movie_title", values="rating")
uim_filled = uim.fillna(0)

# =====================================================================
# 1. RATING DISTRIBUTION (Notebook 01 / general)
# =====================================================================
fig, ax = plt.subplots(figsize=(8, 5))
ratings["rating"].value_counts().sort_index().plot(kind="bar", color=BLUE, ax=ax, zorder=3)
style_ax(ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Ratings")
ax.set_title("Rating Distribution", fontsize=15, weight="bold", color=INK, loc="left")
plt.setp(ax.get_xticklabels(), rotation=0)
save(fig, "01_rating_distribution")

# =====================================================================
# 2. RATINGS PER USER histogram (sparsity illustration, Slide/notebook)
# =====================================================================
fig, ax = plt.subplots(figsize=(8, 5))
counts = ratings.groupby("user_id").size()
ax.hist(counts, bins=range(counts.min(), counts.max()+2), color=TEAL, zorder=3)
style_ax(ax)
ax.set_xlabel("Number of Movies Rated")
ax.set_ylabel("Number of Users")
ax.set_title(f"Most Users Rate Only a Small Fraction of the {len(movies)} Movies",
             fontsize=13.5, weight="bold", color=INK, loc="left")
save(fig, "02_ratings_per_user")

# =====================================================================
# 3. MOST-RATED MOVIES (Notebook 01)
# =====================================================================
top_movies = ratings.groupby("movie_title").size().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(9, 5.5))
colors = [GENRE_COLORS[movies.set_index("movie_title").loc[m, "genre"]] for m in top_movies.index]
ax.barh(top_movies.index[::-1], top_movies.values[::-1], color=colors[::-1], zorder=3)
style_ax(ax)
ax.set_xlabel("Number of Ratings")
ax.set_title("Top 10 Most-Rated Movies", fontsize=15, weight="bold", color=INK, loc="left")
save(fig, "03_most_rated_movies")

# =====================================================================
# 4. USER-ITEM MATRIX HEATMAP (small illustrative subset) — Slide 11
# =====================================================================
sub_users = ["U100", "U101", "U102", "U103", "U104"]
sub_movies_idx = uim.columns[:8]
sub = uim.loc[[u for u in sub_users if u in uim.index], sub_movies_idx]
fig, ax = plt.subplots(figsize=(9, 3.6))
im = ax.imshow(sub.values, cmap="Blues", vmin=0, vmax=5, aspect="auto")
ax.set_xticks(range(len(sub.columns)))
ax.set_xticklabels(sub.columns, rotation=35, ha="right", fontsize=10)
ax.set_yticks(range(len(sub.index)))
ax.set_yticklabels(sub.index)
for i in range(sub.shape[0]):
    for j in range(sub.shape[1]):
        v = sub.values[i, j]
        txt = f"{v:.0f}" if not np.isnan(v) else "?"
        color = "white" if (not np.isnan(v) and v >= 3) else INK
        ax.text(j, i, txt, ha="center", va="center", fontsize=11, color=color, weight="bold")
ax.set_title("A Small Slice of the User-Item Matrix", fontsize=14.5, weight="bold", color=INK, loc="left")
for spine in ax.spines.values():
    spine.set_visible(False)
save(fig, "04_user_item_matrix_heatmap")

# =====================================================================
# 5. FULL SPARSITY HEATMAP (Slide / notebook illustration)
# =====================================================================
fig, ax = plt.subplots(figsize=(9, 6))
mask = uim.notna().values.astype(float)
ax.imshow(mask, cmap="Blues", aspect="auto", vmin=0, vmax=1)
ax.set_xlabel("Movies (60)")
ax.set_ylabel("Users (300)")
ax.set_title("The Full User-Item Matrix Is Mostly Empty", fontsize=15, weight="bold", color=INK, loc="left")
ax.set_xticks([]); ax.set_yticks([])
save(fig, "05_full_sparsity_heatmap")

# =====================================================================
# 6. SIMILARITY INTUITION — vectors as directions (Slide 21, cosine similarity)
# =====================================================================
fig, ax = plt.subplots(figsize=(7, 6))
origin = np.array([0, 0])
# Two similar users (small angle) and one dissimilar
v1 = np.array([4, 3.6])
v2 = np.array([3.6, 4])
v3 = np.array([1, -4])
for v, c, label in [(v1, BLUE, "John"), (v2, TEAL, "Mary (similar)"), (v3, RED, "David (different)")]:
    ax.annotate("", xy=v, xytext=origin, arrowprops=dict(arrowstyle="-|>", color=c, lw=3))
    ax.text(v[0]*1.08, v[1]*1.08, label, color=c, fontsize=13, weight="bold")
ax.set_xlim(-5, 5.5); ax.set_ylim(-5, 5.5)
ax.axhline(0, color=GRID, linewidth=1); ax.axvline(0, color=GRID, linewidth=1)
ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Similarity as Direction — Closer Angle = More Similar", fontsize=13.5, weight="bold", color=INK, loc="left")
for spine in ax.spines.values():
    spine.set_visible(False)
save(fig, "06_cosine_similarity_intuition")

# =====================================================================
# 7. USER SIMILARITY TABLE-STYLE BAR CHART (Slide 15 / notebook)
# =====================================================================
sim = cosine_similarity(uim_filled)
sim_df = pd.DataFrame(sim, index=uim.index, columns=uim.index)
target_user = "U100"
top_sim = sim_df[target_user].drop(target_user).sort_values(ascending=False).head(8)
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.barh(top_sim.index[::-1], top_sim.values[::-1], color=BLUE, zorder=3)
style_ax(ax)
ax.set_xlabel("Cosine Similarity to U100")
ax.set_title(f"Users Most Similar to {target_user}", fontsize=15, weight="bold", color=INK, loc="left")
ax.set_xlim(0, 1)
save(fig, "07_user_similarity_bar")

# =====================================================================
# 8. ITEM SIMILARITY BAR CHART
# =====================================================================
item_sim = cosine_similarity(uim_filled.T)
item_sim_df = pd.DataFrame(item_sim, index=uim.columns, columns=uim.columns)
target_movie = "Steel Vendetta"
top_item_sim = item_sim_df[target_movie].drop(target_movie).sort_values(ascending=False).head(8)
fig, ax = plt.subplots(figsize=(8.5, 5))
mv_genre = movies.set_index("movie_title")["genre"]
colors = [GENRE_COLORS[mv_genre[m]] for m in top_item_sim.index]
ax.barh(top_item_sim.index[::-1], top_item_sim.values[::-1], color=colors[::-1], zorder=3)
style_ax(ax)
ax.set_xlabel(f"Cosine Similarity to \"{target_movie}\"")
ax.set_title(f"Movies Most Similar to \"{target_movie}\"", fontsize=14, weight="bold", color=INK, loc="left")
ax.set_xlim(0, 1)
save(fig, "08_item_similarity_bar")

# =====================================================================
# 9. PRECISION/RECALL @K illustration (Slide 24-25)
# =====================================================================
fig, ax = plt.subplots(figsize=(9, 5))
recommended = ["Movie C", "Movie D", "Movie E", "Movie F", "Movie G"]
relevant_flags = [True, False, True, False, True]  # 3 of 5 relevant -> precision@5 = 0.6
colors = [GREEN if r else "#E5E7EB" for r in relevant_flags]
ax.barh(recommended[::-1], [1]*5, color=colors[::-1], zorder=3, edgecolor=INK, linewidth=0.6)
for i, (m, r) in enumerate(zip(recommended[::-1], relevant_flags[::-1])):
    ax.text(0.5, i, "Relevant" if r else "Not relevant", ha="center", va="center",
            fontsize=11, color="white" if r else MUTED, weight="bold")
ax.set_xlim(0, 1)
ax.set_xticks([])
ax.set_title("Precision@5 = 3 Relevant / 5 Recommended = 0.6", fontsize=14.5, weight="bold", color=INK, loc="left")
save(fig, "09_precision_at_k")

# =====================================================================
# 10. GENRE DISTRIBUTION OF RATINGS (business/data understanding)
# =====================================================================
genre_counts = ratings["genre"].value_counts()
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.bar(genre_counts.index, genre_counts.values, color=[GENRE_COLORS[g] for g in genre_counts.index], zorder=3)
style_ax(ax)
ax.set_ylabel("Number of Ratings")
ax.set_title("Ratings by Genre", fontsize=15, weight="bold", color=INK, loc="left")
save(fig, "10_genre_distribution")

print("\nAll visuals generated.")
