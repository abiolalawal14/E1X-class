import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# Guided Exercise — SOLUTION

**Scenario:** The movie streaming platform wants a working recommendation engine that
suggests movies to a user based on the behaviour of similar users.

This is the fully worked solution to `exercises/collaborative_filtering_exercise.ipynb`. Try
the exercise yourself first — you'll learn more that way!"""))

cells.append(md("## Step 1 — Load the dataset"))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics.pairwise import cosine_similarity

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (9, 5.5)

ratings = pd.read_csv("../data/movie_ratings_dataset.csv")
ratings.shape
"""))

cells.append(md("## Step 2 — Explore the data"))
cells.append(code("""
n_users = ratings["user_id"].nunique()
n_movies = ratings["movie_id"].nunique()
print(f"Users: {n_users}, Movies: {n_movies}")
"""))

cells.append(md("## Step 3 — Create the user-item matrix"))
cells.append(code("""
user_item_matrix = ratings.pivot_table(index="user_id", columns="movie_title", values="rating")
user_item_matrix.shape
"""))

cells.append(md("## Step 4 — Handle missing values"))
cells.append(code("""
user_item_filled = user_item_matrix.fillna(0)
"""))

cells.append(md("## Step 5 — Calculate user similarity"))
cells.append(code("""
user_similarity = cosine_similarity(user_item_filled)
user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_item_filled.index,
    columns=user_item_filled.index,
)
user_similarity_df.iloc[:5, :5].round(2)
"""))

cells.append(md("## Step 6 — Select a target user and find their most similar users"))
cells.append(code("""
target_user = "U120"

similar_users = (
    user_similarity_df[target_user]
    .drop(target_user)
    .sort_values(ascending=False)
    .head(10)
)
similar_users
"""))

cells.append(md("## Step 7 — Identify movies the target user has NOT already rated"))
cells.append(code("""
already_rated = user_item_matrix.loc[target_user].dropna().index
print(f"{target_user} has already rated {len(already_rated)} movies")
"""))

cells.append(md("## Step 8 — Rank candidate movies and return the top 5"))
cells.append(code("""
weighted_scores = pd.Series(dtype=float)
similarity_totals = pd.Series(dtype=float)

for other_user, sim_score in similar_users.items():
    other_ratings = user_item_matrix.loc[other_user].dropna()
    for movie, rating in other_ratings.items():
        if movie in already_rated:
            continue
        weighted_scores[movie] = weighted_scores.get(movie, 0) + rating * sim_score
        similarity_totals[movie] = similarity_totals.get(movie, 0) + sim_score

top_5_recommendations = (weighted_scores / similarity_totals).sort_values(ascending=False).head(5)
top_5_recommendations
"""))

cells.append(md("## Step 9 — Investigate: do the recommendations match the user's taste?"))
cells.append(code("""
genre_lookup = ratings.drop_duplicates("movie_title").set_index("movie_title")["genre"]

print("Recommended movies and their genres:")
print(pd.DataFrame({
    "predicted_rating": top_5_recommendations.round(2),
    "genre": genre_lookup.reindex(top_5_recommendations.index),
}))

print(f"\\n{target_user}'s favourite genre(s) (from movies rated 4 or higher):")
print(ratings[(ratings.user_id == target_user) & (ratings.rating >= 4)]["genre"].value_counts())
"""))

cells.append(md("""## Step 10 — Answers

**1. Do the recommended movies mostly match the user's favourite genre?**
In most runs, yes — the majority of the top 5 recommendations share the user's dominant
genre, confirming that cosine similarity on rating patterns successfully rediscovers taste
clusters without ever being told about genre directly. A recommendation or two outside that
genre is normal — it usually comes from a "similar" user who also has some secondary taste
overlap, which is a realistic and expected part of real-world recommendation behaviour, not
a bug.

**2. What would happen with a near cold-start user (1-2 ratings)?**
With very little rating history, the similarity calculation has almost no signal to work
with — cosine similarity between that user and everyone else would likely be low or
unreliable, and the "similar users" found might not actually share real taste in common. This
is the COLD START problem from the slides in action: collaborative filtering genuinely
struggles here, and platforms typically fall back on other strategies for new users (e.g.
recommending currently popular items, or asking new users to rate a few movies at signup).

**3. What should the platform do with these recommendations?**
Treat them as ONE useful signal, not a final verdict — combine with business rules (e.g. don't
recommend content unsuitable for the user's region or age), monitor actual click-through /
watch-through rates to validate that the recommendations are working in practice, and keep
recalculating as the user rates more movies over time, since preferences and available data
both evolve."""))

nb["cells"] = cells
save(nb, "collaborative_filtering_solution.ipynb")
