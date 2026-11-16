"""Basic tests for the movie recommender.

Run from the project root:  python -m pytest
"""

import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from recommend import build_model, recommend  # noqa: E402

CSV_PATH = PROJECT_ROOT / "data" / "movies.csv"


@pytest.fixture(scope="module")
def model():
    return build_model(CSV_PATH)


def test_dataset_loads_48_movies(model):
    df, _ = model
    assert len(df) == 48


def test_recommendations_for_3_idiots_include_chhichhore(model):
    df, similarity = model
    picks = recommend("3 Idiots", df, similarity)
    assert "Chhichhore" in picks


def test_unknown_title_raises_clear_error(model):
    df, similarity = model
    with pytest.raises(ValueError, match="not in the dataset"):
        recommend("No Such Movie", df, similarity)


def test_top_3_returns_exactly_3(model):
    df, similarity = model
    picks = recommend("3 Idiots", df, similarity, top_n=3)
    assert len(picks) == 3


def test_genre_filter_only_returns_matching_movies(model):
    df, similarity = model
    picks = recommend("3 Idiots", df, similarity, genre="Comedy")
    assert picks  # filter should still find comedy picks
    for title in picks:
        genres = df.loc[df["title"] == title, "genres"].iloc[0]
        assert "comedy" in genres.lower()


def test_cli_top_and_genre_flags():
    result = subprocess.run(
        [sys.executable, "recommend.py", "3 Idiots", "--top", "3", "--genre", "Comedy"],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0
    listed = [line for line in result.stdout.splitlines() if line.strip()[:2].rstrip(".").isdigit()]
    assert len(listed) == 3
    assert "Chhichhore" in result.stdout


def test_cli_unknown_title_is_graceful():
    result = subprocess.run(
        [sys.executable, "recommend.py", "No Such Movie"],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "not in the dataset" in result.stdout
    assert "Traceback" not in result.stderr
