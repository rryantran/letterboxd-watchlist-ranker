import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from schemas.models import EmbeddedFilm, RankedFilm


def rank_watchlist(embedded_films: list[EmbeddedFilm], taste_clusters: np.ndarray, top_n: int = 10) -> list[RankedFilm]:
    """Score watchlist films by mean similarity to their top 3 taste clusters"""

    watchlist = [film for film in embedded_films if film.on_watchlist]

    if not watchlist or taste_clusters.shape[0] == 0:
        return []

    embeddings = np.asarray(
        [film.embedding for film in watchlist], dtype=np.float64)

    similarity = cosine_similarity(embeddings, taste_clusters)

    k = min(3, similarity.shape[1])  # 3 or less clusters
    top_k = np.sort(similarity, axis=1)[:, -k:]
    scores = top_k.mean(axis=1)

    # Rank films by score (array of film indices, descending)
    ranked = np.argsort(scores)[::-1][:top_n]

    return [
        RankedFilm(
            title=watchlist[i].title,
            year=watchlist[i].year,
            genres=watchlist[i].genres,
            directors=watchlist[i].directors,
            score=float(scores[i]),
        )
        for i in ranked
    ]
