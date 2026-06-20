import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def extract_text_for_embeddings(table_name):
    """
    Connects to PostgreSQL and extracts rows to generate embeddings
    :param table_name:
    :return: Dataframe (of the table), Database Engine
    """
    load_dotenv()

    # Load our env variables
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # Create Database Engine
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)

    query = f"SELECT * FROM {table_name};"

    try:
        df = pd.read_sql(query, engine)
        print(f"Now Extracting {len(df)} rows from {table_name}")
        return df, engine
    except Exception as e:
        print(f"Error extracting rows from {table_name}: {e}")
        return None, None

if __name__ == "__main__":
    # Quick execution test
    movies_df, db_engine = extract_text_for_embeddings("movies")
    if movies_df is not None:
        print(movies_df.head())
