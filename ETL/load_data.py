import os
from sqlalchemy import create_engine

def load_data_to_postgres(cleaned_dfs):
    print("Now connecting to PostgreSQL...")

    # Get credentials from .env
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # Construct database URL with our credentials
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Create SQL Engine
    engine = create_engine(db_url)

    # Load our individual dataframes into their own tables
    for table_name, df in cleaned_dfs.items():

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )

        print(f"Successfully loaded table {table_name} to PostgreSQL")

    print("Successfully loaded all data to PostgreSQL")


