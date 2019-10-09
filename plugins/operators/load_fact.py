from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import insert_table_queries

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        self.log.info('Insert songplay data...')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        insert_sql = insert_table_queries["songplays"]

        self.log.info(f'Execute: {insert_sql}')
        ret = redshift.run(insert_sql)
        self.log.info(f"Insert songplays data finished.")
        return ret

