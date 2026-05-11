import zipfile
import pandas as pd


def parse_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall("dataset")
        print(zip_ref.namelist())
