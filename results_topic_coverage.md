# Topic Coverage Score — Results and Discrepancy with ILD

| λ | Topic Coverage |
|---|---|
| 0 | 5 |
| 0.25 | 6 |
| 0.5 | 4 |
| 0.75 | 5 |
| 1.0 | 5 |

**Observation:** Unlike Intra-List Diversity, which decreased monotonically and 
cleanly as λ increased (1.007 → 0.615), Topic Coverage Score shows no clear trend 
across the same λ values — it fluctuates narrowly between 4 and 6 regardless of 
how much weight is placed on diversity.

**Additional finding (top_n=20 test):** Increasing list size from 10 to 20 did not 
resolve the discrepancy — Topic Coverage Score remained non-monotonic (7 → 10 → 8 → 7 → 7), 
even peaking at λ=0.25 rather than λ=0. This suggests the disagreement is not merely a 
small-sample artifact, but reflects a structural mismatch between what MMR optimizes 
for and what Topic Coverage measures.

**Resolution:** a follow-up experiment (see `results_cluster_aware.md`) tested whether 
explicitly forcing topic-cluster spread closes this gap. It does — cluster-aware 
selection achieved Topic Coverage of 10/10 versus MMR's 4/10 on the same seed, at a 
small cost to ILD.
