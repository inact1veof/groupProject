import json
import psycopg2
import time

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
        while(True):
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
                return
            except Exception as _ex:
                logger.info("--------- Соединение c Postgres не установлено: %s ---------", _ex)
                time.sleep(1)

# %% cities
    async def get_cities(self) -> str:
        """
        Возвращает все города из таблицы
        :return: dict
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM ( SELECT * FROM city) r;"
                )
                return json.dumps(cursor.fetchall()[0][0], ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(0, _ex), ensure_ascii=False)

    async def post_city(self, data: dict) -> str:
        """
        Добавляет город в таблицу
        :return: dict
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO City (name, longitude, latitude) VALUES (%s, %s, %s) RETURNING id",
                    (data["name"], data["longitude"], data["latitude"])
                )
                result = cursor.fetchone()[0]
                return json.dumps({
                        "id": int(result),
                        "name": str(data["name"]),
                        "longitude": float(data["longitude"]),
                        "latitude": float(data["latitude"])
                        }, ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(0, _ex), ensure_ascii=False)

    async def get_city_by_id(self, id: int) -> str:
        """
        Достает из базы данных город по заданному id
        :param id:
        :return: dict
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM "
                    "(SELECT * FROM City WHERE id = %s) r;", (id,)
                )
                return json.dumps(cur.fetchone()[0][0], ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(0, _ex), ensure_ascii=False)

    async def delete_city_by_id(self, id: int) -> str:
        """
        Удаляет из базы данных город по заданному id
        :param id:
        :return: dict
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "DELETE FROM City WHERE id = %s", (id,)
                )
                if cur.rowcount == 1:
                    return json.dumps(self.assemble_message(200, "Successful deletion of the City"),
                                      ensure_ascii=False)
                else:
                    return json.dumps(self.assemble_message(1, "Table City has no items with given id"),
                                      ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(0, _ex), ensure_ascii=False)


# %% companies
    async def get_companies(self) -> str:
        """
        Возвращает все компании из таблицы
        :return: str
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM ( SELECT * FROM Company) r;"
                )
                return json.dumps(cursor.fetchall()[0][0], ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(10, _ex), ensure_ascii=False)

    async def post_company(self, data: dict) -> str:
        """
        Добавляет компанию в таблицу
        :return: str
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Company (city_id, name, description, longitude, latitude, sanitary_zone_radius) "
                    "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (data["city_id"], data["name"], data["description"],
                     data["longitude"], data["latitude"], data["sanitary_zone_radius"])
                )
                result = cursor.fetchone()[0]
                return json.dumps({
                    "id": int(result),
                    "city_id": int(data["city_id"]),
                    "name": str(data["name"]),
                    "description": str(data["description"]),
                    "longitude": float(data["longitude"]),
                    "latitude": float(data["latitude"]),
                    "sanitary_zone_radius": float(data["sanitary_zone_radius"])
                    }, ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(10, _ex), ensure_ascii=False)

    async def get_company_by_id(self, id: int) -> str:
        """
        Достает из базы данных компанию по заданному id
        :param id:
        :return: str
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM "
                    "(SELECT * FROM Company WHERE id = %s) r;", (id,)
                )
                return json.dumps(cur.fetchone()[0][0], ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(10, _ex), ensure_ascii=False)

    async def delete_company_by_id(self, id: int) -> str:
        """
        Удаляет из базы данных компанию по заданному id
        :param id:
        :return: str
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "DELETE FROM Company WHERE id = %s", (id,)
                )
                if cur.rowcount == 1:
                    return json.dumps(self.assemble_message(200, "Successful deletion of the company"),
                                      ensure_ascii=False)
                else:
                    return json.dumps(self.assemble_message(11, "Table Company has no items with given id"),
                                      ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(10, _ex), ensure_ascii=False)

    async def get_companies_by_city_id(self, city_id: int) -> str:
        """
        Достает из базы данных компании по заданному city_id
        :param city_id:
        :return: str
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM "
                    "(SELECT * FROM Company WHERE city_id = %s) r;", (city_id,)
                )
                result = cur.fetchall()[0][0]
                if result is not None:
                    return json.dumps(result, ensure_ascii=False)
                else:
                    return json.dumps(self.assemble_message(11, "Table Company has no items with given city_id"),
                                      ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(10, _ex), ensure_ascii=False)

# %% gas_analyzers
    async def get_gas_analyzers(self) -> str:
        """
        Возвращает все газоанализаторы из таблицы
        :return: str
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM ( SELECT * FROM Gas_analyzer) r;"
                )
                return json.dumps(cursor.fetchall()[0][0], ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(20, _ex), ensure_ascii=False)

    async def post_gas_analyzer(self, data: dict) -> str:
        """
        Добавляет газоанализатор в таблицу
        :return: str
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Gas_analyzer (measurement, city_id, longitude, latitude)"
                    "VALUES (%s, %s, %s, %s)",
                    (data["measurement"], data["city_id"],
                     data["longitude"], data["latitude"])
                )
                result = cursor.fetchone()[0]
                return json.dumps({
                    "measurement": int(data["measurement"]),
                    "city_id": str(data["city_id"]),
                    "longitude": float(data["longitude"]),
                    "latitude": float(data["latitude"])
                    }, ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(20, _ex), ensure_ascii=False)

    async def get_gas_analyzer_by_id(self, id: int) -> str:
        """
        Достает из базы данных газоанализатор по заданному id
        :param id:
        :return: str
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM "
                    "(SELECT * FROM Gas_analyzer WHERE id = %s) r;", (id,)
                )
                return json.dumps(cur.fetchone()[0][0], ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(20, _ex), ensure_ascii=False)

    async def delete_gas_analyzer_by_id(self, id: int) -> str:
        """
        Удаляет из базы данных газоанализатор по заданному id
        :param id:
        :return:
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "DELETE FROM Gas_analyzer WHERE id = %s", (id,)
                )
                if cur.rowcount == 1:
                    return json.dumps(self.assemble_message(200, "Successful deletion of the gas analyzer"),
                                      ensure_ascii=False)
                else:
                    return json.dumps(self.assemble_message(21, "Table Gas_analyzer has no items with given Index"),
                                      ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(20, _ex), ensure_ascii=False)

    async def get_gas_analyzers_by_city_id(self, city_id: int) -> str:
        """
        Достает из базы данных газоанализаторы по заданному city_id
        :param city_id:
        :return:
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM "
                    "(SELECT * FROM Gas_analyzer WHERE city_id = %s) r;", (city_id,)
                )
                result = cur.fetchall()[0][0]
                if result is not None:
                    return json.dumps(result, ensure_ascii=False)
                else:
                    return json.dumps(self.assemble_message(21, "Table Gas_analyzer has no items with given city_id"),
                                      ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(20, _ex), ensure_ascii=False)

