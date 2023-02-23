#!/bin/sh

set -e

influx write \
  -b EcoBucket \
    -o ${DOCKER_INFLUXDB_INIT_ORG} \
          -f /bin/pollution.csv