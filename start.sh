#!/bin/bash

# Start airflow
export AIRFLOW_HOME=~/airflow
airflow webserver -p 8080 -d

# Wait till airflow web-server is ready
echo "Waiting for Airflow web server..."
while true; do
  _RUNNING=$(ps aux | grep airflow-webserver | grep ready | wc -l)
  if [ $_RUNNING -eq 0 ]; then
    sleep 1
  else
    echo "Airflow web server is ready"
    break;
  fi
done

sleep 4
airflow scheduler -d


sleep 4
airflow worker -d