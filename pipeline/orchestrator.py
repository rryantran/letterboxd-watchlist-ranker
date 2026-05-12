import asyncio

from pipeline.parser import parse_zip
from pipeline.enricher import enrich_films


def run_pipeline():
    parsed_films = parse_zip(
        'letterboxd-advantagelucy-2026-05-10-01-31-utc.zip')

    enriched_films = asyncio.run(enrich_films(parsed_films))

    print(enriched_films[:5])
