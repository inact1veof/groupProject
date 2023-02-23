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
def cities():
    """

    :return:
    """
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"


@app.route('/cities/<id>', methods=['DELETE', 'GET'])
def cities(id):
    """

    :return:
    """
    # id = request.args.get('id')
    if request.method == 'GET':
        return "GET"
    else:
        return "DELETE"


# %% companies
@app.route('/companies', methods=['POST', 'GET'])
def companies():
    """

    :return:
    """
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"


@app.route('/companies/<id>', methods=['DELETE', 'GET'])
def companies(id):
    """

    :return:
    """
    # id = request.args.get('id')
    if request.method == 'GET':
        return "GET"
    else:
        return "DELETE"


@app.route('/companies/city/<city_id>', methods=['GET'])
def companies_by_city_id(city_id):
    """

    :return:
    """
    # id = request.args.get('id')
    return "GET " + str(city_id)


# %% gas_analyzers
@app.route('/gas_analyzers', methods=['POST', 'GET'])
def gas_analyzers():
    """

    :return:
    """
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"


@app.route('/gas_analyzers/<measurement>', methods=['DELETE', 'GET'])
def gas_analyzers(measurement):
    """

    :return:
    """
    # id = request.args.get('measurement')
    if request.method == 'GET':
        return "GET"
    else:
        return "DELETE"


@app.route('/gas_analyzers/city/<city_id>', methods=['GET'])
def gas_analyzers_by_city_id(city_id):
    """

    :return:
    """
    # id = request.args.get('id')
    return "GET " + str(city_id)


# %% pipes
@app.route('/pipes', methods=['POST', 'GET'])
def pipes():
    """

    :return:
    """
    if request.method == 'GET':
        return "GET"
    else:
        return "POST"


@app.route('/pipes/<measurement>', methods=['DELETE', 'GET'])
def pipes(measurement):
    """

    :return:
    """
    # id = request.args.get('measurement')
    if request.method == 'GET':
        return "GET"
    else:
        return "DELETE"


@app.route('/pipes/company/<company_id>', methods=['GET'])
def pipes_by_companies_id(company_id):
    """

    :return:
    """
    # id = request.args.get('id')
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
