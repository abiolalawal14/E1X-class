import sys, os
sys.path.insert(0, os.path.abspath(".."))
from nb_helpers import new_notebook, md, code, save

nb = new_notebook()
cells = []

cells.append(md("""# 01 — Recommender System Introduction

**Hour 2, 60–70 min: Understanding the data**

We're picking up the story from the slides: a movie streaming platform wants to recommend
movies to its users based on the patterns in what similar users have liked. Before we build
anything, we need to load the ratings data and understand its shape.

By the end of this notebook you will have:
- Loaded the movie ratings dataset
- Counted users, movies, and ratings
- Checked how sparse the data is (most users only rate a handful of movies)
- Visualized the most-rated movies, the rating distribution, and ratings-per-user"""))

cells.append(md("## Step 1 — Import Libraries"))
cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", 20)
plt.rcParams["figure.figsize"] = (9, 5)
"""))

cells.append(md("""## Step 2 — Load the Dataset

`movie_ratings_dataset.csv` is a **synthetic** dataset built to feel like real movie ratings
data. Movie titles are entirely invented — this does not represent any real streaming
platform, user, or film."""))
cells.append(code("""
ratings = pd.read_csv("../data/movie_ratings_dataset.csv")
ratings.shape
"""))
cells.append(code("""
ratings.head()
"""))

cells.append(md("""## Step 3 — Explore

Here's what each column means:

| Column | Meaning |
|---|---|
| `user_id` | Unique ID for the user who gave the rating |
| `movie_id` | Unique ID for the movie |
| `movie_title` | The movie's title |
| `genre` | The movie's genre (included for teaching purposes, to help us sanity-check our results) |
| `rating` | The user's rating, 1–5 (explicit feedback) |"""))
cells.append(code("""
n_users = ratings["user_id"].nunique()
n_movies = ratings["movie_id"].nunique()
n_ratings = len(ratings)

print(f"Users:   {n_users}")
print(f"Movies:  {n_movies}")
print(f"Ratings: {n_ratings}")
"""))

cells.append(md("""**How sparse is this data?** If every user had rated every movie, we'd have
`n_users x n_movies` ratings. Let's see what fraction of that is actually filled in."""))
cells.append(code("""
max_possible = n_users * n_movies
sparsity = 1 - n_ratings / max_possible
print(f"Maximum possible user-movie pairs: {max_possible}")
print(f"Actual ratings given: {n_ratings}")
print(f"Sparsity: {sparsity*100:.1f}% of the matrix is EMPTY (unrated)")
"""))
cells.append(md("**Business perspective:** Almost 4 out of every 5 possible user-movie pairs have no rating "
                 "at all. This is completely normal for recommendation data — no user has time to watch and "
                 "rate every movie on the platform. This is exactly the SPARSE DATA challenge from the slides, "
                 "and it's the reason we can't simply 'look up' what a user thinks of an unrated movie — we "
                 "have to predict it."))

cells.append(md("### Any missing values in the columns themselves?"))
cells.append(code("""
ratings.isna().sum()
"""))
cells.append(md("No missing values in the columns we loaded — every row is a complete (user, movie, rating) "
                 "record. The 'missing values' we care about for recommendations are the user-movie PAIRS "
                 "that never appear as a row at all, which we already measured above as sparsity."))

cells.append(md("""## Step 4 — Visualize Basic Information

### Rating distribution"""))
cells.append(code("""
fig, ax = plt.subplots()
ratings["rating"].value_counts().sort_index().plot(kind="bar", color="#2563EB", ax=ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Ratings")
ax.set_title("Rating Distribution")
plt.xticks(rotation=0)
plt.show()
"""))
cells.append(md("**What do we see?** Ratings skew toward the higher end — this makes sense: our synthetic "
                 "users mostly rate movies they *chose to watch*, and they tend to choose movies in genres "
                 "they already like."))

cells.append(md("### Most-rated movies"))
cells.append(code("""
top_movies = ratings.groupby("movie_title").size().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(top_movies.index[::-1], top_movies.values[::-1], color="#0D9488")
ax.set_xlabel("Number of Ratings")
ax.set_title("Top 10 Most-Rated Movies")
plt.show()
"""))

cells.append(md("### Number of ratings per user\n\nHow many movies does a typical user rate?"))
cells.append(code("""
ratings_per_user = ratings.groupby("user_id").size()

fig, ax = plt.subplots()
ax.hist(ratings_per_user, bins=range(ratings_per_user.min(), ratings_per_user.max() + 2), color="#7C3AED")
ax.set_xlabel("Number of Movies Rated")
ax.set_ylabel("Number of Users")
ax.set_title("Ratings per User")
plt.show()

print(ratings_per_user.describe())
"""))
cells.append(md("""**What do we see?** Most users rate somewhere between about 6 and 22 movies — a small
fraction of the full 60-movie catalog. This confirms, visually, the sparsity number we calculated above.

### Recap
- We loaded the ratings dataset and counted users, movies, and ratings.
- We measured sparsity directly — most user-movie pairs are unrated, which is the normal, expected
  situation for recommendation data.
- We visualized the rating distribution, the most-rated movies, and how many movies a typical
  user rates.

**Next: `02_User_Based_Collaborative_Filtering.ipynb`** — where we turn this data into a
user-item matrix and start finding similar users."""))

nb["cells"] = cells
save(nb, "01_Recommender_System_Introduction.ipynb")
