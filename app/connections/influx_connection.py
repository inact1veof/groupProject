import datetime
import json

from influxdb import InfluxDBClient
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import FluxStructureEncoder
import time

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
        while(True):
            try:
                self.connection = influxdb_client.InfluxDBClient(url="http://influxdb:8086",
                                               token=influx_config["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"],
                                               org=influx_config["DOCKER_INFLUXDB_INIT_ORG"])

                self.write_api = self.connection.write_api(write_options=SYNCHRONOUS)
                self.query_api = self.connection.query_api()

                logger.info("--------- Соединение c Influx установлено: %s ----------", self.connection)
                return
            except Exception as _ex:
                logger.info("--------- Соединение c Influx не установлено: %s ---------", _ex)
                time.sleep(1)

    async def read_data_from_influx(self, measurement: str, date_from: str, date_to: str):

        query = """
                    from(bucket: "EcoBucket")
                    |> range(start: _dateFrom, stop: _dateTo)
                    |> filter(fn: (r) => r["_time"] >= _dateFrom and r["_time"] <= _dateTo)  
                    |> filter(fn: (r) => r["_measurement"] == _myM)
                    |> filter(fn: (r) => r["_field"] == "value")
                    |> keep(columns: ["_time","_value", "_measurement"])
                """

        param = {
                "_myM": str(measurement),
                "_dateFrom": datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S"),
                "_dateTo": datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
        }

        try:
            response = self.query_api.query(query=query, params=param)
            output = response.to_json(indent=5)
            return output
        except Exception as _ex:
            return json.dumps({
                "code": int(40),
                "message": str(_ex)
                }, ensure_ascii=False)

    async def write_data_to_influx(self, measurement: str, value: float):
        point = influxdb_client.Point(measurement).field("value", value)
        try:
            self.write_api.write(bucket=influx_config["DOCKER_INFLUXDB_INIT_BUCKET"],
                                org=influx_config["DOCKER_INFLUXDB_INIT_ORG"],
                                record=point)
            return json.dumps({
                    "code": int(200),
                    "message": str("success")
                    }, ensure_ascii=False)
        except Exception as _ex:
            return json.dump({
                    "code": int(41),
                    "message": str(_ex)
                    }, ensure_ascii=False)
