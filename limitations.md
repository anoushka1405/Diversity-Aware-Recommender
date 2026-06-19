# Evaluation Scope and Limitations

## Why Precision@K, Recall@K, MAP, and Novelty Score are not computed

These relevance metrics require **ground-truth relevance labels**,  an independent
signal of which videos are "actually" relevant to a given query, separate from the
similarity scores the recommender itself produces. This dataset contains no such
signal: there is no real user interaction data, no click-through history, and no
human labeled relevance judgments.

Computing Precision@K or Recall@K here would require treating the system's own
cosine-similarity output as ground truth, which is circular. It would not measure
whether the recommender is *correct*, only whether it agrees with itself. A high
"Precision@K" computed this way would be guaranteed by construction, not earned,
and would misrepresent the rigor of the evaluation.

Novelty Score has the same root problem: it requires knowledge of a user's typical
viewing cluster (real interaction history), which isn't available in this dataset.

**Decision:** rather than compute a metric that would look complete but measure
nothing meaningful, these are explicitly scoped out. This mirrors a limitation — the absence of real user interaction data.

## What was evaluated instead

Two diversity-side metrics were implemented and validated, since these can be
computed directly and meaningfully from content alone:

- **Intra-List Diversity (ILD)** — average pairwise dissimilarity within a
  recommendation list. Showed a clean, monotonic relationship with λ across
  multiple seed videos and list sizes.
- **Topic Coverage Score** — count of distinct topic clusters represented in a
  recommendation list. Did *not* show a monotonic relationship with λ, even at
  larger list sizes attributable to the structural property of MMR's greedy selection process.

The disagreement between these two diversity metrics is itself a meaningful result:
it shows that "diversity" is not a single well-defined quantity, and that metric
choice materially affects what conclusions can be drawn from the same recommender.