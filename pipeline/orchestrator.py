from pipeline.parser import parse_zip


def run_pipeline():
    parsed_films = len(parse_zip(
        'letterboxd-advantagelucy-2026-05-10-01-31-utc.zip'))
    print(parsed_films)
