def clean_data(dfs):

    # New dictionary that will hold our transformed data
    cleaned_dfs = {}

    # Transform all 3 CSVs to include only Title, Description, and DataType
    # columns, with no missing values.

    # Books:
    if "raw_books.csv" in dfs.keys():
        df_books = dfs['raw_books.csv'][['title', 'description']].dropna().copy()
        df_books.insert(2, 'DataType', "Book")
        df_books.rename(columns={'title': 'Title', 'description': 'Description'}, inplace=True)
        cleaned_dfs['books'] = df_books
    else:
        print("Error, raw_books.csv does not exist")

    # Movies:
    if "raw_movies.csv" in dfs.keys():
        df_movies = dfs['raw_movies.csv'][['Series_Title', 'Overview']].dropna()
        df_movies.insert(2, 'DataType', "Movie")
        df_movies.rename(columns={'Series_Title': 'Title', 'Overview': 'Description'}, inplace=True)
        cleaned_dfs['movies'] = df_movies
    else:
        print("Error, raw_movies.csv does not exist")

    # Video Games:
    if "raw_games.csv" in dfs.keys():
        df_games = dfs['raw_games.csv'][['Title', 'Summary']].dropna()
        df_games.insert(2, 'DataType', "Game")
        df_games.rename(columns={'Summary': 'Description'}, inplace=True)
        cleaned_dfs['games'] = df_games
    else:
        print("Error, raw_games.csv does not exist")

    return cleaned_dfs
