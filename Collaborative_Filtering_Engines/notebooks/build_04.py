import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# 04 — Collaborative Filtering Mini Project

**Hour 2, 112–120 min: Compare approaches, evaluate, and the mini challenge**

In this final notebook we:
1. Compare user-based vs. item-based recommendations side by side
2. Build a simple Precision@K / Recall@K evaluation using a held-out test set
3. Run the mini challenge — build the "recommend top 5 movies for a user" pipeline yourself
4. Wrap everything into one complete, reusable function — your first real collaborative
   filtering engine, end to end"""))

cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics.pairwise import cosine_similarity

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (9, 5.5)

ratings = pd.read_csv("../data/movie_ratings_dataset.csv")
genre_lookup = ratings.drop_duplicates("movie_title").set_index("movie_title")["genre"]

user_item_matrix = ratings.pivot_table(index="user_id", columns="movie_title", values="rating")
user_item_filled = user_item_matrix.fillna(0)

user_similarity_df = pd.DataFrame(
    cosine_similarity(user_item_filled), index=user_item_filled.index, columns=user_item_filled.index)
item_similarity_df = pd.DataFrame(
    cosine_similarity(user_item_filled.T), index=user_item_filled.columns, columns=user_item_filled.columns)
"""))

cells.append(md("""## Compare Both Approaches"""))
cells.append(code("""
def recommend_movies_user_based(user_id, top_n=5, n_similar_users=10):
    similar = user_similarity_df[user_id].drop(user_id).sort_values(ascending=False).head(n_similar_users)
    already_rated = user_item_matrix.loc[user_id].dropna().index

    weighted_scores, similarity_totals = pd.Series(dtype=float), pd.Series(dtype=float)
    for other_user, sim_score in similar.items():
        for movie, rating in user_item_matrix.loc[other_user].dropna().items():
            if movie in already_rated:
                continue
            weighted_scores[movie] = weighted_scores.get(movie, 0) + rating * sim_score
            similarity_totals[movie] = similarity_totals.get(movie, 0) + sim_score

    if len(weighted_scores) == 0:
        return pd.Series(dtype=float)
    return (weighted_scores / similarity_totals).sort_values(ascending=False).head(top_n)


def recommend_movies_item_based(user_id, top_n=5, liked_threshold=4):
    user_ratings = user_item_matrix.loc[user_id].dropna()
    liked_movies = user_ratings[user_ratings >= liked_threshold].index
    already_rated = user_ratings.index

    scores = pd.Series(dtype=float)
    for movie in liked_movies:
        for other_movie, sim_score in item_similarity_df[movie].drop(movie, errors="ignore").items():
            if other_movie in already_rated:
                continue
            scores[other_movie] = scores.get(other_movie, 0) + sim_score
    return scores.sort_values(ascending=False).head(top_n)


target_user = "U100"
user_based = recommend_movies_user_based(target_user)
item_based = recommend_movies_item_based(target_user)

print("USER-BASED recommendations for", target_user)
print(pd.DataFrame({"score": user_based.round(2), "genre": genre_lookup.reindex(user_based.index)}))
print()
print("ITEM-BASED recommendations for", target_user)
print(pd.DataFrame({"score": item_based.round(2), "genre": genre_lookup.reindex(item_based.index)}))
"""))

cells.append(md("""**Discussion:** The two lists won't be identical, but they should mostly agree on GENRE —
that's a good sign both approaches are picking up the same underlying signal from two different
angles. In practice, teams often use both and blend the results, or A/B test which performs
better for their specific platform."""))

cells.append(md("""## Simple Evaluation: Precision@K and Recall@K

**The idea:** hide a few of a user's ACTUAL highly-rated movies (pretend we don't know about
them), generate recommendations without that information, and check how many of the hidden
movies show up in our top-K recommendations."""))
cells.append(code("""
import random
random.seed(42)

def evaluate_user(user_id, k=5, hide_fraction=0.3):
    \"\"\"
    Hides a fraction of a user's liked (rating >= 4) movies, regenerates the user-item
    matrix without them, and checks whether the hidden movies appear in the top-K
    recommendations.
    \"\"\"
    user_ratings = ratings[ratings.user_id == user_id]
    liked = user_ratings[user_ratings.rating >= 4]
    if len(liked) < 3:
        return None  # not enough liked movies to test meaningfully

    n_hide = max(1, int(len(liked) * hide_fraction))
    hidden_movies = set(random.sample(list(liked["movie_title"]), n_hide))

    # Build a temporary ratings table with the hidden movies removed for this user only
    mask = ~((ratings.user_id == user_id) & (ratings.movie_title.isin(hidden_movies)))
    temp_ratings = ratings[mask]

    temp_matrix = temp_ratings.pivot_table(index="user_id", columns="movie_title", values="rating")
    temp_filled = temp_matrix.fillna(0)
    temp_user_sim = pd.DataFrame(cosine_similarity(temp_filled), index=temp_filled.index, columns=temp_filled.index)

    similar = temp_user_sim[user_id].drop(user_id).sort_values(ascending=False).head(10)
    already_rated = temp_matrix.loc[user_id].dropna().index

    weighted_scores, similarity_totals = pd.Series(dtype=float), pd.Series(dtype=float)
    for other_user, sim_score in similar.items():
        for movie, rating in temp_matrix.loc[other_user].dropna().items():
            if movie in already_rated:
                continue
            weighted_scores[movie] = weighted_scores.get(movie, 0) + rating * sim_score
            similarity_totals[movie] = similarity_totals.get(movie, 0) + sim_score

    if len(weighted_scores) == 0:
        return None
    top_k = set((weighted_scores / similarity_totals).sort_values(ascending=False).head(k).index)

    hits = len(top_k & hidden_movies)
    precision = hits / k
    recall = hits / len(hidden_movies)
    return precision, recall


results = [evaluate_user(u, k=5) for u in user_item_matrix.index[:60]]
results = [r for r in results if r is not None]

precisions = [r[0] for r in results]
recalls = [r[1] for r in results]
print(f"Evaluated {len(results)} users")
print(f"Average Precision@5: {np.mean(precisions):.2f}")
print(f"Average Recall@5:    {np.mean(recalls):.2f}")
"""))

