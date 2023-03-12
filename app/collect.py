"""
Запуск приложения.
"""
import json
import time

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import psycopg2
import requests

from settings import postgres_config, influx_config, cron_config


def postgres_connection() -> str:
    postgres_count = 0
    while True:
        try:
            print("--------- Соединение c Postgres ... ----------")
            with psycopg2.connect(
                    host=postgres_config["DB_HOST"],
                    port=postgres_config["DB_PORT"],
                    user=cron_config["CRON_POSTGRES_USER"],
                    password=cron_config["CRON_POSTGRES_VALUE"],
                    database=postgres_config["POSTGRES_DB"]
            ) as connection:
                connection.autocommit = True
                print(f"--------- Соединение c Postgres установлено: {connection}----------")

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT array_to_json(array_agg(row_to_json (r))) FROM ( SELECT * FROM city) r;"
                        )
                        return json.dumps(cursor.fetchall()[0][0], ensure_ascii=False)
                except Exception as _ex:
                    print(f"--------- Postgres: {_ex} ---------")

        except Exception as _ex:
            if postgres_count == 5:
                print(f"--------- Соединение c Postgres не установлено: {_ex} ---------")
                return ""
            postgres_count += 1
            time.sleep(5)


def influx_connection(cities_str: str) -> None:
    influx_count = 0
    while True:
        try:
            print("--------- Соединение c Influx ... ----------")
            with influxdb_client.InfluxDBClient(url="http://influxdb:8086",
                                                token=influx_config["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"],
                                                org=influx_config["DOCKER_INFLUXDB_INIT_ORG"]) as connection:
                write_api = connection.write_api(write_options=SYNCHRONOUS)
                bucket = influx_config["DOCKER_INFLUXDB_INIT_BUCKET"]
                print(f"--------- Соединение c Influx установлено: {connection} ----------")

                cities = json.loads(cities_str)
                for city in cities:

                    result = requests.get(
                        f"https://api.open-meteo.com/v1/forecast?"
                        f"latitude={city['latitude']}"
                        f"&longitude={city['longitude']}"
                        f"&current_weather=True"
                        f"&windspeed_unit=ms"
                        f"&timezone=GMT")
                    result_json = result.json()

                    point = influxdb_client.Point(city['name']) \
                        .field("temperature", result_json["current_weather"]["temperature"]) \
                        .field("windspeed", result_json["current_weather"]["windspeed"]) \
                        .field("winddirection", result_json["current_weather"]["winddirection"]) \
                        .field("weathercode", result_json["current_weather"]["weathercode"])

                    try:
                        write_api.write(bucket=bucket,
                                             org=influx_config["DOCKER_INFLUXDB_INIT_ORG"],
                                             record=point)
                        print(f"--------- Запись в Influx: {city['name']} ---------")
                    except Exception as _ex:
                        print(f"--------- Influx: {_ex} ---------")

                break
        except Exception as _ex:
            if influx_count == 5:
                print(f"--------- Соединение c Influx не установлено: {_ex} ---------")
                break
            influx_count += 1
            time.sleep(5)


if __name__ == "__main__":
    print("Запуск обновления данных ...")

    cities = postgres_connection()
    print("--------- Соединение c Postgres закрыто ----------")

    if cities != "":
        influx_connection(cities)
        print("--------- Соединение c Influx закрыто ----------")

    print("Обновление завершено.")

