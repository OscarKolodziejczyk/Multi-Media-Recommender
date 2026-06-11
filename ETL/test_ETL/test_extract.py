import unittest
import os
from unittest.mock import patch, MagicMock

import pytest
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd
from ETL.extract_data import extract_data_from_azure


def test_azure_env_vars():

    load_dotenv()

    AZURE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')

    assert AZURE_CONNECTION_STRING is not None
    assert CONTAINER_NAME is not None

    assert AZURE_CONNECTION_STRING != ""
    assert CONTAINER_NAME != ""

@patch('ETL.extract_data.BlobServiceClient')
def test_raw_files_in_dataframes(mock_blob_service_client):

    # Setup fake csv byte data
    fake_csv_data = b"title, description\nFake Title, Fake Description"

    # Setup fake blob client that returns our fake csv data
    mock_blob_client = MagicMock()
    mock_blob_client.download_blob.return_value.readall.return_value = fake_csv_data

    # Setup fake containers:
    mock_container_client = MagicMock()
    mock_blob_1 = MagicMock()
    mock_blob_1.name = "raw_movies.csv"

    mock_container_client.list_blobs.return_value = [mock_blob_1]
    mock_container_client.get_blob_client.return_value = mock_blob_client

    # Tie it all together:
    mock_blob_service_client.from_connection_string.return_value.get_container_client.return_value = mock_container_client

    # Execute the function, and @patch will intercept with our mock data
    dfs = extract_data_from_azure()

    assert "raw_movies.csv" in dfs.keys()
    assert isinstance(dfs["raw_movies.csv"], pd.DataFrame)
    assert dfs["raw_movies.csv"].iloc[0]['title'] == 'Fake Title'

@patch('ETL.extract_data.AZURE_CONNECTION_STRING', "DefaultEndpointsProtocol=https;AccountName=bad;AccountKey=bad;EndpointSuffix=core.windows.net")
def test_bad_credentials():
    with pytest.raises(Exception):
        extract_data_from_azure()

if __name__ == '__main__':
    unittest.main()
