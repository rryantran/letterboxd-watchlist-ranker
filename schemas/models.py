from pydantic import BaseModel


class Film(BaseModel):
    title: str
    year: int
    decade: int
    rating: float | None
    on_watchlist: bool


class EnrichedFilm(BaseModel):
    # Details
    title: str
    year: int
    decade: int
    genres: list[str]
    runtime: str = ""
    country: str = ""
    language: str = ""
    studio: str = ""

    # Credits
    top_cast: list[str] = []  # 3-5 actors
    directors: list[str]
    writers: list[str] = []
    cinematographers: list[str] = []

    # Keywords
    keywords: list[str] = []

    # Other
    rating: float | None = None
    on_watchlist: bool
