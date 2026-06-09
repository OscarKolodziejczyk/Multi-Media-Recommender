import os
import io
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import pandas as pd

load_dotenv()

AZURE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')

def extract_data_from_azure():
    print('Extracting data from Azure')

    # Instantiate blob client
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    # We will return a dictionary where the keys are the filenames of the data
    # and the value is the CSV data read in by pandas
    dataframes = {}

    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print(f"Extracting data from {blob.name}")

        # Get individual blob client for the file
        blob_client = container_client.get_blob_client(blob.name)

        # Download the data strean into memory
        download_stream = blob_client.download_blob().readall()

        # Read the byte stream into Pandas
        df = pd.read_csv(io.BytesIO(download_stream))

        # Store in our dictionary
        dataframes[blob.name] = df

    return dataframes
