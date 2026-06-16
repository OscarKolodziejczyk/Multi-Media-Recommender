import os
import unittest
from ETL.load_data import load_data_to_postgres
import pandas as pd
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

def test_db_env_vars():

    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    assert DB_USER is not None
    assert DB_PASSWORD is not None
    assert DB_HOST is not None
    assert DB_PORT is not None
    assert DB_NAME is not None

    assert DB_USER != ""
    assert DB_PASSWORD != ""
    assert DB_HOST != ""
    assert DB_PORT != ""
    assert DB_NAME != ""

@patch("ETL.load_data.create_engine")
@patch("pandas.DataFrame.to_sql")
def test_load_data_to_postgres(mock_df_to_sql, mock_create_engine):
    fake_cleaned_dfs = {
        "movies": pd.DataFrame({
            "Title": ["The Matrix"],
            "Description": ["Simulation action movie."],
            "DataType": ["Movie"]
        })
    }

    # Fake database engine
    fake_engine = MagicMock()
    mock_create_engine.return_value = fake_engine

    # EXECUTE
    load_data_to_postgres(fake_cleaned_dfs)

    # Assert our engine was created
    mock_create_engine.assert_called_once()

    # Assert our pandas writing to database
    mock_df_to_sql.assert_called_once_with(
        name="movies",
        con=fake_engine,
        if_exists="replace",
        index=False
    )

if __name__ == '__main__':
    unittest.main()
