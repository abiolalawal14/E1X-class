import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# Guided Exercise — Build Your First Collaborative Filtering Engine

**Scenario:** The movie streaming platform wants a working recommendation engine that
suggests movies to a user based on the behaviour of similar users.

You'll use the same `movie_ratings_dataset.csv` dataset from class. Cells marked `# TODO`
need you to fill something in — everywhere else is provided to keep things moving. If you get
stuck, the fully worked version is in `solutions/collaborative_filtering_solution.ipynb`, but
try this yourself first!

**Estimated time: 30-45 minutes.**"""))

cells.append(md("## Step 1 — Load the dataset"))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics.pairwise import cosine_similarity

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (9, 5.5)

# TODO: load "../data/movie_ratings_dataset.csv" into a DataFrame called ratings
ratings = ...  # YOUR CODE HERE

ratings.shape
"""))

cells.append(md("## Step 2 — Explore the data\n\nHow many unique users and movies are there?"))
cells.append(code("""
# TODO: compute n_users and n_movies
n_users = ...    # YOUR CODE HERE
n_movies = ...   # YOUR CODE HERE
print(f"Users: {n_users}, Movies: {n_movies}")
"""))

cells.append(md("## Step 3 — Create the user-item matrix\n\nUse `pivot_table()` with `index=\"user_id\"`, `columns=\"movie_title\"`, `values=\"rating\"`."))
cells.append(code("""
# TODO
user_item_matrix = ...  # YOUR CODE HERE
user_item_matrix.shape
"""))

cells.append(md("## Step 4 — Handle missing values\n\nFill missing ratings with 0 so we can compute similarity."))
cells.append(code("""
# TODO
user_item_filled = ...  # YOUR CODE HERE
"""))

cells.append(md("## Step 5 — Calculate user similarity\n\nUse `cosine_similarity()` on the filled matrix, and wrap the result in a labelled DataFrame."))
cells.append(code("""
# TODO
user_similarity = ...  # YOUR CODE HERE
user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_item_filled.index,
    columns=user_item_filled.index,
)
user_similarity_df.iloc[:5, :5].round(2)
"""))

cells.append(md("## Step 6 — Select a target user and find their most similar users\n\nPick any user ID from `user_item_matrix.index` and find their top 10 most similar users (excluding themselves)."))
cells.append(code("""
target_user = "U120"   # feel free to change this

# TODO: find the top 10 most similar users to target_user (excluding target_user itself)
similar_users = ...  # YOUR CODE HERE
similar_users
"""))

cells.append(md("## Step 7 — Identify movies the target user has NOT already rated"))
cells.append(code("""
# TODO
already_rated = ...  # YOUR CODE HERE (hint: user_item_matrix.loc[target_user].dropna().index)
print(f"{target_user} has already rated {len(already_rated)} movies")
"""))

cells.append(md("## Step 8 — Rank candidate movies and return the top 5\n\nFor each similar user, collect the movies they rated (excluding already-rated ones), weight "
                 "each rating by that user's similarity score, and rank the resulting weighted average."))
cells.append(code("""
# TODO: build weighted_scores and similarity_totals, then compute the ranked predictions
weighted_scores = pd.Series(dtype=float)
similarity_totals = pd.Series(dtype=float)

# YOUR CODE HERE — loop over similar_users, then over that user's ratings

top_5_recommendations = ...  # YOUR CODE HERE — (weighted_scores / similarity_totals), sorted, top 5
top_5_recommendations
"""))

cells.append(md("## Step 9 — Investigate: do the recommendations match the user's taste?\n\nLook up the genre of each recommended movie, and compare against the genres the user already rates highly."))
cells.append(code("""
genre_lookup = ratings.drop_duplicates("movie_title").set_index("movie_title")["genre"]

# TODO: show the genre of each recommended movie
...  # YOUR CODE HERE

# TODO: show the target user's favourite genre(s) from their highly-rated movies (rating >= 4)
...  # YOUR CODE HERE
"""))

cells.append(md("""## Step 10 — Answer these questions

1. Do the recommended movies mostly match the user's favourite genre? If not, why might that be?
2. What would happen if the target user had only rated 1 or 2 movies (a near cold-start user)?
3. What should the platform do with these recommendations — show them directly, or use them as
   one signal among several?"""))
cells.append(md("_Your answers here._"))

nb["cells"] = cells
save(nb, "collaborative_filtering_exercise.ipynb")
