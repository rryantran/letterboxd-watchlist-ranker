from pydantic import BaseModel


class Film(BaseModel):
    title: str
    decade: int
    rating: float | None
    on_watchlist: bool
