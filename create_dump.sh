#!/bin/env bash
# creates a mysql dump file
sudo mysqldump dc_dev_db > dumpfile.sql
echo "Dump file created"
