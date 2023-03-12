import os

# postgresdb variables
postgres_config = dict(
    POSTGRES_USER =     os.getenv("POSTGRES_USER", "user"),
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password"),
    POSTGRES_DB =       os.getenv("POSTGRES_DB", "default"),
    DB_HOST =           os.getenv("DB_HOST", "db"),
    DB_PORT =           os.getenv("DB_PORT", 5432)
)

# influxdb variables
influx_config = dict(
    DOCKER_INFLUXDB_INIT_MODE = os.getenv(
        "DOCKER_INFLUXDB_INIT_MODE","setup"),
    DOCKER_INFLUXDB_INIT_USERNAME = os.getenv(
        "DOCKER_INFLUXDB_INIT_USERNAME","user"),
    DOCKER_INFLUXDB_INIT_PASSWORD = os.getenv(
        "DOCKER_INFLUXDB_INIT_PASSWORD","password"),
    DOCKER_INFLUXDB_INIT_ORG = os.getenv(
        "DOCKER_INFLUXDB_INIT_ORG","myorg"),
    DOCKER_INFLUXDB_INIT_BUCKET = os.getenv(
        "DOCKER_INFLUXDB_INIT_BUCKET","mybucket"),
    DOCKER_INFLUXDB_INIT_ADMIN_TOKEN = os.getenv(
        "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN","mytoken")
)

cron_config = dict(
    CRON_POSTGRES_USER = os.getenv(
        "CRON_POSTGRES_USER","mycron"
    ),
    CRON_POSTGRES_VALUE = os.getenv(
        "CRON_POSTGRES_VALUE","mycronpassword"
    )
)

# logging variables
LOGGING_PATH: str = os.getenv("LOGGING_PATH", "logs")

LOGGING_FORMAT: str = os.getenv(
    "LOGGING_FORMAT", "%(name)s %(asctime)s %(levelname)s %(message)s"
)
LOGGING_LEVEL: str = os.getenv("LOGGING_LEVEL", "INFO")