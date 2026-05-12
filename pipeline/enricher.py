import httpx
from aiolimiter import AsyncLimiter
from datetime import date
from tqdm.asyncio import tqdm

from configs import Settings
from schemas.models import Film, EnrichedFilm

settings = Settings()
tmdb_api_key = settings.tmdb_api_key
tmdb_api_url = "https://api.themoviedb.org/3"

limiter = AsyncLimiter(max_rate=38, time_period=1)


async def enrich_films(films: list[Film]) -> list[EnrichedFilm]:
    """Enrich a list of films with TMDB data"""

    async with httpx.AsyncClient(base_url=tmdb_api_url, params={"api_key": tmdb_api_key}, http2=True) as client:
        enriched_films_raw = await tqdm.gather(*[_enrich_film(client, film) for film in films], desc="Enriching films")

        enriched_films = [
            film for film in enriched_films_raw if film is not None]

    return enriched_films


async def _enrich_film(client: httpx.AsyncClient, film: Film) -> EnrichedFilm | None:
    """Enrich a film with TMDB data"""

    tmdb_id = await _get_tmdb_id(client, film.title, film.year)

    if not tmdb_id:
        return None

    film_info = await _get_tmdb_film_info(client, tmdb_id)

    # Details
    genres = [genre["name"] for genre in film_info.get("genres", [])]
    runtime_mins = film_info.get("runtime")
    runtime = _runtime_category(runtime_mins) if runtime_mins else ""
    studio = next((company["name"] for company in film_info.get(
        "production_companies", [])), "")

    # Credits
    credits = film_info.get("credits", {})
    crew = credits.get("crew", [])
    top_cast = [cast["name"] for cast in credits.get("cast", [])[:3]]
    directors = _crew_by_job(crew, "Director")
    writers = _crew_by_job(crew, "Writer") + _crew_by_job(crew, "Screenplay")
    cinematographers = _crew_by_job(crew, "Director of Photography")

    # Extract full country name using origin country code
    origin_country_code = next(
        (country for country in film_info.get("origin_country", [])), "")
    production_countries = film_info.get("production_countries", [])
    country = next(
        (country["name"] for country in production_countries if country["iso_3166_1"] == origin_country_code), "")

    # Extract full language name in English using original language code
    original_language = film_info.get("original_language", "")
    spoken_languages = film_info.get("spoken_languages", [])
    language = next((language["english_name"]
                    for language in spoken_languages if language["iso_639_1"] == original_language), "")

    # Keywords
    keywords_raw = film_info.get("keywords", {}).get("keywords", [])
    keywords = [keyword["name"] for keyword in keywords_raw]

    return EnrichedFilm(
        title=film.title,
        year=film.year,
        decade=film.decade,
        genres=genres,
        runtime=runtime,
        country=country,
        language=language,
        studio=studio,
        top_cast=top_cast,
        directors=directors,
        writers=writers,
        cinematographers=cinematographers,
        keywords=keywords,
        rating=film.rating,
        on_watchlist=film.on_watchlist,
    )


async def _get_tmdb_id(client: httpx.AsyncClient, title: str, year: int) -> int | None:
    """Get TMDB ID for a film using search"""

    async with limiter:
        response = await client.get("/search/movie", params={"query": title})

    response.raise_for_status()
    results = response.json().get("results", [])

    if not results:
        return None

    # Prevent duplicates by checking release year (issue with identical titles, +/- 1 year tolerance for festival releases)
    for result in results:
        titles = [
            _normalize_title(result.get("title", "")),
            _normalize_title(result.get("original_title", ""))
        ]

        # Check if title matches at least one listed title
        if _normalize_title(title) not in titles:
            continue

        release_date_str = result.get("release_date", "")

        if not release_date_str:
            continue

        year_diff = abs(int(release_date_str.split("-")[0]) - year)

        if year_diff <= 2:
            release_date = date.fromisoformat(release_date_str)

            # Filter out future releases
            if release_date > date.today():
                return None

            return result.get("id")

    print(f"No TMDB ID found for: {title} ({year})")
    print(f"TMDB titles: {titles}")

    return None


async def _get_tmdb_film_info(client: httpx.AsyncClient, tmdb_id: int) -> dict:
    """Get TMDB details, credits, and keywords for a film"""

    async with limiter:
        response = await client.get(f"/movie/{tmdb_id}", params={"append_to_response": "credits,keywords"})

    response.raise_for_status()
    film_info = response.json()

    return film_info


def _runtime_category(runtime: int) -> str:
    """Get runtime category for a film"""

    if runtime < 90:
        return "Short"
    elif runtime < 120:
        return "Standard"
    elif runtime < 150:
        return "Long"
    else:
        return "Epic"


def _crew_by_job(crew: list[dict], job: str) -> list[str]:
    """Get crew by job title"""

    return [c["name"] for c in crew if c["job"] == job]


def _normalize_title(title: str) -> str:
    """Normalize title (lowercase, standardize dashes)"""

    dash_chars = (
        "\u2010",
        "\u2011",
        "\u2012",
        "\u2013",
        "\u2014",
        "\u2212",
    )

    for char in dash_chars:
        title = title.replace(char, "-")

    return title.lower().strip()
