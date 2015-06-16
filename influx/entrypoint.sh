#!/bin/bash

set -e

if [ "$1" = "influxd" ]; then
    echo "influxd bin = $INFLUX"
    echo "influx cfg file = $INFLUX_CFG"

    # Creates config file
    if [ ! -f "$INFLUX_CFG" ]; then
        su - -c "\"$INFLUX\" config" influx > "$INFLUX_CFG"
        echo "influx cfg created"
    fi;
    shift 1;

    # Add config file to parameters
    params="$@"
    if [[ ! "$params" == *" -config "* ]]; then
        params="$params -config \"$INFLUX_CFG\" "
    fi

    # Create the cmd line and execute it
    cmd="\"$INFLUX\" $params"
    exec su - -c "$cmd" - influx


else
    exec "$@";
fi;
