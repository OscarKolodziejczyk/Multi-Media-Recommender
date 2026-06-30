import pandas as pd
from unittest.mock import patch, MagicMock
import numpy as np

from src.Embedding.encode_embeddings import generate_vectors

@patch('src.Embedding.encode_embeddings.SentenceTransformer')
def test_generate_vectors_logic(mock_SentenceTransformer):
    # Fake dataframe to pass into generate_vectors
    fake_df = pd.DataFrame({
        "Title": ["The Matrix"],
        "Description": ["Simulation action movie."],
        "DataType": ["Movie"]
    })

    # Need to create a fake embedding for the return value of mock_model.encode
    fake_embeddings = np.array([[0.1] * 384])

    # Creating the mock HuggingFace model & its return values
    mock_model = MagicMock()
    mock_SentenceTransformer.return_value = mock_model
    mock_model.encode.return_value = fake_embeddings

    # EXECUTE with our fake dataframe
    result_df = generate_vectors(fake_df)

    # Resulting DF assertions
    assert result_df is not None
    assert 'embedding' in result_df.columns
    assert result_df['Title'].iloc[0] == "The Matrix"
    assert result_df['Description'].iloc[0] == "Simulation action movie."
    assert result_df['DataType'].iloc[0] == "Movie"
    assert result_df['embedding'].iloc[0] == fake_embeddings.tolist()[0]

    # Check that our model was called once to encode our fake description
    mock_model.encode.assert_called_once_with(["Simulation action movie."])
