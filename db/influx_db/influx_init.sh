#!/bin/sh

set -e

#influx -execute "CREATE USER admin WITH PASSWORD '123465789' WITH ALL PRIVILEGES"

influx write \
  -b ${DOCKER_INFLUXDB_INIT_BUCKET} \
    -o ${DOCKER_INFLUXDB_INIT_ORG} \
          -f /bin/PM10.csv