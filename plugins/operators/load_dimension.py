from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import insert_table_queries

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table

    def execute(self, context):
        redshift = PostgresHook(self.redshift_conn_id)
        sql_query = insert_table_queries[self.table]

        self.log.info(f"Load data to table {self.table} executing {sql_query} ...")
        ret = redshift.run(sql_query)
        self.log.info(f"Insert data to table {self.table} finished.")
        return ret