import zipfile
import pandas as pd
from datetime import datetime
from pathlib import Path

from schemas.models import Film


def parse_zip(letterboxd_username: str) -> list[Film]:
    """Parse a Letterboxd data export zip file and return a list of Film objects"""

    zip_path = _find_letterboxd_export_zip(letterboxd_username)

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


def _find_letterboxd_export_zip(letterboxd_username: str) -> Path:
    """Find Letterboxd export zip for a user"""

    root = Path.cwd()
    pattern = f"letterboxd-{letterboxd_username}-*.zip"
    matches = list(root.glob(pattern))

    if not matches:
        raise FileNotFoundError(
            f"No Letterboxd export zip found for {letterboxd_username}"
        )

    return matches[0]


def _convert_to_decade(year: int) -> int:
    """Convert a year to its decade"""

    return year // 10 * 10
