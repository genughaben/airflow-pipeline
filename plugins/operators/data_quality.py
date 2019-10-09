from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 expected_counts=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.tables=tables
        self.expected_counts=expected_counts

    def execute(self, context):
        self.log.info('Detect number of entries per table, optionally compare to expected numbers')

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for idx, table in enumerate(self.tables):
            query = f"SELECT COUNT(*) FROM {table};"
            count = redshift.get_first(query)[0]
            print(f"result of {query} is {count}")
            if len(self.expected_counts) > 0:
                expected_count = self.expected_counts[idx]
                if count != expected_count:
                    print(f"Validation error: table {table} contains {count} records while {expected_count} where expected.")
                else:
                    print(f"Validation success: table {table} contains {count} records as expected.")
            else:
                if count > 0:
                    print(f"Validation success: table {table} contains {count} records.")
                else:
                    print(f"Validation error: table {table} contains no records while some records where expected.")

        return True