#!/bin/env bash
# FILEPATH: /home/okeoma/Desktop/DataCapture/resedb.sh
# echo "DROP DATABASE dc_dev_db;" | sudo mysql
cat setup_mysql_dev.sql | mysql
