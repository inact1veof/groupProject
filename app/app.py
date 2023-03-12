import datetime
import json

from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin


from connections.influx_connection import InfluxConnection
from connections.postgres_connection import PostgresConnection
from logger import get_logger

postgres_connection = PostgresConnection()
influx_connection = InfluxConnection()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
logger = get_logger(__name__)


# %% cities
@app.route('/cities', methods=['POST', 'GET'])
async def cities() -> str:
    """
    Обрабатывает POST и GET запросы /cities
    :return: str
    """
    check_postgres_connection()
    if request.method == 'GET':
        return await postgres_connection.get_cities()
    elif request.method == 'POST':
        data = request.get_json()
        return await postgres_connection.post_city(data)


@app.route('/cities/<id>', methods=['DELETE', 'GET'])
async def cities_by_id(id: int) -> str:
    """
    Обрабатывает DELETE и GET запросы /cities/<id>
    :return: str
    """
    check_postgres_connection()

    if request.method == 'GET':
        return await postgres_connection.get_city_by_id(id)
    elif request.method == "DELETE":
        return await postgres_connection.delete_city_by_id(id)


# %% companies
@app.route('/companies', methods=['POST', 'GET'])
async def companies() -> str:
    """
    Обрабатывает POST и GET запросы /companies
    :return: str
    """
    check_postgres_connection()

    if request.method == 'GET':
        return await postgres_connection.get_companies()
    elif request.method == 'POST':
        data = request.get_json()
        return await postgres_connection.post_company(data)


@app.route('/companies/<id>', methods=['DELETE', 'GET'])
async def companies_by_id(id: int) -> str:
    """
    Обрабатывает DELETE и GET запросы /companies/{id}
    :return: str
    """
    check_postgres_connection()

    if request.method == 'GET':
        return await postgres_connection.get_company_by_id(id)
    elif request.method == "DELETE":
        return await postgres_connection.delete_company_by_id(id)


@app.route('/companies/city/<city_id>', methods=['GET'])
async def companies_by_city_id(city_id: int):
    """
    Обрабатывает GET запрос /companies/city/{city_id}
    :return:
    """
    check_postgres_connection()

    return await postgres_connection.get_companies_by_city_id(city_id)


# %% gas_analyzers
@app.route('/gas_analyzers', methods=['POST', 'GET'])
async def gas_analyzers() -> str:
    """
    Обрабатывает POST и GET запросы /gas_analyzers
    :return: str
    """
    check_postgres_connection()

    if request.method == 'GET':
        return await postgres_connection.get_gas_analyzers()
    elif request.method == 'POST':
        data = request.get_json()
        return await postgres_connection.post_gas_analyzer(data)


@app.route('/gas_analyzers/<id>', methods=['DELETE', 'GET'])
async def gas_analyzers_by_id(id: int) -> str:
    """
    Обрабатывает DELETE и GET запросы /gas_analyzers/{id}
    :return: str
    """
    check_postgres_connection()

    if request.method == 'GET':
        return await postgres_connection.get_gas_analyzer_by_id(id)
    elif request.method == "DELETE":
        return await postgres_connection.delete_gas_analyzer_by_id(id)


@app.route('/gas_analyzers/city/<city_id>', methods=['GET'])
async def gas_analyzers_by_city_id(city_id: int):
    """
    Обрабатывает GET запрос /gas_analyzers/city/{city_id}
    :return:
    """
    check_postgres_connection()

    return await postgres_connection.get_gas_analyzers_by_city_id(city_id)


# %% pipes
@app.route('/pipes', methods=['POST', 'GET'])
async def gas_pipes() -> str:
    """
    Обрабатывает POST и GET запросы /pipes
    :return: str
    """
    check_postgres_connection()

    if request.method == 'GET':
        return await postgres_connection.get_pipes()
    elif request.method == 'POST':
        data = request.get_json()
        return await postgres_connection.post_pipe(data)


@app.route('/pipes/<id>', methods=['DELETE', 'GET'])
async def pipes_by_id(id: int) -> str:
    """
    Обрабатывает DELETE и GET запросы /pipes/<id>
    :return: str
    """
    check_postgres_connection()

    if request.method == 'GET':
        return await postgres_connection.get_pipe_by_id(id)
    elif request.method == "DELETE":
        return await postgres_connection.delete_pipe_by_id(id)


@app.route('/pipes/company/<company_id>', methods=['GET'])
async def pipes_by_company_id(company_id: int):
    """
    Обрабатывает GET запрос /pipes/company/<company_id>
    :return:
    """
    check_postgres_connection()

    return await postgres_connection.get_pipes_by_company_id(company_id)


# %% influx
@app.route('/influx/data', methods=['POST'])
async def data_from_influx():
    check_influx_connection()

    if request.method == 'POST':
        measurement = request.args.get('measurement')
        value = request.args.get('value')
        return await influx_connection.write_data_to_influx(measurement, float(value))


@app.route('/influx/gas_analyzer', methods=['GET'])
async def gas_analyzer_from_influx():
    check_influx_connection()

    if request.method == 'GET':
        measurement = request.args.get('measurement')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        if date_to is None:
            date_to = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return await influx_connection.read_gas_analyzer_data_from_influx(measurement, date_from, date_to)


@app.route('/influx/weather', methods=['GET'])
async def weather_from_influx():
    check_influx_connection()

    if request.method == 'GET':
        measurement = request.args.get('measurement')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        if date_to is None:
            date_to = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return await influx_connection.read_weather_data_from_influx(measurement, date_from, date_to)


# %% hello_world
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def check_postgres_connection():
    if postgres_connection.connection.closed != 0:
        logger.info("--------- Соединение c Postgres потеряно возобновляем соединение ----------")
        postgres_connection.connection()


def check_influx_connection():
    if not influx_connection.connection.ping():
        logger.info("--------- Соединение c Influx потеряно возобновляем соединение ----------")
        influx_connection.conncet()


def get_connections():
    influx_connection.conncet()
    postgres_connection.conncet()


if __name__ == '__main__':
    logger.info("--------- Старт сервера ---------")
    get_connections()
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)
