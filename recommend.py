"""
Content-Based Movie Recommender
--------------------------------
Recommends movies similar to one you like, using TF-IDF over each
movie's genres + keywords and cosine similarity between movies.

Dataset: data/movies.csv - 48 well-known Indian and international
films with hand-written genre/keyword tags, included in this repo.

Run:  python recommend.py                      (demo picks)
      python recommend.py "3 Idiots"           (one film)
      python recommend.py "3 Idiots" --top 3   (fewer results)
      python recommend.py "3 Idiots" --genre Comedy  (one genre only)
"""

import argparse
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Default dataset sits next to this script, so the CLI works from anywhere.
DEFAULT_CSV = Path(__file__).parent / "data" / "movies.csv"


def build_model(csv_path=DEFAULT_CSV):
    df = pd.read_csv(csv_path)
    df["tags"] = df["genres"] + " " + df["keywords"]
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(df["tags"])
    similarity = cosine_similarity(matrix)
    return df, similarity


def recommend(title: str, df: pd.DataFrame, similarity, top_n: int = 5,
              genre: str | None = None) -> list[str]:
    matches = df[df["title"].str.lower() == title.lower()]
    if matches.empty:
        raise ValueError(f"'{title}' is not in the dataset. Try one of: {', '.join(df['title'][:8])} ...")
    idx = matches.index[0]
    # Most similar first; position 0 is the movie itself, so skip it.
    scores = sorted(enumerate(similarity[idx]), key=lambda p: p[1], reverse=True)
    picks = []
    for i, _ in scores[1:]:
        movie = df.iloc[i]
        # With a genre filter, keep only movies whose genres contain it.
        if genre and genre.lower() not in movie["genres"].lower():
            continue
        picks.append(movie["title"])
        if len(picks) == top_n:
            break
    return picks


def show(title: str, df: pd.DataFrame, similarity, top_n: int, genre: str | None) -> None:
    picks = recommend(title, df, similarity, top_n, genre)
    print(f"\nBecause you liked '{title}':")
    for i, rec in enumerate(picks, 1):
        print(f"  {i}. {rec}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommend movies similar to one you like.")
    parser.add_argument("title", nargs="?", help="movie title, e.g. \"3 Idiots\" (omit for demo picks)")
    parser.add_argument("--top", type=int, default=5, help="how many recommendations (default: 5)")
    parser.add_argument("--genre", help="only recommend movies of this genre, e.g. Comedy")
    args = parser.parse_args()

    df, similarity = build_model()
    if args.title:
        try:
            show(args.title, df, similarity, args.top, args.genre)
        except ValueError as error:
            print(error)
    else:
        for title in ["3 Idiots", "Interstellar", "Drishyam"]:
            show(title, df, similarity, args.top, args.genre)


if __name__ == "__main__":
    main()
