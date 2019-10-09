from datetime import datetime, timedelta
import os
import logging
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (CreateDatabaseSchema, StageToRedshiftOperator,
                               LoadFactOperator, LoadDimensionOperator)

default_args = {
    'depends_on_past': False,
    'catchup_by_default': False,
    'max_active_runs':1
}

dag = DAG(
    "udac_dag",
    description="Testing",
    start_date=datetime(2019, 10, 5, 0, 0, 0, 0),
    schedule_interval="@monthly"
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

re_create_db_schema = CreateDatabaseSchema(
    task_id="Drop_and_create_db_schema",
    redshift_conn_id="redshift",
    to_exec=True,
    dag=dag
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id="Stage_events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_source_region_name="eu-west-1",
    table="staging_events",
    s3_bucket="udacity-song-data",
    s3_key="log_data",
    dag=dag
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id="Stage_songs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_source_region_name="eu-west-1",
    table="staging_songs",
    s3_bucket="udacity-song-data",
    s3_key="song_data",
    dag=dag
)

load_songplays_table = LoadFactOperator(
    task_id="Load_songplays_fact_table",
    redshift_conn_id="redshift",
    dag=dag
)

load_dim_time_table = LoadDimensionOperator(
    task_id="Load_dim_time_table",
    redshift_conn_id="redshift",
    table="time",
    dag=dag
)

load_dim_users_table = LoadDimensionOperator(
    task_id="Load_dim_users_table",
    redshift_conn_id="redshift",
    table="users",
    dag=dag
)

load_dim_songs_table = LoadDimensionOperator(
    task_id="Load_dim_songs_table",
    redshift_conn_id="redshift",
    table="songs",
    dag=dag
)

load_dim_artists_table = LoadDimensionOperator(
    task_id="Load_dim_artists_table",
    redshift_conn_id="redshift",
    table="artists",
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> re_create_db_schema
re_create_db_schema >> stage_events_to_redshift
re_create_db_schema >> stage_songs_to_redshift
stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table
load_songplays_table >> load_dim_time_table
load_songplays_table >> load_dim_users_table
load_songplays_table >> load_dim_songs_table
load_songplays_table >> load_dim_artists_table
load_dim_time_table >> end_operator
load_dim_users_table >> end_operator
load_dim_songs_table >> end_operator
load_dim_artists_table >> end_operator