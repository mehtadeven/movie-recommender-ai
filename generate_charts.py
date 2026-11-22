"""
Generate the README result chart for the Movie Recommender.

Runs the real recommender for "3 Idiots" and saves a horizontal bar
chart of the top-5 recommendations with their similarity scores
to assets/result.png.

Run:  python generate_charts.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from recommend import build_model

NAVY = "#0B3C5D"
GOLD = "#E3A82B"
CREAM = "#F7F1E1"
OUT = Path(__file__).parent / "assets" / "result.png"
TITLE = "3 Idiots"


def top_picks_with_scores(title: str, top_n: int = 5):
    """Return [(movie_title, similarity_score)] most similar to title."""
    df, similarity = build_model()
    idx = df.index[df["title"].str.lower() == title.lower()][0]
    # Sort every other movie by similarity to the chosen one.
    ranked = sorted(enumerate(similarity[idx]), key=lambda p: p[1], reverse=True)
    picks = [(df.iloc[i]["title"], float(score)) for i, score in ranked[1:top_n + 1]]
    return picks


def main() -> None:
    picks = top_picks_with_scores(TITLE)
    for title, score in picks:
        print(f"{title}: {score:.3f}")

    # Reverse so the best match sits on top of the chart.
    names = [title for title, _ in reversed(picks)]
    scores = [score * 100 for _, score in reversed(picks)]

    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    bars = ax.barh(names, scores, color=[GOLD] + [NAVY] * 4, height=0.55)
    for bar, score in zip(bars, scores):
        ax.text(score + 0.6, bar.get_y() + bar.get_height() / 2,
                f"{score:.1f}%", va="center", fontweight="bold")
    ax.set_xlim(0, max(scores) * 1.25)
    ax.set_xlabel("Cosine similarity to '3 Idiots' (%)")
    ax.set_title("Because you liked '3 Idiots' — top 5 of 60 films",
                 fontsize=12, fontweight="bold", color=NAVY)
    plt.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    plt.savefig(OUT, dpi=150)
    print(f"Chart saved to {OUT}")


if __name__ == "__main__":
    main()
