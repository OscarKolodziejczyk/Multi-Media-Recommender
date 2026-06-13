from extract_data import extract_data_from_azure
from transform_data import clean_data
from load_data import load_data_to_postgres

def execute_etl_pipeline():
    """
    1. Extracts raw data from azure and turns it into a dictionary of DataFrames
    2. Transforms the raw data into a clean version with only necessary data
    3. Loads the cleaned data into PostgreSQL
    """
    # 1. Extract
    dfs = extract_data_from_azure()

    # 2. Transform
    clean_dfs = clean_data(dfs)

    # 3. Load
    load_data_to_postgres(clean_dfs)
