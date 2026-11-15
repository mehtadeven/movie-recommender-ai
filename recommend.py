"""
Content-Based Movie Recommender
--------------------------------
Recommends movies similar to one you like, using TF-IDF over each
movie's genres + keywords and cosine similarity between movies.

Dataset: data/movies.csv - 48 well-known Indian and international
films with hand-written genre/keyword tags, included in this repo.

Run:  python recommend.py
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_model(csv_path: str = "data/movies.csv"):
    df = pd.read_csv(csv_path)
    df["tags"] = df["genres"] + " " + df["keywords"]
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(df["tags"])
    similarity = cosine_similarity(matrix)
    return df, similarity


def recommend(title: str, df: pd.DataFrame, similarity, top_n: int = 5) -> list[str]:
    matches = df[df["title"].str.lower() == title.lower()]
    if matches.empty:
        raise ValueError(f"'{title}' is not in the dataset. Try one of: {', '.join(df['title'][:8])} ...")
    idx = matches.index[0]
    scores = sorted(enumerate(similarity[idx]), key=lambda p: p[1], reverse=True)
    return [df.iloc[i]["title"] for i, _ in scores[1 : top_n + 1]]


def main() -> None:
    df, similarity = build_model()
    for title in ["3 Idiots", "Interstellar", "Drishyam"]:
        print(f"\nBecause you liked '{title}':")
        for i, rec in enumerate(recommend(title, df, similarity), 1):
            print(f"  {i}. {rec}")


if __name__ == "__main__":
    main()
