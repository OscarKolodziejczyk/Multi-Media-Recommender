import unittest
import pandas as pd
import pytest

from ETL.transform_data import clean_data

def test_missing_files():
    fake_dfs = {
        "raw_movies.csv": pd.DataFrame({
            "Series_Title": ["Star Wars Episode IV: A New Hope"],
            "Overview": ["An epic space opera following Luke Skywalker's"
                            " journey across the galaxy"]
        }),
    }

    cleaned_dict = clean_data(fake_dfs)

    assert "movies" in cleaned_dict.keys()
    assert "books" not in cleaned_dict.keys()
    assert "games" not in cleaned_dict.keys()

def test_missing_columns():
    fake_dfs = {
        "raw_games.csv": pd.DataFrame({
            "Title": ["Star Wars Episode IV: A New Hope"],
            "Bad_Summary": ["An epic space opera following Luke Skywalker's"
                         " journey across the galaxy"]
        }),
    }

    with pytest.raises(KeyError):
        clean_data(fake_dfs)



if __name__ == '__main__':
    unittest.main()
