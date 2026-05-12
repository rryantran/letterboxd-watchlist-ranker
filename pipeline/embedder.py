from sentence_transformers import SentenceTransformer

from schemas.models import EnrichedFilm, EmbeddedFilm

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_films(films: list[EnrichedFilm]) -> list[EmbeddedFilm]:
    """Embed films using a sentence transformer model"""
    text_blobs = [_build_text_blob(film) for film in films]
    embeddings = model.encode(text_blobs)

    return [EmbeddedFilm(title=film.title, embedding=embedding, rating=film.rating, on_watchlist=film.on_watchlist) for film, embedding in zip(films, embeddings)]


def _build_text_blob(film: EnrichedFilm) -> str:
    """Build text blob from film metadata for embedding"""

    sentences = []

    genres = [g.lower() for g in film.genres]
    if genres:
        genre_phrase = _oxford_join(genres)
        if film.country:
            country_phrase = _country_with_article(film.country)
            sentences.append(f"A {genre_phrase} film from {country_phrase}.")
        else:
            sentences.append(f"A {genre_phrase} film.")
    elif film.country:
        sentences.append(f"A film from {_country_with_article(film.country)}.")

    if film.directors:
        sentences.append(
            f"Directed by {_oxford_join(film.directors)}."
        )
    if film.writers:
        sentences.append(
            f"Written by {_oxford_join(film.writers)}."
        )
    if film.top_cast:
        sentences.append(
            f"Starring {_oxford_join(film.top_cast)}."
        )
    if film.cinematographers:
        sentences.append(
            f"Cinematography by {_oxford_join(film.cinematographers)}."
        )
    if film.studio:
        sentences.append(f"Produced by {film.studio}.")
    sentences.append(f"Released in the {film.decade}s.")
    if film.runtime:
        sentences.append(f"Runtime is {film.runtime.lower()}.")
    if film.language:
        sentences.append(f"Originally in {film.language}.")
    if film.keywords:
        lowered = [k.lower() for k in film.keywords]
        sentences.append(
            f"The film is characterized by {_oxford_join(lowered)}.")

    return " ".join(sentences)


def _oxford_join(items: list[str]) -> str:
    """Join items with Oxford comma"""

    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"

    return ", ".join(items[:-1]) + f", and {items[-1]}"


def _country_with_article(country: str) -> str:
    """Add article to country name if needed"""

    if country.startswith("United "):
        return f"the {country}"

    return country
