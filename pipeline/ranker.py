import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from schemas.models import EmbeddedFilm, RankedFilm


def rank_watchlist(embedded_films: list[EmbeddedFilm], taste_clusters: np.ndarray, top_n: int = 10) -> list[RankedFilm]:
    """Score watchlist films against taste clusters and return the top N ranked"""

    watchlist = [film for film in embedded_films if film.on_watchlist]

    if not watchlist or taste_clusters.shape[0] == 0:
        return []

    embeddings = np.asarray(
        [film.embedding for film in watchlist], dtype=np.float64)

    similarity = cosine_similarity(embeddings, taste_clusters)

    best_cluster = np.argmax(similarity, axis=1)  # (n watchlist,)
    best_score = np.max(similarity, axis=1)  # (n watchlist,)

    # Rank films by score (array of film indices, descending)
    ranked = np.argsort(best_score)[::-1][:top_n]

    return [
        RankedFilm(
            title=watchlist[i].title,
            year=watchlist[i].year,
            genres=watchlist[i].genres,
            directors=watchlist[i].directors,
            score=float(best_score[i]),
            cluster_index=int(best_cluster[i]),
        )
        for i in ranked
    ]