cells.append(md("""**Business language:** Precision@5 around this level means that, on average, a solid
fraction of our top-5 recommendations for a user turn out to be movies they actually liked
(among those we deliberately hid). Recall@5 tells us how much of a user's full set of liked
movies we managed to surface in just 5 recommendations — naturally lower, since we're only
showing a handful of items out of everything the user might enjoy.

**Important honesty check:** this evaluation is simplified for teaching purposes — real
recommender evaluation is more nuanced (e.g. accounting for popularity bias, ranking position,
not just presence/absence). But the core idea — hide some known-good answers, see if your
system finds them — is the right starting intuition."""))

cells.append(md("""## Mini Challenge

**Task:** Build a recommendation engine that recommends the top 5 movies for a selected user,
from scratch, using the steps below. Try picking a DIFFERENT user than `U100` to see how the
recommendations change."""))
cells.append(code("""
# TRY IT YOURSELF — change this user ID
my_user = "U150"

# 1. Create the user-item matrix (already done above as user_item_matrix)
# 2. Calculate similarity (already done above as user_similarity_df)
# 3. Select similar users
my_similar_users = user_similarity_df[my_user].drop(my_user).sort_values(ascending=False).head(10)

# 4. Identify unseen movies + 5. Rank + 6. Return top 5
my_recommendations = recommend_movies_user_based(my_user, top_n=5)

print(f"Top 5 recommendations for {my_user}:\\n")
for i, (movie, score) in enumerate(my_recommendations.items(), start=1):
    print(f"{i}. {movie}  (predicted rating: {score:.2f}, genre: {genre_lookup[movie]})")

print(f"\\n{my_user}'s actual favourite genre (from their highly-rated movies):")
print(ratings[(ratings.user_id == my_user) & (ratings.rating >= 4)]["genre"].value_counts())
"""))
cells.append(md("**Ask yourself:** why were these specific movies recommended? Do they match the genre this "
                 "user already rates highly? If a recommendation looks 'wrong,' look at which similar users "
                 "drove that score — sometimes a user has mixed tastes, and that's a completely realistic, "
                 "expected outcome, not a bug."))

cells.append(md("""## The Complete Engine

Let's wrap the full pipeline into ONE function you could hand to someone else to use."""))
cells.append(code("""
def build_collaborative_filtering_engine(csv_path):
    \"\"\"
    Loads ratings data and returns a ready-to-use recommend(user_id, top_n) function —
    a complete, self-contained collaborative filtering engine.
    \"\"\"
    data = pd.read_csv(csv_path)
    uim = data.pivot_table(index="user_id", columns="movie_title", values="rating")
    uim_filled = uim.fillna(0)
    user_sim = pd.DataFrame(cosine_similarity(uim_filled), index=uim_filled.index, columns=uim_filled.index)

    def recommend(user_id, top_n=5):
        similar = user_sim[user_id].drop(user_id).sort_values(ascending=False).head(10)
        already_rated = uim.loc[user_id].dropna().index

        weighted_scores, similarity_totals = pd.Series(dtype=float), pd.Series(dtype=float)
        for other_user, sim_score in similar.items():
            for movie, rating in uim.loc[other_user].dropna().items():
                if movie in already_rated:
                    continue
                weighted_scores[movie] = weighted_scores.get(movie, 0) + rating * sim_score
                similarity_totals[movie] = similarity_totals.get(movie, 0) + sim_score

        if len(weighted_scores) == 0:
            return pd.Series(dtype=float)
        return (weighted_scores / similarity_totals).sort_values(ascending=False).head(top_n)

    return recommend


recommend = build_collaborative_filtering_engine("../data/movie_ratings_dataset.csv")

print("Recommendations for U205:\\n")
for i, (movie, score) in enumerate(recommend("U205", top_n=5).items(), start=1):
    print(f"{i}. {movie}")
"""))

cells.append(md("""### Recap — you have now built a complete, working collaborative filtering engine:

Raw ratings → cleaned into a user-item matrix → similarity calculated → similar users found →
unseen movies identified → scores ranked → top recommendations returned → evaluated with
Precision@K / Recall@K.

This is the exact shape of a real-world recommender system, just with a simpler similarity
method and smaller data than production platforms use. The workflow itself does not change
much as systems scale up — only the similarity/scoring step usually gets replaced with more
sophisticated techniques (matrix factorization, neural collaborative filtering) for very large
platforms, which is exactly where a future course would pick up."""))

nb["cells"] = cells
save(nb, "04_Collaborative_Filtering_Mini_Project.ipynb")
