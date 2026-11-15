![Movie Recommender AI](assets/banner.svg)

# Movie Recommender AI

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) ![Recommender](https://img.shields.io/badge/Type-Recommendation%20System-ff69b4) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)

A **content-based recommendation engine**: give it a film you like and it returns the five most similar titles from its catalogue — the same core mechanism behind the recommendation rows of major streaming platforms, implemented transparently in a few dozen lines.

## Sample output

```
Because you liked '3 Idiots':        Because you liked 'Interstellar':
  1. Chhichhore                        1. Avengers: Endgame
  2. Munna Bhai MBBS                   2. Mad Max: Fury Road
  3. The Shawshank Redemption          3. Inception
  4. RRR                               4. The Matrix
  5. Hera Pheri                        5. Shaitaan

Because you liked 'Drishyam':
  1. A Wednesday
  2. Gangs of Wasseypur
  3. Shaitaan
  4. Parasite
  5. Andhadhun
```

## How it works

![Pipeline](assets/flow.svg)

Each of the 48 films in `data/movies.csv` (Indian and international) carries hand-written genre and keyword tags. TF-IDF vectorises the tags; **cosine similarity** then measures the angle between any two films' vectors. The five smallest angles to your pick are the recommendations — no user data, no ratings matrix, purely content.

## Quick start

```bash
pip install -r requirements.txt
python recommend.py
```

Call `recommend("Inception", df, similarity)` with any title in the dataset for your own list.

## What this project demonstrates

- How production recommenders work at the concept level
- TF-IDF and cosine similarity as general text-comparison tools
- Why metadata quality drives recommendation quality

## Roadmap

- Scale the catalogue to 500+ films
- Add collaborative filtering (users who liked X also liked Y)
- Simple web UI

---

**Author:** [Mehta Deven](https://github.com/mehtadeven) — IT student at SAL College of Engineering, Ahmedabad, building a public portfolio in Python, Machine Learning and AI.
**Portfolio:** [mehtadeven.github.io/portfolio](https://mehtadeven.github.io/portfolio/)

