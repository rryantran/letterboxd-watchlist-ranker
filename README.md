# letterboxd-watchlist-ranker

Rank films on your Letterboxd watchlist by how closely they match your taste, using your ratings history and metadata from [The Movie Database (TMDB)](https://www.themoviedb.org/).

## How it works

1. **Parse** — Reads your Letterboxd data export (`ratings.csv` and `watchlist.csv`).
2. **Enrich** — Looks up each film on TMDB for genres, cast, crew, keywords, and other metadata.
3. **Embed** — Converts each film into a vector using [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) sentence embeddings built from that metadata.
4. **Cluster** — Groups your highly-rated films (3+ stars) into taste clusters via weighted K-means; higher ratings carry more weight.
5. **Rank** — Scores each watchlist film by its mean cosine similarity to its top 3 taste clusters and returns the highest-scoring titles.

## Prerequisites

- Python 3.10+
- A [TMDB API key](https://www.themoviedb.org/settings/api) (free)
- A Letterboxd account data export

## Setup

1. Clone the repository and create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your TMDB API key:

```
TMDB_API_KEY=your_api_key_here
```

3. Export your Letterboxd data:
   - Go to [letterboxd.com/settings/data](https://letterboxd.com/settings/data/)
   - Request and download your data export
   - Place the zip file in the project root. It should match the pattern `letterboxd-<username>-*.zip`

## Usage

```bash
python main.py -u <letterboxd_username> [-n <top_n>]
```

| Flag               | Description                                        |
| ------------------ | -------------------------------------------------- |
| `-u`, `--username` | Your Letterboxd username (required)                |
| `-n`, `--top-n`    | Number of top-ranked films to output (default: 10) |

Example:

```bash
python main.py -u ryan -n 15
```

Sample output:

```
Inception (2010)
Directed by: Christopher Nolan
Genres: Action, Science Fiction, Adventure
Similarity Score: 87.42%
```

## Project structure

```
├── main.py                 # CLI entry point
├── configs.py              # Settings (TMDB API key from .env)
├── pipeline/
│   ├── orchestrator.py     # Runs the full pipeline
│   ├── parser.py           # Parses Letterboxd export zip
│   ├── enricher.py         # Fetches TMDB metadata (async)
│   ├── embedder.py         # Builds text blobs and embeddings
│   ├── clusterer.py        # Taste clustering from rated films
│   └── ranker.py           # Scores and ranks watchlist films
└── schemas/
    └── models.py           # Pydantic data models
```

## Notes

- Films that cannot be matched on TMDB are skipped during enrichment.
- Watchlist entries with a future release year are excluded.
- The extracted export is written to a `dataset/` directory (gitignored).
- Letterboxd export zip files are gitignored.
