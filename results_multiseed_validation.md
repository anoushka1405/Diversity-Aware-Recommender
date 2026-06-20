# Multi-Seed Validation: Does the λ Trade-off Hold Across Random Seeds?

## Motivation

Earlier evaluation (`results_ild_vs_lambda.md`, `results_topic_coverage.md`) was
based primarily on two hand-picked seed videos. This raises a fair question:
does the observed relevance-diversity trade-off generalize, or was it specific
to those particular examples?

This experiment runs the full λ sweep (λ = 0, 0.25, 0.5, 0.75, 1.0) across 20
randomly sampled seed videos (`random.seed(42)` for reproducibility) and reports
both the mean and standard deviation of ILD and Topic Coverage at each λ.

## Results

| λ | ILD (mean) | ILD (std) | Topic Coverage (mean) | Topic Coverage (std) |
|---|---|---|---|---|
| 0.00 | 1.011 | 0.000 | 6.00 | 0.000 |
| 0.25 | 0.999 | 0.014 | 5.30 | 1.031 |
| 0.50 | 0.750 | 0.088 | 5.15 | 0.933 |
| 0.75 | 0.417 | 0.255 | 2.75 | 1.888 |
| 1.00 | 0.343 | 0.214 | 2.20 | 1.322 |

## Interpretation

**The core finding generalizes — and is even cleaner on average.** Mean ILD
decreases monotonically as λ increases (1.011 → 0.343), confirming the original
single-seed result was not a fluke. Mean Topic Coverage also now shows a clear
downward trend (6.00 → 2.20) across 20 seeds, in contrast to the non-monotonic
pattern observed for any single seed in earlier evaluation — averaging across
many seeds smooths out seed-specific variation that looked like noise when
examined one seed at a time.

**The standard deviation reveals a structural pattern of its own.** Variation
across seeds is **lowest at λ=0 (std = 0.000 for both metrics) and highest at
λ=0.75–1.0**. This is explainable directly from the MMR formula: at λ=0, the
relevance term is multiplied by zero and drops out entirely — the algorithm's
behavior no longer depends on which seed video was used at all, since it's
purely maximizing dissimilarity to already-selected items regardless of starting
point. This is why every seed produces nearly identical ILD/coverage at λ=0.
At high λ, by contrast, the seed's specific position in embedding space
dominates the result — a seed sitting in a dense neighborhood of similar videos
behaves very differently from one sitting in a sparse, isolated region — so
results vary substantially seed to seed.

**Takeaway:** λ doesn't only control the average relevance-diversity trade-off —
it also controls how much any single result depends on which seed video was
used. Low λ produces consistent, seed-independent behavior; high λ produces
seed-dependent, less predictable results. This is a meaningful operational
property: a product relying on high-λ recommendations should expect more
variable behavior across different users/seed content than one relying on
low-λ recommendations.