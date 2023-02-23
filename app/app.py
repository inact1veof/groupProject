from flask import Flask, jsonify

from connections.influx_connection import InfluxConnection
from connections.postgres_connection import PostgresConnection
from logger import get_logger

postgres_connection = PostgresConnection()
influx_connection = InfluxConnection()

app = Flask(__name__)
logger = get_logger(__name__)

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

