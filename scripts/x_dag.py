from datetime import timedelta,  datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from x_etl import run_x_etl


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),   
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'x_dag',
    default_args=default_args,
    description='A DAG to run X ETL process',
)

run_etl = PythonOperator(
    task_id='run_x_etl_task',
    python_callable=run_x_etl,
    dag=dag,
)

run_etl