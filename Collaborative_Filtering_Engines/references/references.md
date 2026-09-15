# References / Sources

## Textbook

- Aggarwal, C. C. (2015). *Data Mining: The Textbook*. Springer.
  Section 18.5, "Recommender Systems" — utility matrices (ratings-based vs. positive-preference),
  content-based vs. collaborative filtering, and neighborhood-based methods (user-based
  similarity with ratings, item-based / adjusted cosine similarity, graph-based methods). Used
  as the primary conceptual reference for the user-item matrix, sparsity, and user-based /
  item-based collaborative filtering in this course.
  Note: the textbook's treatment includes formal similarity mathematics (the Pearson
  correlation coefficient with mean-centering, adjusted cosine similarity, graph/PageRank-based
  neighborhoods) that is graduate-level and was deliberately NOT carried into this beginner
  course — only the underlying ideas and a simplified, un-adjusted cosine similarity were used.
  Matrix factorization and graph-based methods are flagged as out of scope for this session and
  left for a later course.

## Official Documentation (verified for current syntax during course development)

- scikit-learn: `sklearn.metrics.pairwise.cosine_similarity`
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
- pandas API Reference: `DataFrame.pivot_table()`
  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot_table.html

Every code snippet in the slide deck and notebooks was checked against these pages during
course development (September 2026) to confirm current, non-deprecated behaviour.

## Evaluation Concepts

Precision@K and Recall@K definitions were cross-checked against standard recommender-systems
evaluation references, since the primary textbook does not cover these metrics explicitly:
- Precision@K: of the K items recommended, what fraction were relevant?
- Recall@K: of all the relevant items available, what fraction appeared in the top K
  recommendations?

These are widely used, standard definitions in recommender-systems literature and are not
specific to any single library or tool.

## Data

All ratings data used in this course (`data/movie_ratings_dataset.csv`,
`data/movies_catalog.csv`) is **synthetic**, generated for teaching purposes by
`data/generate_data.py`. Movie titles are entirely invented — this does not represent any
real streaming platform, user, or film. The dataset was deliberately constructed with genuine
latent genre-preference structure (each simulated user has a primary and often a secondary
favourite genre) so that collaborative filtering produces realistic, explainable results —
this is a teaching design choice, not a claim about how real-world rating data is distributed.
