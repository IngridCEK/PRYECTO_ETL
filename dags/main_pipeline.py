from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from transform_all import transform_all


from ingestion_infectious import fetch_infectious_data
from ingestion_diabetes import fetch_diabetes_data
from ingestion_space import fetch_people_in_space

default_args = {
    "owner": "ingrid",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 7, 22),
}

with DAG(
    "etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["massive_data_management"],
) as dag:

    task_infectious = PythonOperator(
        task_id="fetch_infectious_data",
        python_callable=fetch_infectious_data,
    )

    task_diabetes = PythonOperator(
        task_id="fetch_diabetes_data",
        python_callable=fetch_diabetes_data,
    )

    task_people_in_space = PythonOperator(
        task_id="fetch_people_in_space",
        python_callable=fetch_people_in_space,
    )
    task_transform_all = PythonOperator(
    task_id="transform_all",
    python_callable=transform_all,
)

task_infectious >> task_diabetes >> task_people_in_space >> task_transform_all
