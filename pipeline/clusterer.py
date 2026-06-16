import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

from schemas.models import EmbeddedFilm


def build_taste_clusters(embedded_films: list[EmbeddedFilm]) -> np.ndarray:
    """Cluster normalized embeddings of films rated 3+ stars into taste centroids"""

    ratings = [
        film for film in embedded_films if film.rating is not None and film.rating >= 3.0]

    if not ratings:
        return np.empty((0, 384), dtype=np.float64)

    embeddings = normalize(
        np.asarray([film.embedding for film in ratings], dtype=np.float64),
        norm="l2",
    )
    weights = np.asarray([_rating_weight(film.rating)
                         for film in ratings], dtype=np.float64)

    k = _pick_k(len(ratings))

    kmeans = KMeans(n_clusters=k, n_init="auto", random_state=67)
    kmeans.fit(embeddings, sample_weight=weights)

    return kmeans.cluster_centers_


def _pick_k(n: int, min_films_per_cluster: int = 18) -> int:
    """Choose k (ranged 1-8) based on number of films and minimum films per cluster"""

    return min(max(1, n // min_films_per_cluster), 8)


# def _rating_weight(rating: float, min_rating: float = 3.0, max_rating: float = 5.0) -> float:
#     """Map rating (3-5) to weight"""

#     return (rating - min_rating) / (max_rating - min_rating)


def _rating_weight(rating: float, min_rating: float = 3.0, max_rating: float = 5.0, floor: float = 0.1) -> float:
    """Map rating (3-5) to weight (alternative version)"""

    normalized = (rating - min_rating) / (max_rating - min_rating)

    return floor + (1 - floor) * normalized
