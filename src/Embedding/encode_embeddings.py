from sentence_transformers import SentenceTransformer
import pandas as pd

def generate_vectors(df):
    """
    Loads Hugging Face model and generates vector embeddings for the Description
     column
    :param df: DataFrame containing the table of data
    :return:
    """
    if df is None or df.empty:
        print("No DataFrame provided")
        return df

    # Initialize Hugging Face model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Extract the descriptions column and turn it into a list
    descriptions = df['Description'].tolist()

    # Pass the list of descriptions into the model to generate embeddings
    embeddings = model.encode(descriptions)

    # Attach the new vector embedding back to the DataFrame for each row
    df['Embedding'] = embeddings.tolist()

    print("Vector Embeddings Successfully Generated")
    return df

if __name__ == "__main__":
    # 1. Create a tiny "fake" dataset
    test_data = {
        'Title': ['The Matrix', 'Inception'],
        'Description': [
            'A computer hacker learns from mysterious rebels about the true nature of his reality.',
            'A thief who steals corporate secrets through the use of dream-sharing technology.'
        ],
        'DataType': ['Movie', 'Movie']
    }
    test_df = pd.DataFrame(test_data)

    # 2. Run the dataframe through our Hugging Face function
    print("Starting vector generation test...")
    result_df = generate_vectors(test_df)

    # 3. Inspect the resulting math
    if result_df is not None and 'Embedding' in result_df.columns:
        print("\n--- TEST SUCCESS ---")
        print(f"New Columns: {result_df.columns.tolist()}")

        # Isolate the first vector to prove it is a 384-dimensional array
        first_movie = result_df['Title'].iloc[0]
        first_vector = result_df['Embedding'].iloc[0]

        print(f"\nTarget: {first_movie}")
        print(f"Total Vector Dimensions: {len(first_vector)}")
        print(f"First 5 math values: {first_vector[:5]}")
