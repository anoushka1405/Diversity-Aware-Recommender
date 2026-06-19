## Intra-List Diversity (ILD) vs λ — Seed: "WE WANT TO TALK ABOUT OUR MARRIAGE"

| λ | ILD |
|---|---|
| 0 | 1.007099986076355 |
| 0.25 | 0.9864000082015991 |
| 0.5 | 0.7861999869346619 |
| 0.75 | 0.6873000264167786 |
| 1.0 | 0.6151999831199646 |

**Observation:** ILD decreases monotonically as λ increases from 0 to 1, confirming the theoretical relevance-diversity trade-off: as relevance is weighted more heavily, recommended items become more similar to each other.

**Note:** ILD at λ=0 slightly exceeds 1.0 (1.007), which is possible because cosine similarity on embeddings can be negative (unlike TF-IDF, which is bounded 0-1). At λ=0, MMR actively seeks maximally dissimilar pairs, occasionally surfacing negative-similarity pairs — confirming the algorithm behaves correctly at the diversity extreme.
