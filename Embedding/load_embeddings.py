from sqlalchemy import text
from sqlalchemy.engine import row


def update_postgres_with_embeddings(df, engine, table_name):
    """
    Update existing postgreSQL table with new embeddings column & value
    :param df: dataframe of table data
    :param engine: database engine
    :param table_name: name of table to update
    """
    # Safety check for missing df or embedding column
    if df is None or df.empty or "Embedding" not in df.columns:
        print("No vector embeddings found to load")
        return

    print(f"Updating Embeddings for {table_name}...")

    # Context Manager: ensures update to db is clean and won't corrupt
    with engine.begin() as conn:

        # Adds an 'Embedding' column to the table if it doesn't exist
        alter_query = text(f"""
            ALTER TABLE {table_name}
            ADD COLUMN IF NOT EXISTS Embedding vector(384);
            """)
        conn.execute(alter_query)

        # Prepare update statement, casting embedding input to a vector
        update_query = text(f"""
            UPDATE {table_name}
            SET Embedding = CAST(:Embedding AS vector)
            WHERE "Title" = :title;
            """)

        # Format data into a list of dicts & make python list into a string
        # This allows SQLAlchemy & PostgreSQL to use them correctly
        update_data = [
            {
                "Embedding": str(row["Embedding"]),
                "title": row["Title"]
            }
            for index, row in df.iterrows()
        ]

        conn.execute(update_query, update_data)

        print(f"Successfully updated {len(df)} Embeddings for {table_name}")
