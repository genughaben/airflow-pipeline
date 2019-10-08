from datetime import datetime, timedelta
import os
import logging
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import StageToRedshiftOperator
#from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
#                                LoadDimensionOperator, DataQualityOperator)

from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'depends_on_past': False,
    'catchup_by_default': False,
    'max_active_runs':1
}

dag = DAG(
    'udac_dag',
    description='Testing',
    start_date=datetime(2019, 10, 5, 0, 0, 0, 0),
    schedule_interval='@monthly'
)


stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    region_name="us-west-2",
    table="staging_events",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    dag=dag
)


stage_events_to_redshift