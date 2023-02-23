from influxdb import InfluxDBClient

from logger import get_logger
from settings import influx_config

from connections.base import BaseConnection

logger = get_logger(__name__)

class InfluxConnection(BaseConnection):
    """
    Класс для работы с Influx.
    """

    def conncet(self) -> None:
        """
        Соединение с Influx

        :return: None
        """
        try:
            self.connection = InfluxDBClient(
                host='localhost',
                port=8086,
                username=influx_config["DOCKER_INFLUXDB_INIT_USERNAME"],
                password=influx_config["DOCKER_INFLUXDB_INIT_PASSWORD"]
            )
            logger.info("--------- Соединение c Influx установлено: %s ----------", self.connection)
        except Exception as _ex:
            logger.info("--------- Соединение c Influx не установлено: %s ---------", _ex)