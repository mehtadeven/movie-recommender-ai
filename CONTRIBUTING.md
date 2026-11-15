# Contributing

Thanks for your interest in this project. Small, clear contributions are
very welcome.

## Setup

```bash
git clone https://github.com/mehtadeven/movie-recommender-ai.git
cd movie-recommender-ai
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run it

```bash
python recommend.py                          # demo picks
python recommend.py "3 Idiots"               # recommendations for one film
python recommend.py "3 Idiots" --top 3       # only 3 results
python recommend.py "3 Idiots" --genre Comedy
```

## Run the tests

```bash
pip install pytest
python -m pytest
```

Please make sure the tests pass before opening a pull request.

## Suggesting changes

- **Found a bug or have an idea?** Open an issue first and describe what
  you expected and what actually happened.
- **Want to fix something?** Fork the repo, make your change on a new
  branch, and open a pull request with a short explanation of the change.

## Adding movies

New films are welcome. Add one row per film to `data/movies.csv`, keeping
the exact same columns and format:

```
title,year,genres,keywords
```

- `genres`: space-separated, e.g. `Comedy Drama`
- `keywords`: a few space-separated words describing the story and themes
- No commas inside a field (the file is comma-separated).

Good tags matter more than a big catalogue: the recommendations are only
as good as the genres and keywords.

## Code style

Keep it simple: short functions, clear names, and a brief comment where
the code is not obvious. If a beginner cannot follow it, it is too
complicated for this project.
