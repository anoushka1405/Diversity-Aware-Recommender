# Diversity-Aware Recommendation System

Mitigating echo chambers in online video platforms using content-based filtering and Maximal Marginal Relevance (MMR) re-ranking.

## Overview

Mainstream recommendation systems are optimized almost exclusively for engagement — watch time, click-through rate, retention. This creates a well-documented side effect: the **echo chamber**, where users are served an increasingly narrow slice of content that reinforces their existing preferences.

This project treats diversity not as a constraint on relevance, but as a **co-equal optimization objective**. It combines content-based filtering with an MMR-based re-ranking layer, producing recommendations that are simultaneously relevant and topically diverse.

## Project Status

| Phase | Status |
|---|---|
| Data cleaning & preprocessing | ✅ Done |
| TF-IDF feature extraction | ✅ Done |
| Sentence embeddings (semantic features) | ✅ Done |
| Title-weighted embeddings | ✅ Done |
| MMR re-ranking engine | 🚧 In progress |
| Diversity evaluation metrics | 🚧 In progress |
| Visualizations | ⏳ Planned |
| Streamlit / demo interface | ⏳ Planned |

This project is being built incrementally and documented honestly at each stage — including dead ends and fixes, not just final results.

## Dataset

[YouTube Trending Video Dataset](https://www.kaggle.com/datasets/datasnaek/youtube-new) (Kaggle) — combined US and India regions, ~22,400 unique videos after deduplication.

Due to file size constraints, raw and processed datasets are not included in this repo. Download from the link above and place CSVs in a `data/` folder to reproduce.

## Methodology

### 1. Data Preparation
Combined US + IN trending data, handled missing descriptions, removed duplicate video entries (videos trend across multiple days), and merged title/tags/description into a unified content field.

### 2. Feature Engineering
Two representations were built and compared:

- **TF-IDF** — lightweight, keyword-level similarity
- **Sentence embeddings** (`all-MiniLM-L6-v2`) — semantic, meaning-level similarity
- **Title-weighted embeddings** — titles weighted 3x over tags/description, since titles carry more reliable topic signal (with the caveat that titles can also be clickbait)

A real debugging finding from this stage: early TF-IDF similarity scores were dominated by **channel boilerplate** (sign-off text, affiliate links) rather than actual topical content — e.g., two completely unrelated videos from the same creator scored 95%+ similarity purely due to shared gear-list text in descriptions. This was diagnosed by inspecting raw text overlap, then addressed through text cleaning (URL removal, normalization) and validated by comparing before/after recommendation quality.

### 3. Candidate Generation
Given a seed video, candidates are retrieved via cosine similarity over the chosen feature representation, prioritizing recall before downstream re-ranking.

### 4. Diversity-Aware Re-ranking (Core Contribution)
Candidates are re-ranked using Maximal Marginal Relevance:

```
Score(i) = λ · Relevance(i, query) − (1−λ) · max Similarity(i, already_selected)
```

At λ=1, the system reduces to pure similarity ranking (baseline). At λ=0, it maximizes diversity regardless of relevance. The system is evaluated across the λ spectrum to characterize this trade-off.

### 5. Baseline Comparison
A naive similarity-only recommender serves as the baseline. All diversity improvements are measured against it.

## Evaluation Framework

| Category | Metric | What It Measures |
|---|---|---|
| Relevance | Precision@K | How many of the top K recommendations are relevant |
| Relevance | Recall@K | What fraction of relevant items are surfaced |
| Diversity | Intra-List Diversity | Average pairwise dissimilarity within a recommendation list |
| Diversity | Topic Coverage Score | Number of distinct topic clusters represented |

## What Differentiates This Project

- **Algorithmic depth** — diversity is a first-class objective, with MMR implemented and explained, not just referenced
- **Rigorous evaluation** — results are compared against a baseline, not assumed
- **Documented debugging** — real issues (boilerplate-driven similarity inflation, channel-style bias in embeddings) were found, diagnosed, and addressed, with before/after evidence kept in the notebooks
- **Intellectual honesty** — this system achieves topic-level diversity, not true viewpoint diversity. That distinction is acknowledged explicitly.

## Scope and Limitations

- Diversity is approximated at the topic level via content similarity — individual stance/viewpoint is not detected
- No real user interaction data is available; similarity-based proxies are used instead
- Non-English content has reduced TF-IDF signal due to English-only stopword/token handling; embeddings partially mitigate this
- Creator/channel writing style can influence similarity scores independently of topic, a structural limitation of text-only signals

## Future Work

- Transcript-based stance detection for true viewpoint diversity
- Comment sentiment analysis as an ideological signal
- Channel-level bias modeling
- Behavioral controversy scoring from engagement patterns

## Tech Stack

Python · pandas · NumPy · scikit-learn · sentence-transformers (`all-MiniLM-L6-v2`) · matplotlib/seaborn (planned)

## Repository Structure

```
├── data/                          # not committed — see Dataset section
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_text_embeddings.ipynb
│   ├── 03_mmr_engine.ipynb        # in progress
│   └── 04_evaluation.ipynb        # planned
└── README.md
```
