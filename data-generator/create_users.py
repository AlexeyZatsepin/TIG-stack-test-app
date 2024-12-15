import os
import csv
import random
import re
from pymongo import MongoClient
from bson.objectid import ObjectId

genre_list = ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller"]
actors_list = ["Tom Hanks", "Leonardo DiCaprio", "Meryl Streep", "Brad Pitt", "Scarlett Johansson"]
title_list = ["Tom Hanks", "Leonardo DiCaprio", "Meryl Streep", "Brad Pitt", "Scarlett Johansson"]
director_list = ["Tom Hanks", "Leonardo DiCaprio", "Meryl Streep", "Brad Pitt", "Scarlett Johansson"]

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")


def get_random_elements(my_list, min_elements=2, max_elements=5):
    """Selects 2 or 4 random elements from a list.

    Args:
        my_list: The list to select elements from.
        min_elements: The minimum number of elements to select.
        max_elements: The maximum number of elements to select.

    Returns:
        A list containing the randomly selected elements.
        Returns an empty list if the input list is empty or if max_elements is greater than the input list's length.
    """

    num_elements = random.randint(min_elements, min(max_elements, len(my_list))) if my_list else 0
    return random.sample(my_list, num_elements)


def get_unique_values_from_csv(filepath, columns):
    try:
        unique_values = {col: set() for col in columns}
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)  # Use DictReader for easier column access
            for row in reader:
                for col in columns:
                    value = row.get(col)  # handles missing values gracefully
                    if value:  # skips empty or missing cells
                        unique_values[col].add(value)
        return unique_values
    # transforms set of unique values to a list
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except Exception as e:  # Catches any other potential errors
        print(f"An error occurred: {e}")
        return None


def create_users(unique_data, num_users=1000):
    """Creates n users with random genre and actor preferences."""
    try:
        client = MongoClient(MONGO_URI)
        db = client["test_db"]
        users_collection = db["users"]
        for i in range(num_users):
            user_data = {
                "username": f"user_{i + 1}",  # Create unique usernames
                "genres": get_random_elements(list(unique_data["Genre"])),
                "actors": get_random_elements(list(unique_data["Actor"]), 3, 10),
                "directors": get_random_elements(list(unique_data["Director"])),
                "liked": get_random_elements(list(unique_data["Series_Title"]), 5, 50)
            }
            users_collection.insert_one(user_data)
        client.close()  # Close connection to db
        print(f"{num_users} users created successfully.")
    except Exception as e:
        print(f"An error occurred creating users: {e}")

def merge_actors(unique_data):
    all_actors = set()
    for i in range(1, 5):
        all_actors.update(unique_data[f"Star{i}"])
    unique_data["Actor"] = all_actors

def merge_genres(unique_data):
    all_genres = set()
    for genre_string in unique_data["Genre"]:
        genres = re.split(r',\s*', genre_string)
        for genre in genres:
            all_genres.add(genre)
    unique_data["Genre"] = all_genres


if __name__ == "__main__":
    filepath = os.path.join("imdb_top_1000.csv")  # gets file path, modify it accordingly
    columns_to_extract = ["Genre", "Director", "Series_Title", "Star1", "Star2", "Star3", "Star4"]
    unique_data = get_unique_values_from_csv(filepath, columns_to_extract)
    merge_actors(unique_data)
    merge_genres(unique_data)

    for col, values in unique_data.items():
        print(f"Unique {col}s ({len(values)}):")

    create_users(unique_data, 1000)
