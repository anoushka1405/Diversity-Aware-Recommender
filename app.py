"""
Diversity-Aware Recommender — Streamlit Demo

A thin UI layer over the RecommendationEngine (src/recommender.py).
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from recommender import RecommendationEngine

st.set_page_config(page_title="Diversity-Aware Recommender", layout="wide")


@st.cache_data
def load_data():
    df1 = pd.read_csv("data/cleaned_videos_part1.csv")
    df2 = pd.read_csv("data/cleaned_videos_part2.csv")
    df = pd.concat([df1, df2], ignore_index=True)
    embeddings = np.load("data/embeddings_weighted.npy")
    sim_matrix = cosine_similarity(embeddings)
    return df, sim_matrix


@st.cache_data
def get_clusters(_sim_matrix_shape, embeddings, n_clusters=20):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)
    return labels


def intra_list_diversity(indices, similarity_matrix):
    count = 0
    dissimilarity = 0
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            video_i, video_j = indices[i], indices[j]
            dissimilarity += 1 - similarity_matrix[video_i][video_j]
            count += 1
    return dissimilarity / count if count > 0 else 0


def topic_coverage(indices, df):
    clusters_seen = set()
    for index in indices:
        clusters_seen.add(df["topic_cluster"][index])
    return len(clusters_seen)


def cluster_aware_recommend(seed_idx, similarity_matrix, df, top_n, n_clusters=20):
    candidates = [i for i in range(len(df)) if i != seed_idx]
    selected = []

    for cluster_num in range(n_clusters):
        cluster_candidates = [c for c in candidates if df["topic_cluster"][c] == cluster_num]
        if cluster_candidates:
            best = max(cluster_candidates, key=lambda c: similarity_matrix[seed_idx][c])
            selected.append(best)
            candidates.remove(best)
        if len(selected) >= top_n:
            break

    while len(selected) < top_n:
        scores = {}
        for candidate in candidates:
            relevance = similarity_matrix[seed_idx, candidate]
            redundancy = max([similarity_matrix[candidate, s] for s in selected])
            scores[candidate] = 0.5 * relevance - 0.5 * redundancy
        best = max(scores, key=scores.get)
        selected.append(best)
        candidates.remove(best)

    return selected[:top_n]


# --- Load everything ---
st.title("Diversity-Aware Video Recommender")
st.caption(
    "MMR-based re-ranking to mitigate echo chambers in content recommendations. "
    "Pick a seed video, adjust λ, and compare relevance vs. diversity."
)

with st.spinner("Loading data and embeddings..."):
    df, sim_matrix = load_data()
    embeddings = np.load("data/embeddings_weighted.npy")
    if "topic_cluster" not in df.columns:
        df["topic_cluster"] = get_clusters(sim_matrix.shape, embeddings)

engine = RecommendationEngine(df, sim_matrix)

# --- Sidebar controls ---
st.sidebar.header("Controls")

search_query = st.sidebar.text_input("Search for a seed video by title keyword")

if search_query:
    matches = df[df["title"].str.contains(search_query, case=False, na=False)]
    options = matches["title"].head(20).tolist()
else:
    # a few interesting defaults
    default_titles = [
        "WE WANT TO TALK ABOUT OUR MARRIAGE",
        "CURRENT AFFAIRS | THE HINDU | 5th December 2017 | UPSC,IBPS, RRB, SSC,CDS,IB,CLAT",
        "All Sports Golf Battle 2 | Dude Perfect",
        "Wearing Fashion Nova Outfits For A Week",
        "How Nike Designs for an N.B.A. Athlete | In the Studio",
        "Missouri Star Quilt Company Live Stream"
    ]
    options = [t for t in default_titles if t in df["title"].values] or df["title"].head(20).tolist()

if not options:
    st.sidebar.warning("No matches found — try a different keyword.")
    st.stop()

selected_title = st.sidebar.selectbox("Seed video", options)
seed_idx = df[df["title"] == selected_title].index[0]

method = st.sidebar.radio("Method", ["MMR (relevance ↔ diversity slider)", "Cluster-aware (guaranteed topic spread)"])

top_n = st.sidebar.slider("Number of recommendations", 5, 20, 10)

if method.startswith("MMR"):
    lam = st.sidebar.slider("λ (relevance weight)", 0.0, 1.0, 0.5, 0.05)
else:
    lam = None

run = st.sidebar.button("Get Recommendations", type="primary")

# --- Main panel ---
st.subheader("Seed Video")
st.write(f"**{selected_title}**")

if run:
    if method.startswith("MMR"):
        result = engine.recommend(seed_idx=seed_idx, lambda_param=lam, top_n=top_n)
    else:
        result = cluster_aware_recommend(seed_idx, sim_matrix, df, top_n)

    ild = intra_list_diversity(result, sim_matrix)
    coverage = topic_coverage(result, df)

    col1, col2 = st.columns(2)
    col1.metric("Intra-List Diversity (ILD)", f"{ild:.3f}")
    col2.metric("Topic Coverage", f"{coverage} / {top_n}")

    st.subheader("Recommendations")
    for rank, idx in enumerate(result, start=1):
        title = df.iloc[idx]["title"]
        country = df.iloc[idx].get("country", "")
        st.write(f"{rank}. {title}  `{country}`")

    st.caption(
        "ILD = average pairwise dissimilarity within this list (higher = more diverse). "
        "Topic Coverage = number of distinct topic clusters represented (out of 20 total clusters)."
    )
else:
    st.info("Set your options in the sidebar and click **Get Recommendations**.")

st.divider()
st.caption(
    "This demo proves the relevance-diversity trade-off is real and controllable. "
    "It does not measure whether users would actually prefer more diverse results — "
    "see `limitations.md` for the full reasoning."
)