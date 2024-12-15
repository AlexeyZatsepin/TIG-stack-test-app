import requests
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv


load_dotenv() # load api key from .env file

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
ES_HOST = os.getenv("ES_HOST") # or 'localhost' if running locally
ES_PORT = int(os.getenv("ES_PORT", 9200))


es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])

def index_movie(movie):

    try:
        res = es.index(index='movies', id=movie['imdbID'], document=movie)
        print(f"Indexed movie: {movie['Title']}")
    except Exception as e:
        print(f"Error indexing movie {movie.get('Title', 'Unknown')} : {e}")




def fetch_and_index_movie(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        movie_data = response.json()
        index_movie(movie_data)


    else:
        print(f"Error fetching data for IMDb ID: {imdb_id}")



if __name__ == "__main__":

    imdb_ids = ["tt0111161", "tt1375666"] # Example IDs

    for imdb_id in imdb_ids:
        fetch_and_index_movie(imdb_id)