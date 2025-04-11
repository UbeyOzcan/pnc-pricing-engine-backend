import pandas as pd
from pathlib import Path


class DataFactory:
    def __init__(self):
        pass

    def get_project_root(self) -> Path:
        return Path(__file__).parent.parent.parent

    def getData(self):
        return pd.read_csv(f'{self.get_project_root()}/models/data/frenchmtpl_clean.csv', sep=';', engine='python')