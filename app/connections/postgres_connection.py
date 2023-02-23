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
            logger.info("--------- Соединение c Postgres установлено: %s ----------", self.connection)
        except Exception as _ex:
            logger.info("--------- Соединение c Postgres не установлено: %s ---------", _ex)

    async def get_items(self) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM quote;"
            )
            msg = cursor.fetchall()
            return msg