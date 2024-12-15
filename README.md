# Example Docker Compose project for Telegraf, InfluxDB and Grafana

This example project demonstrates the TIG (Telegraf, InfluxDB, and Grafana) stack and includes a sample Flask application (`movie-service`) with load testing and data generation capabilities.

## Start the stack with docker compose

```bash
$ docker-compose up
```

## Services and Ports

### Grafana
- URL: http://localhost:3000 
- User: admin 
- Password: admin 

### Telegraf
- Port: 8125 UDP (StatsD input)

### InfluxDB
- Port: 8086 (HTTP API)
- User: admin 
- Password: admin 
- Database: influx

Run the influx client:

```bash
$ docker-compose exec influxdb influx -execute 'SHOW DATABASES'
```

Run the influx interactive console:

```bash
$ docker-compose exec influxdb influx

Connected to http://localhost:8086 version 1.8.0
InfluxDB shell version: 1.8.0
>
```

[Import data from a file with -import](https://docs.influxdata.com/influxdb/v1.8/tools/shell/#import-data-from-a-file-with-import)

```bash
$ docker-compose exec -w /imports influxdb influx -import -path=data.txt -precision=s
```

### Nginx
- Port: 80 (Reverse proxy for movie-service and Grafana)
- Routes:
    - `/grafana/`: Access Grafana UI.
    - `/`: Access `movie-service` API.

### movie-service (Flask application)
- Internal Port: 9000 (Nginx handles external access)
- API Endpoints:
    - `/recommendations/{user_id}`: Get movie recommendations.
    - `/watched/{user_id}`: Get watched movies.
    - `/users/{user_id}`: Get user details.
    - `/users/username/{userName}`: Get user details using username.

## Load Testing
The `load_test.sh` script simulates user traffic to the `/recommendations` and
`/watched` API endpoints. It uses `ab` (Apache Benchmark) to generate load with
configurable parameters:
- **Configuration:** Modify `load_test.sh` to adjust the `num_requests`,
  `concurrency`, `base_url`, and `user_ids` variables to customize your load
  tests.
- **Nginx:** Nginx acts as a reverse proxy, routing traffic to the
  `movie-service` container.

## Data Generator
* Describe your data generation process if applicable. If you have a script or
process to populate Elasticsearch/MongoDB, explain it here. 
* The `data_generator.py` script populates the Elasticsearch database with sample
movie data. It retrieves movie information from a CSV file and indexes it into
Elasticsearch. Run the script as follows:

# Screenshots

Here are some screenshots of the grafana dashboard:

<!-- Screenshots -->
$(ls screenshots/*.png | while read image; do echo "![$(basename "$image" .png)]($image)"; done)
<!-- End Screenshots -->

## License

The MIT License (MIT). Please see [License File](LICENSE) for more information.

