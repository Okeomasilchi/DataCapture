#!/bin/env bash
if [ -z "$1" ]; then
    echo "Usage: $0 <command>"
    exit 1
fi
DC_MYSQL_USER=dc_dev DC_MYSQL_PWD=dc_dev_pwd DC_MYSQL_HOST=localhost DC_MYSQL_DB=dc_dev_db DC_TYPE_STORAGE=db DEBUG=True HOST="0.0.0.0" PORT=5000 "$@"
