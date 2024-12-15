#!/bin/bash

# Set the base URL
base_url="http://127.0.0.1:80"  # nginx is listening on port 80 and is a reverse proxy for movie-service

# Set the number of requests for each test
num_requests=100000

# Set the concurrency level for each test
concurrency=1000

user_ids=("675ea176ba2cc3a351f4fccb" "675ea176ba2cc3a351f4fcd6" "675ea176ba2cc3a351f4fd19")

for user_id in "${user_ids[@]}"; do
    # Test 1: Recommendations
    echo "Testing /recommendations/$user_id"
    ab -n $num_requests -c $concurrency "$base_url/recommendations/$user_id"

    # Test 2: Watched
    echo "Testing /watched/$user_id"
    ab -n $num_requests -c $concurrency "$base_url/watched/$user_id"
done

echo "Tests complete."

