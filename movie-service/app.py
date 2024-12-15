import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from elasticsearch import Elasticsearch
from flask import Flask, jsonify, request

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = MongoClient(MONGO_URI)
db = client["test_db"]
users_collection = db["users"]
movies_collection = db["movies"]

# Elasticsearch Configuration
ES_HOST = os.getenv("ES_HOST", "elasticsearch")
ES_PORT = int(os.getenv("ES_PORT", 9200))
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT, 'scheme': 'http'}])


def get_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return user


def search_movies(genres, actors, directors, limit=50):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "Director.keyword": directors
                        }
                    }
                ]
                # ,
                # "should": [
                #     {
                #         "match": {
                #             "Genre": genres
                #         }
                #     }
                # ]
            }
        }
    }
    print(query)
    results = es.search(index="movies", size=limit, **query)
    movies = []
    for hit in results['hits']['hits']:
        movies.append(hit["_source"])
    return movies


@app.route('/users/<user_id>', methods=['GET'])
def get_user_route(user_id):
    user = get_user(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/users/username/<username>', methods=['GET'])  # create new endpoint
def get_user_by_username_route(username):  # new route
    user = users_collection.find_one({"username": username})  # queries user by username
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    genres = user.get('genres', [])
    actors = user.get('actors', [])
    directors = user.get('directors', [])

    recommendations = search_movies(genres, actors, directors)

    return jsonify(recommendations), 200


@app.route('/watched/<user_id>', methods=['GET'])
def get_watched_list(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    watched_list = user.get('liked', [])  # Access the 'liked' field, default to empty list if not present
    return jsonify(watched_list), 200  # Return the watched list


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, host='0.0.0.0', port=9000)
