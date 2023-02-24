import json
import psycopg2

from logger import get_logger
from settings import postgres_config

from connections.base import BaseConnection

logger = get_logger(__name__)

class PostgresConnection(BaseConnection):
    """
    Класс для работы с Postgres.
    """

    def conncet(self) -> None:
        """
        Соединение с Postgres

        :return: None
        """
        try:
            self.connection = psycopg2.connect(
                host=postgres_config["DB_HOST"],
                port=postgres_config["DB_PORT"],
                user=postgres_config["POSTGRES_USER"],
                password=postgres_config["POSTGRES_PASSWORD"],
                database=postgres_config["POSTGRES_DB"]
            )
            self.connection.autocommit = True
            logger.info("--------- Соединение c Postgres установлено: %s ----------", self.connection)
        except Exception as _ex:
            logger.info("--------- Соединение c Postgres не установлено: %s ---------", _ex)

    async def get_cities(self) -> dict:
        """
        Возвращает все города из таблицы
        :return: dict
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM ( SELECT * FROM city) r;"
                )
                result = cursor.fetchall()
                return result[0][0]
        except Exception as _ex:
            return {
                "code": 0,
                "message": _ex
            }

    async def post_city(self, data: dict) -> dict:
        """
        Добавляет город в таблице
        :return: dict
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO City (name, longitude, latitude) VALUES (%s, %s, %s) RETURNING id",
                    (data["name"], data["longitude"], data["latitude"])
                )
                result = cursor.fetchone()[0]
                return {
                        "id": int(result),
                        "name": str(data["name"]),
                        "longitude": float(data["longitude"]),
                        "latitude": float(data["latitude"])
                        }
        except Exception as _ex:
            return {
                    "code": 0,
                    "message": _ex
                    }

    async def get_city_by_id(self, id: int) -> dict:
        """

        :param id:
        :return: dict
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM (SELECT * FROM City WHERE id = %s) r;", (id,)
                )
                return cur.fetchone()[0][0]
        except Exception as _ex:
            return {
                    "code": str(0),
                    "message": str(_ex)
                    }

    async def delete_city_by_id(self, id: int) -> dict:
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "DELETE FROM City WHERE id = %s", (id,)
                )
                if cur.rowcount == 1:
                    return {
                        "code": str(200),
                        "message": str("Successful deletion of the city")
                    }
                else:
                    return {
                        "code": str(0),
                        "message": str("Index doesn't exit in the city")
                    }
        except Exception as _ex:
            return {
                    "code": str(0),
                    "message": str(_ex)
                    }

    async def post_city(self, n, long, lat) -> dict:
        """
        Добавляет город в таблице
        :return: dict
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "INSERT INTO City (name, longitude, latitude) VALUES (%s, %s, %s) RETURNING id",
                    (n, long, lat)
                )
                result = cur.fetchone()[0]
                return {
                        "id": int(result),
                        "name": str(n),
                        "longitude": float(long),
                        "latitude": float(lat)
                        }
        except Exception as _ex:
            return {
                    "code": str(0),
                    "message": str(_ex)
                    }

    async def get_items(self) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM quote;"
            )
            msg = cursor.fetchall()
            return msg