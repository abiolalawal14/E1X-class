"""
Generates a synthetic movie-ratings dataset used throughout the Collaborative
Filtering course (slides, visuals, and notebooks).

The data is synthetic but designed with real LATENT STRUCTURE so that
collaborative filtering actually produces sensible, explainable results:
  - 60 movies span 6 genres (10 movies each).
  - Each user has a primary genre preference (and often a secondary one),
    and rates movies accordingly — high ratings for preferred-genre movies,
    lower ratings and much lower rating PROBABILITY for other genres.
  - This creates genuine clusters of similar users (same taste) and genuinely
    similar items (same genre, co-rated by the same kinds of users) — exactly
    what user-based and item-based collaborative filtering are meant to find.
  - The resulting user-item matrix is realistically SPARSE: each user rates
    only a small fraction of the 60 movies, never all of them.

Movie titles are entirely invented (no real film titles are used).

Run:
    python generate_data.py
Produces:
    movie_ratings_dataset.csv          (user_id, movie_id, movie_title, genre, rating)
    movies_catalog.csv                 (movie_id, movie_title, genre) — lookup table
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

GENRES = {
    "Action": ["Steel Vendetta", "Midnight Pursuit", "Iron Protocol", "Blackout Squad",
               "Apex Strike", "Rogue Circuit", "Last Stand Alpha", "Crimson Velocity",
               "Ghost Payload", "Titan Fall Zero"],
    "Comedy": ["The Wedding Disaster", "Office Chaos", "Roommates Anonymous",
               "Family Reunion Fiasco", "The Interview Trap", "Dog Sitter Diaries",
               "Vacation Gone Wrong", "The Prank War", "Blind Date Bingo", "Suburban Mayhem"],
    "Drama": ["Quiet Waters", "The Inheritance", "Letters Unsent", "A Winter's Promise",
              "The Long Goodbye", "Broken Compass", "Sunday's Child", "The Weight of Silence",
              "Fractured Light", "Where We Belong"],
    "Sci-Fi": ["Neon Horizon", "The Quantum Divide", "Colony Seven", "Echoes of Andromeda",
               "The Last Signal", "Synthetic Dawn", "Beyond the Rift", "Parallel Code",
               "The Singularity Gate", "Mars Protocol"],
    "Romance": ["Autumn in Paris", "The Coffee Shop Letters", "Second Chances",
                "Love at First Flight", "The Wedding Planner's Heart", "Rainy Day Promises",
                "Two Hearts, One City", "The Summer We Met", "Midnight Serenade",
                "Falling for You Again"],
    "Horror": ["The Basement", "Whispers in the Attic", "The Hollow House", "Nightfall Manor",
               "The Uninvited Guest", "Shadow Creek", "The Cellar Door", "Haunted Hollow",
               "The Night Watcher", "Cursed Static"],
}

movies = []
movie_id = 1
for genre, titles in GENRES.items():
    for title in titles:
        movies.append({"movie_id": f"M{movie_id:03d}", "movie_title": title, "genre": genre})
        movie_id += 1
movies_df = pd.DataFrame(movies)
movies_df.to_csv("movies_catalog.csv", index=False)
print(f"Catalog: {len(movies_df)} movies across {len(GENRES)} genres")

# ---------------------------------------------------------------- users --
N_USERS = 300
genre_names = list(GENRES.keys())

# Each user gets a primary genre and (usually) a secondary genre
primary_genre = rng.choice(genre_names, N_USERS)
has_secondary = rng.random(N_USERS) < 0.6
secondary_genre = np.array([
    rng.choice([g for g in genre_names if g != primary_genre[i]])
    if has_secondary[i] else None
    for i in range(N_USERS)
])

users_df = pd.DataFrame({
    "user_id": [f"U{100+i}" for i in range(N_USERS)],
    "primary_genre": primary_genre,
    "secondary_genre": secondary_genre,
})

# --------------------------------------------------------------- ratings --
rows = []
for _, user in users_df.iterrows():
    for _, movie in movies_df.iterrows():
        if movie["genre"] == user["primary_genre"]:
            watch_prob, mean_rating, sd = 0.75, 4.4, 0.6
        elif movie["genre"] == user["secondary_genre"]:
            watch_prob, mean_rating, sd = 0.45, 3.7, 0.7
        else:
            watch_prob, mean_rating, sd = 0.06, 2.7, 0.9

        if rng.random() < watch_prob:
            rating = rng.normal(mean_rating, sd)
            rating = int(np.clip(round(rating), 1, 5))
            rows.append({
                "user_id": user["user_id"],
                "movie_id": movie["movie_id"],
                "movie_title": movie["movie_title"],
                "genre": movie["genre"],
                "rating": rating,
            })

ratings_df = pd.DataFrame(rows)
ratings_df = ratings_df.sample(frac=1, random_state=42).reset_index(drop=True)
ratings_df.to_csv("movie_ratings_dataset.csv", index=False)

print(f"Ratings: {len(ratings_df)} rows")
print(f"Users who rated at least 1 movie: {ratings_df['user_id'].nunique()} / {N_USERS}")
print(f"Movies rated at least once: {ratings_df['movie_id'].nunique()} / {len(movies_df)}")
n_possible = N_USERS * len(movies_df)
sparsity = 1 - len(ratings_df) / n_possible
print(f"Matrix sparsity: {sparsity*100:.1f}% of user-movie pairs are unrated")
print(f"Ratings per user: min={ratings_df.groupby('user_id').size().min()}, "
      f"median={ratings_df.groupby('user_id').size().median():.0f}, "
      f"max={ratings_df.groupby('user_id').size().max()}")
print(ratings_df.head())
