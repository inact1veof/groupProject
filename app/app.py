import json

from flask import Flask, jsonify, request, Response

from connections.influx_connection import InfluxConnection
from connections.postgres_connection import PostgresConnection
from logger import get_logger

postgres_connection = PostgresConnection()
influx_connection = InfluxConnection()

app = Flask(__name__)
logger = get_logger(__name__)


# %% cities
@app.route('/cities', methods=['POST', 'GET'])
async def cities() -> str:
    """
    Обрабатывает POST и GET запросы /cities
    :return: str
    """
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
    if request.method == 'GET':
        return await postgres_connection.get_city_by_id(id)
    elif request.method == "DELETE":
        return await postgres_connection.delete_city_by_id(id)


@app.route('/cities-test')
async def post_by_id() -> str:
    """
    Обрабатывает GET запрос /cities-test
    :return: str
    """
    data = request.args
    name = data.get('name', type=str)
    longitude = data.get('longitude', type=float)
    latitude = data.get('latitude', type=float)

    result = await postgres_connection.post_city(name, longitude, latitude)
    return json.dumps(result, ensure_ascii=False)


@app.route('/cities-delete-test/<id>')
async def delete_by_id(id: int) -> str:
    """
    Обрабатывает DELETE запрос /cities-delete-test/{id}
    :return: str
    """
    return await postgres_connection.delete_city_by_id(id)


# %% companies
@app.route('/companies', methods=['POST', 'GET'])
async def companies() -> str:
    """
    Обрабатывает POST и GET запросы /companies
    :return: str
    """
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
    return await postgres_connection.get_companies_by_city_id(city_id)


# %% gas_analyzers
@app.route('/gas_analyzers', methods=['POST', 'GET'])
async def gas_analyzers() -> str:
    """
    Обрабатывает POST и GET запросы /gas_analyzers
    :return: str
    """
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
    return await postgres_connection.get_gas_analyzers_by_city_id(city_id)


# %% pipes
@app.route('/pipes', methods=['POST', 'GET'])
async def gas_analyzers() -> str:
    """
    Обрабатывает POST и GET запросы /pipes
    :return: str
    """
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
    return await postgres_connection.get_pipes_by_company_id(company_id)


# %%
@app.route('/')
def hello_world():  # put application's code here
    return 'Helloddd!'


@app.route('/items')
async def items():
    data = await postgres_connection.get_items()
    return jsonify(data)


if __name__ == '__main__':
    logger.info("--------- Старт сервера ---------")
    influx_connection.conncet()
    postgres_connection.conncet()
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)
