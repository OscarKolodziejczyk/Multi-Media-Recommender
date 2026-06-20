import pandas as pd
from unittest.mock import MagicMock

from src.Embedding.load_embeddings import update_postgres_with_embeddings

def test_load_embeddings():

    # Create fake DataFrame & Engine to pass to update_postgres_with_embeddings
    fake_vectors = [0.1] * 384
    fake_df = pd.DataFrame({
        "Title": ["The Matrix"],
        "Description": ["Simulation action movie."],
        "DataType": ["Movie"],
        "embedding": [fake_vectors]
    })
    fake_engine = MagicMock()
    mock_conn = MagicMock()

    # when "with fake_engine.begin() as conn:" runs we give it mock_conn instead
    fake_engine.begin.return_value.__enter__.return_value = mock_conn

    # Expected update data
    expected_update_data = [
        {
            "embedding": str(fake_vectors),
            "title": "The Matrix"
        }
    ]

    # EXECUTE with fake data
    update_postgres_with_embeddings(fake_df, fake_engine, "movies")

    assert mock_conn.execute.call_count == 2, "Expected 2 queries to execute"

    actual_update_data = mock_conn.execute.call_args_list[1].args[1]

    assert actual_update_data == expected_update_data, "Database formatting error"
