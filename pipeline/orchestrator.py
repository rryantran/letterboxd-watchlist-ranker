import asyncio

from pipeline.parser import parse_zip
from pipeline.enricher import enrich_films
from pipeline.embedder import embed_films
from pipeline.clusterer import build_taste_clusters
from pipeline.ranker import rank_watchlist


def run_pipeline(letterboxd_username: str):
    parsed_films = parse_zip(letterboxd_username)

    enriched_films = asyncio.run(enrich_films(parsed_films))

    embedded_films = embed_films(enriched_films)
    taste_clusters = build_taste_clusters(embedded_films)
    ranked = rank_watchlist(embedded_films, taste_clusters, 5)

    print()
    for film in ranked:
        print(film.title, f"({film.year})")
        print(f"Directed by: {', '.join(film.directors)}")
        print(f"Genres: {', '.join(film.genres)}")
        print(f"Similarity Score: {film.score * 100}%")
        print()
