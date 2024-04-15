#!/usr/bin/env bash

# Start the app server
if [ $# -lt 3 ]; then
    printf "Usage: %s <function> <host> <port>\n" $0
    exit 1
fi
dev() {
    printf "Starting the app server on host: %s and port: %s\n" $1 $2
    export FLASK_APP=app_server
    flask run --host=$1 --port=$2
}
debug() {
    printf "Starting the app server on host: %s and port: %s\n" $1 $2
    export FLASK_APP=app_server
    export FLASK_DEBUG=1
    flask run --host=$1 --port=$2
}
"$1" "$2" "$3"
