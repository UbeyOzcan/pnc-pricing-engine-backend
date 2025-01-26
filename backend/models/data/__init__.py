import polars as pl
import os

def get_mtpl_data():
    module_path = os.path.dirname(__file__)
    return pl.read_csv(source = os.path.join(module_path,"frenchmtpl_clean.csv"), separator=";", infer_schema_length=int(1e10))