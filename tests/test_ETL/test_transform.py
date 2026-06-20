import unittest
import pandas as pd
import pytest

from src.ETL.transform_data import clean_data

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

def test_duplicates_dropped():
    fake_dfs = {
        "raw_games.csv": pd.DataFrame({
            "Title": ["Doom", "Doom", "Minecraft", "Minecraft"],
            "Summary": ["Classic FPS", "The Sequel to the Classic FPS", "Cube Building Game", "Cube Building Game"]
        })
    }
    cleaned_dict = clean_data(fake_dfs)

    assert len(cleaned_dict["games"]) == 3
    assert cleaned_dict['games'].iloc[0]['Title'] == "Doom"
    assert cleaned_dict['games'].iloc[1]['Title'] == "Doom"
    assert cleaned_dict['games'].iloc[2]['Title'] == "Minecraft"


if __name__ == '__main__':
    unittest.main()
