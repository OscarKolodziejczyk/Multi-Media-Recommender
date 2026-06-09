from extract_data import extract_data_from_azure
from transform_data import clean_data
from load_data import load_data_to_postgres

def execute_etl_pipeline():
    # Extract
    dfs = extract_data_from_azure()

    # Transform
    clean_dfs = clean_data(dfs)

    # Load
    load_data_to_postgres(clean_dfs)
