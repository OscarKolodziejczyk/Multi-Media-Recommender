import os
import pandas as pd
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

from Embedding.extract_embeddings import extract_text_for_embeddings


def test_postgres_env_vars():
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

@patch('Embedding.extract_embeddings.pd.read_sql')
@patch('Embedding.extract_embeddings.create_engine')
def test_database_read(mock_create_engine, mock_pd_read_sql):

    # Create a fake database engine
    fake_engine = MagicMock()
    mock_create_engine.return_value = fake_engine

    # This is the expected query within extract_text_for_embeddings, we are
    # recreating it here for a later assertion
    query = "SELECT * FROM movies;"

    # Fake DF for the mock_pd_read_sql call
    fake_df = pd.DataFrame({
            "Title": ["The Matrix"],
            "Description": ["Simulation action movie."],
            "DataType": ["Movie"]
        })
    mock_pd_read_sql.return_value = fake_df

    # EXECUTE with mock data
    result_df, result_engine = extract_text_for_embeddings("movies")

    # Assert our mock pd.read_sql was called with the correct arguments
    mock_pd_read_sql.assert_called_with(query, fake_engine)

    # Asserting the resultant DF and engine are the same as our mocks
    assert result_df.equals(fake_df), "Result DataFrame does not match mock"
    assert result_engine is fake_engine, "Result Engine does not match mock"
