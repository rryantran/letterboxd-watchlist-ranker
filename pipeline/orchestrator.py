import asyncio

from pipeline.parser import parse_zip
from pipeline.enricher import enrich_films
from pipeline.embedder import embed_films


def run_pipeline():
    parsed_films = parse_zip(
        'letterboxd-advantagelucy-2026-05-10-01-31-utc.zip')

    enriched_films = asyncio.run(enrich_films(parsed_films))

    embedded_films = embed_films(enriched_films)

    return embedded_films
