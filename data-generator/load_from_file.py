import csv
import os
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv

load_dotenv()

ES_HOST = os.getenv("ES_HOST", "localhost")  # Default to localhost if not set
ES_PORT = int(os.getenv("ES_PORT", 9200))
CSV_FILE = os.getenv("CSV_FILE", "imdb_top_1000.csv")  # Default filename if not set
INDEX_NAME = os.getenv("INDEX_NAME", "movies")  # Elasticsearch index name

es = Elasticsearch(
    [
        {'host': ES_HOST, 'port': ES_PORT, 'scheme': 'http'}
    ]
)


def load_from_csv_to_elasticsearch(csv_file, index_name):
    with open(csv_file, 'r', encoding='utf-8') as file:  # Handle potential UnicodeDecodeErrors
        reader = csv.DictReader(file)  # Assuming the first row contains headers
        try:
            helpers.bulk(es, generate_actions(reader, index_name))
            print(f"Data from {csv_file} loaded into Elasticsearch index '{index_name}' successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")


def generate_actions(reader, index_name):
    for row in reader:
        if 'imdbID' in row:
            doc = {
                "_index": index_name,
                "_id": row['imdbID'],  # Use 'imdbID' as unique ID
                "_source": row
            }
        else:
            doc = {
                "_index": index_name,
                "_source": row
            }
        yield doc


if __name__ == "__main__":
    load_from_csv_to_elasticsearch(CSV_FILE, INDEX_NAME)
