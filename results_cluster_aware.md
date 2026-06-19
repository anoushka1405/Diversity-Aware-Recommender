# Cluster-Aware Re-ranking: Does Forcing Topic Spread Close the Coverage Gap?

## Motivation

Earlier evaluation found that Intra-List Diversity (ILD) decreased cleanly and
monotonically as λ increased, but Topic Coverage Score did not follow the same
trend (see `results_topic_coverage.md`). The working hypothesis was that MMR's
greedy, pairwise selection process optimizes for raw dissimilarity at each step,
which does not guarantee the final list spreads across many topic clusters — a
candidate can be "maximally different" from items already selected without the
overall list achieving broad cluster coverage.

This experiment tests that hypothesis directly: does explicitly forcing one
selection per topic cluster, rather than relying on MMR's greedy pairwise choice,
close the gap?

## Method

A `cluster_aware_recommend()` function was implemented: for each of the 20
KMeans topic clusters, the single candidate with highest relevance
to the seed video is selected. If `top_n` exceeds the number of clusters, remaining
slots are filled using standard MMR (λ=0.5) on the leftover candidates.

This was compared against pure MMR (λ=0.5) on the same seed video
("WE WANT TO TALK ABOUT OUR MARRIAGE"), `top_n=10`.

## Results

| Method | Intra-List Diversity (ILD) | Topic Coverage (of 10) |
|---|---|---|
| Pure MMR (λ=0.5) | 0.786 | 4 |
| Cluster-aware | 0.723 | **10** |

## Interpretation

**The hypothesis is confirmed.** Cluster-aware selection achieves perfect topic
coverage (10 out of 10 recommended items from 10 distinct clusters), more than
doubling pure MMR's coverage of 4. This directly demonstrates that MMR's greedy
pairwise optimization was indeed leaving topic coverage on the table, exactly as
predicted, explicitly forcing cluster spread closes that gap.

**A new, smaller trade-off emerges in exchange.** ILD dropped slightly
(0.786 → 0.723) under the cluster-aware method. This is explainable: cluster-aware
selection picks the single best item per cluster by relevance alone, without any
pairwise dissimilarity optimization across that selection. Because topic clusters
are not perfectly separated in embedding space, two items from different clusters
can still have moderately high pairwise similarity,  so cluster-aware selection
gains guaranteed category-level spread at a small cost to fine-grained pairwise
dissimilarity.

**Conclusion:** neither method dominates the other outright — they optimize for
different notions of diversity, and the right choice depends on which one matters
more for a given application. A natural extension would be
a hybrid: cluster-aware selection for coarse topic spread, with MMR re-ranking
applied *within* each cluster's candidate pool before the single best item is chosen,
potentially recovering some of the lost ILD without sacrificing coverage.