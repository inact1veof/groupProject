import json

from flask import Flask, jsonify, request

from connections.influx_connection import InfluxConnection
from connections.postgres_connection import PostgresConnection
from logger import get_logger

postgres_connection = PostgresConnection()
influx_connection = InfluxConnection()

app = Flask(__name__)
logger = get_logger(__name__)


# %% cities
@app.route('/cities', methods=['POST', 'GET'])
async def cities():
    """

    :return:
    """
    if request.method == 'GET':
        result = await postgres_connection.get_cities()
        return json.dumps(result, ensure_ascii=False)
    elif request.method == 'POST':
        data = request.get_json()
        result = await postgres_connection.post_city(data)
        return result


@app.route('/cities/<id>', methods=['DELETE', 'GET'])
async def cities_by_id(id):
    """

    :return:
    """
    if request.method == 'GET':
        result = await postgres_connection.get_city_by_id(id)
        return json.dumps(result, ensure_ascii=False)
    elif request.method == "DELETE":
        result = await postgres_connection.delete_city_by_id(id)
        return json.dumps(result, ensure_ascii=False)


@app.route('/cities-test')
async def post_by_id():
    """

    :return:
    """
    data = request.args
    name = data.get('name', type=str)
    longitude = data.get('longitude', type=float)
    latitude = data.get('latitude', type=float)

    result = await postgres_connection.post_city(name, longitude, latitude)
    return json.dumps(result, ensure_ascii=False)

@app.route('/cities-delete-test/<id>')
async def delete_by_id(id):
    result = await postgres_connection.delete_city_by_id(id)
    return json.dumps(result, ensure_ascii=False)


# %% companies
@app.route('/companies', methods=['POST', 'GET'])
def companies():
    """

    :return:
    """
    data = request.get_json()
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"


@app.route('/companies/<id>', methods=['DELETE', 'GET'])
def companies_by_id(id):
    """

    :return:
    """
    if request.method == 'GET':
        return "GET"
    else:
        return "DELETE"


@app.route('/companies/city/<city_id>', methods=['GET'])
def companies_by_city_id(city_id):
    """

    :return:
    """
    return "GET " + str(city_id)


# %% gas_analyzers
@app.route('/gas_analyzers', methods=['POST', 'GET'])
def gas_analyzers():
    """

    :return:
    """
    data = request.get_json()
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"


@app.route('/gas_analyzers/<measurement>', methods=['DELETE', 'GET'])
def gas_analyzers_by_id(measurement):
    """

    :return:
    """
    if request.method == 'GET':
        return "GET"
    else:
        return "DELETE"


@app.route('/gas_analyzers/city/<city_id>', methods=['GET'])
def gas_analyzers_by_city_id(city_id):
    """

    :return:
    """
    return "GET " + str(city_id)


# %% pipes
@app.route('/pipes', methods=['POST', 'GET'])
def pipes():
    """

    :return:
    """
    data = request.get_json()
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"


@app.route('/pipes/<measurement>', methods=['DELETE', 'GET'])
def pipes_by_id(measurement):
    """

    :return:
    """
    if request.method == 'GET':
        return "GET"
    else:
        return "DELETE"


@app.route('/pipes/company/<company_id>', methods=['GET'])
def pipes_by_companies_id(company_id):
    """

    :return:
    """
    return "GET " + str(company_id)


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
