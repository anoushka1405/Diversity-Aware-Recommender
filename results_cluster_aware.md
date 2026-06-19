# Cluster-Aware Selection: Does Forcing Topic Spread Close the Coverage Gap?

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

## Method — a note on terminology

This is **not** a re-ranking method in the same sense as MMR, and is more
accurately described as **pre-partitioned selection**:

- **MMR re-ranks**: each candidate's score is computed *relative to items already
  selected* (via the redundancy penalty). Diversity emerges from this comparison,
  step by step.
- **Cluster-aware selection pre-partitions**: candidates are split into 20 topic
  clusters (via KMeans, computed once up front) *before* any selection happens.
  Within the primary phase, the single best-matching candidate is chosen from each
  cluster, by relevance alone — with **no comparison to other already-selected
  items at all**. Diversity here is structural, guaranteed by the partitioning
  itself, not earned through any ranking logic.

A fallback to standard MMR is included only for the case where `top_n` exceeds
`n_clusters` (i.e., more recommendations are needed than there are clusters to draw
from). In that case, after one pick per cluster, the remaining slots are filled
using plain MMR (λ=0.5) on whatever candidates are left — at this point, cluster
labels are no longer used at all; the fallback treats all leftover candidates as a
single undifferentiated pool, exactly as in the original implementation.

**In the experiment below (top_n=10, n_clusters=20), the fallback never
triggered** — all 10 selected videos came from the cluster-partitioning phase
alone, with zero pairwise-redundancy optimization involved. This matters for
interpreting the ILD result below.

## Results

Tested on the seed video "WE WANT TO TALK ABOUT OUR MARRIAGE", `top_n=10`.

| Method | Intra-List Diversity (ILD) | Topic Coverage (of 10) |
|---|---|---|
| Pure MMR (λ=0.5) | 0.786 | 4 |
| Cluster-aware (pre-partitioned) | 0.723 | **10** |

## Interpretation

**The hypothesis is confirmed.** Pre-partitioned selection achieves perfect topic
coverage (10 out of 10 recommended items from 10 distinct clusters), more than
doubling pure MMR's coverage of 4. This directly demonstrates that MMR's greedy
pairwise optimization was indeed leaving topic coverage on the table, exactly as
predicted — explicitly forcing cluster spread closes that gap.

**A new, smaller trade-off emerges in exchange.** ILD dropped slightly
(0.786 → 0.723). Given that no MMR fallback ran in this test, this drop is
entirely attributable to the absence of any pairwise-dissimilarity optimization:
pre-partitioned selection picks the single best item per cluster by relevance
alone, with no check on how similar that item is to others already chosen.
Because topic clusters are not perfectly separated in embedding space, two items
from neighboring clusters can still have moderately high pairwise similarity — so
this method gains guaranteed category-level spread at a small, explainable cost
to fine-grained pairwise dissimilarity.

**Which method to use is a design choice, not a strict improvement.** Neither
method dominates the other:

- Use **plain MMR** when fine-grained pairwise dissimilarity matters most — e.g.,
  ensuring no two recommended items feel similar to each other, even within a
  broad topic.
- Use **pre-partitioned (cluster-aware) selection** when guaranteed topic-level
  spread matters most — e.g., ensuring a user sees multiple distinct categories
  of content, not just several variations on one theme.

**Conclusion / Future Work:** a natural hybrid would apply MMR *within* each
cluster's candidate pool — i.e., still pick one item per cluster, but choose that
item by relevance-minus-redundancy against other already-selected items, rather
than by relevance alone. This could potentially recover some of the lost ILD
without sacrificing the guaranteed coverage demonstrated here.