from src.Embedding.extract_embeddings import extract_text_for_embeddings
from src.Embedding.encode_embeddings import generate_vectors
from src.Embedding.load_embeddings import update_postgres_with_embeddings


def execute_embeddings_pipeline(table_names: list[str]):
    """
    Executes the full pipeline to encode media descriptions as vector embeddings
    :param table_names: list of table names
    """
    print("Starting Embedding Pipeline")

    for table_name in table_names:
        df, engine = extract_text_for_embeddings(table_name)

        if df is None or engine is None:
            print(f"Could not extract {table_name}; skipping table.")
            continue

        updated_df = generate_vectors(df)

        update_postgres_with_embeddings(updated_df, engine, table_name)

    print("Embedding Pipeline Completed")

if __name__ == "__main__":
    tables = ["Movies", "Books", "Games"]

    execute_embeddings_pipeline(tables)