# %% pipes
    async def get_pipes(self) -> str:
        """
        Возвращает все трубы из таблицы
        :return: str
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM ( SELECT * FROM Pipe) r;"
                )
                return json.dumps(cursor.fetchall()[0][0], ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(30, _ex), ensure_ascii=False)

    async def post_pipe(self, data: dict) -> str:
        """
        Добавляет трубы в таблицу
        :return: str
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Pipe (measurement, company_id, longitude, latitude)"
                    "VALUES (%s, %s, %s, %s)",
                    (data["measurement"], data["company_id"],
                     data["longitude"], data["latitude"])
                )
                result = cursor.fetchone()[0]
                return json.dumps({
                    "measurement": int(data["measurement"]),
                    "company_id": str(data["company_id"]),
                    "longitude": float(data["longitude"]),
                    "latitude": float(data["latitude"])
                }, ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(30, _ex), ensure_ascii=False)

    async def get_pipe_by_id(self, id: int) -> str:
        """
        Достает из базы данных трубу по заданному id
        :param id:
        :return: str
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM "
                    "(SELECT * FROM Pipe WHERE id = %s) r;", (id,)
                )
                return json.dumps(cur.fetchone()[0][0], ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(30, _ex), ensure_ascii=False)

    async def delete_pipe_by_id(self, id: int) -> str:
        """
        Удаляет из базы данных трубу по заданному id
        :param id:
        :return: str
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "DELETE FROM Pipe WHERE id = %s", (id,)
                )
                if cur.rowcount == 1:
                    return json.dumps(self.assemble_message(200, "Successful deletion of the Pipe"),
                                      ensure_ascii=False)
                else:
                    return json.dumps(self.assemble_message(11, "Table Pipe has no items with given id"),
                                      ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(30, _ex), ensure_ascii=False)

    async def get_pipes_by_company_id(self, company_id: int) -> str:
        """
        Достает из базы данных трубу по заданному company_id
        :param company_id:
        :return: str
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    "SELECT array_to_json(array_agg(row_to_json (r))) FROM "
                    "(SELECT * FROM Pipe WHERE company_id = %s) r;", (company_id,)
                )
                result = cur.fetchall()[0][0]
                if result is not None:
                    return json.dumps(result, ensure_ascii=False)
                else:
                    return json.dumps(self.assemble_message(31, "Table Pipe has no items with given company_id"),
                                      ensure_ascii=False)
        except Exception as _ex:
            return json.dumps(self.assemble_message(30, _ex), ensure_ascii=False)

# %%
    @staticmethod
    def assemble_message(code: int, message: str) -> dict:
        return {
            "code": int(code),
            "message": str(message)
        }
