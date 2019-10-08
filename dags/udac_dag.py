from datetime import datetime, timedelta
import os
import logging
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import StageToRedshiftOperator
#from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
#                                LoadDimensionOperator, DataQualityOperator)

from helpers import SqlQueries

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

#start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_source_region_name="eu-west-1",
    table="staging_events",
    s3_bucket="udacity-song-data",
    s3_key="log_data",
    dag=dag
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_source_region_name="eu-west-1",
    table="staging_songs",
    s3_bucket="udacity-song-data",
    s3_key="song_data",
    dag=dag
)

#end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


#start_operator >> stage_events_to_redshift
#start_operator >> stage_songs_to_redshift
#stage_events_to_redshift >> end_operator
#stage_songs_to_redshift >> end_operator

stage_events_to_redshift
stage_songs_to_redshift