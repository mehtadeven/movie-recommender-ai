# 🎬 Movie Recommender AI


![Banner](assets/banner.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![Status](https://img.shields.io/badge/status-working-brightgreen)

A **content-based recommendation system**: give it a movie you like, and it suggests similar ones — the same core idea behind Netflix and Spotify recommendations, in a small, readable project.

## 🍿 Sample output

```
Because you liked '3 Idiots':
  1. Chhichhore
  2. Munna Bhai MBBS
  3. The Shawshank Redemption
  ...

Because you liked 'Interstellar':
  1. Avengers Endgame
  2. Mad Max: Fury Road
  3. Inception
  ...

Because you liked 'Drishyam':
  1. A Wednesday
  2. Gangs of Wasseypur
  3. Parasite
  ...
```

## ⚙️ How it works

1. Each movie in `data/movies.csv` (48 Indian + international films) is tagged with genres and keywords
2. TF-IDF converts those tags into a numeric vector for every movie
3. **Cosine similarity** measures how close any two movies' vectors are
4. The 5 closest movies to your pick become the recommendations

## 🚀 Run it

```bash
pip install -r requirements.txt
python recommend.py
```

To get recommendations for any movie in the dataset, call `recommend("Inception", df, similarity)` with your own title.

## 🧠 What I learned

- How recommendation systems work under the hood (content-based filtering)
- TF-IDF and cosine similarity for comparing text
- Why good tags/metadata matter more than a fancy model

## 🔮 Next steps

- [ ] Grow the dataset to 500+ movies
- [ ] Add collaborative filtering (users who liked X also liked Y)
- [ ] Build a simple web UI for it

---
Built by [Mehta Deven](https://github.com/mehtadeven) — IT student learning ML/AI in public.
