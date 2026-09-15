# Instructor Guide — 2-Hour Delivery Plan

**Course:** Building Collaborative Filtering Engines
**Audience:** Beginner Data Scientists (comfortable with Python, Pandas, basic ML)
**Format:** Hour 1 conceptual (slides), Hour 2 hands-on (Jupyter notebooks)

The whole session is one connected story: *"Can we recommend something to a user based on the
behaviour and preferences of other users?"* Keep returning to the movie-streaming example
(John, Mary, David and their overlapping tastes) throughout — this is not a tour of separate
algorithms.

---

## Before class

- Open `Collaborative_Filtering_Engines_Beginner_Course.pptx` in Google Slides or PowerPoint
  and skim speaker notes once.
- Confirm `data/movie_ratings_dataset.csv` and `data/movies_catalog.csv` exist (regenerate with
  `python data/generate_data.py` if needed — it's deterministic, `random_state=42`).
- Have `notebooks/01` through `04` open and pre-run once so you're not debugging live.
- Decide whether students code along in real time or watch you build 01-04 and then do
  `exercises/collaborative_filtering_exercise.ipynb` themselves — the timing below assumes the
  latter.

---

## Hour 1 — Concepts (Slides 1–33)

| Time | Slides | Focus |
|---|---|---|
| 0–10 min | 1–4 | Title, learning objectives, why recommendations matter, the movie streaming problem |
| 10–20 min | 5–8 | What is a recommender system, users/items, interactions |
| 20–30 min | 9–12 | Explicit vs. implicit feedback, the user-item matrix, the big question |
| 30–40 min | 13–16 | Collaborative filtering intuition, user-based filtering |
| 40–50 min | 17–21 | Item-based filtering, comparison, similarity, cosine similarity |
| 50–57 min | 22–26 | The recommendation pipeline, making a recommendation, evaluation, top-K, real-world challenges |
| 57–60 min | 27–30 | Common mistakes, business value, recap, transition to coding |

**Pacing notes:**
- Slide 13 (the simple idea) and Slides 20–21 (similarity/cosine similarity) are the two
  concepts worth slowing down for — everything else in the course builds on them. Don't rush.
- If you're behind schedule, the safest slides to compress are 6 (industry examples) and
  28 (business value) — read briskly, since they're supporting context rather than core
  mechanics.
- Slides 31–32 (misconceptions table, quiz) can be run as a quick group call-and-response
  rather than individual writing, to protect time. Full answer key is in the quiz slide's
  speaker notes.

---

## Hour 2 — Hands-On Coding

| Time | Activity | Notebook |
|---|---|---|
| 60–70 min | Load and understand the dataset | `notebooks/01_Recommender_System_Introduction.ipynb` |
| 70–80 min | Create the user-item matrix | `notebooks/02_User_Based_Collaborative_Filtering.ipynb` (Steps 1-2) |
| 80–95 min | Build user-based collaborative filtering | `notebooks/02` (Steps 3-4) |
| 95–105 min | Generate recommendations | `notebooks/02` (Step 5) |
| 105–112 min | Build item-based collaborative filtering | `notebooks/03_Item_Based_Collaborative_Filtering.ipynb` |
| 112–117 min | Mini challenge | `notebooks/04_Collaborative_Filtering_Mini_Project.ipynb` (mini challenge section) |
| 117–120 min | Recap and discussion | `notebooks/04` (recap) |

**Delivery notes:**
- All four main notebooks have been executed end-to-end with no errors under the current
  pandas/scikit-learn versions — you should not hit install or environment surprises live.
- Real numbers on this dataset to anchor discussion: 300 users, 60 movies, ~3,800 ratings,
  ~78.7% sparsity. User U100's top similar users and recommendations are almost entirely
  Action movies (their known genre) — a clean, visually convincing demonstration that cosine
  similarity rediscovers taste purely from rating patterns, with no genre label ever given to
  the algorithm.
- The Precision@5 / Recall@5 evaluation in Notebook 04 (hide-some-known-likes-and-check)
  typically lands around Precision@5 ≈ 0.3, Recall@5 ≈ 0.7 on this dataset — good numbers to
  quote if a live re-run produces something different (randomness in the hidden-movie sampling
  will shift results slightly run to run).
- `exercises/collaborative_filtering_exercise.ipynb` is intentionally incomplete (`# TODO`
  cells with `...` placeholders) — it will NOT run as downloaded. That's by design: assign it
  as the 30–45 minute capstone to complete after class, or as a guided in-class exercise if
  time allows. `solutions/collaborative_filtering_solution.ipynb` is the fully worked, executed
  reference, using target user "U120" (a Sci-Fi-leaning user) rather than "U100," so it's
  recognizably its own worked example.
- Close Hour 2 by returning explicitly to the business-value questions (Slide 28 /
  Notebook 04's final section): a recommendation engine only matters once it changes what users
  actually see and do on the platform.

---

## Common questions to anticipate

- **"Why fill missing ratings with 0 instead of the average rating?"** — Simplicity for a
  first pass; filling with 0 is the standard beginner-friendly approach and works reasonably
  well here because 0 doesn't overlap with the real 1-5 rating scale. Mention (briefly) that
  production systems often mean-center ratings first (subtracting each user's average) — this
  is the "adjusted cosine similarity" from the textbook, intentionally not taught in depth
  today.
- **"Why cosine similarity and not Pearson correlation?"** — Cosine similarity is simpler to
  explain intuitively (direction/angle) and is what `sklearn.metrics.pairwise.cosine_similarity`
  provides directly. Pearson correlation (used in the textbook) additionally corrects for each
  user's personal rating bias (some people rate everything a 5) — a good "going deeper" note
  for advanced learners, not required for today's session.
- **"Isn't recommending movies I've already rated pointless?"** — Exactly right, and that's why
  every recommendation function explicitly filters out `already_rated` movies — point students
  to that specific line of code if this question comes up.
- **"What if two approaches (user-based vs. item-based) disagree?"** — That's normal and
  expected; Notebook 04's comparison section shows this directly. In practice, teams often
  blend both, or A/B test which performs better for their specific platform and user base.
