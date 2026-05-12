import zipfile
import pandas as pd
from datetime import datetime

from schemas.models import Film


def parse_zip(zip_path):
    """Parse a Letterboxd data export zip file and return a list of Film objects"""

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall("dataset")

        parsed_films = _parse_ratings() + _parse_watchlist()

    return parsed_films


def _parse_ratings() -> list[Film]:
    """Parse a Letterboxd ratings CSV file and return a list of Film objects"""

    df = pd.read_csv("dataset/ratings.csv")
    df = df.dropna()

    films = [Film(title=row["Name"], year=row["Year"], decade=_convert_to_decade(row["Year"]), rating=row["Rating"],
                  on_watchlist=False) for index, row in df.iterrows()]

    return films


def _parse_watchlist() -> list[Film]:
    """Parse a Letterboxd watchlist CSV file and return a list of Film objects"""

    df = pd.read_csv("dataset/watchlist.csv")
    df = df.dropna()
    df = df[df["Year"] <= datetime.now().year]

    films = [Film(title=row["Name"], year=row["Year"], decade=_convert_to_decade(row["Year"]), rating=None,
                  on_watchlist=True) for index, row in df.iterrows()]

    return films


def _convert_to_decade(year: int) -> int:
    """Convert a year to its decade"""

    return year // 10 * 10
