from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importamos las funciones de ingesta que solo hacen la parte cruda (raw)
from raw_infectious_data import raw_infectious_data
from raw_diabetes_data import raw_diabetes_data
from raw_people_in_space import raw_people_in_space

# Importamos la función central que transforma y carga todos los datos
from transform_all import transform_all

# Configuraciones generales del DAG (como si fueran reglas de operación)
default_args = {
    "owner": "ingrid",  # Dice que yo soy la responsable del DAG
    "depends_on_past": False,  # Cada ejecución es independiente de la anterior
    "retries": 1,  # Si falla, reintenta 1 vez
    "retry_delay": timedelta(minutes=5),  # Espera 5 minutos antes del reintento
    "start_date": datetime(2025, 7, 22),  # Fecha de inicio del DAG
}

# Aquí declaramos el DAG principal que orquesta todo el flujo
with DAG(
    dag_id="etl_pipeline",  # Este es el nombre que se verá en la interfaz de Airflow
    default_args=default_args,
    schedule_interval="@daily",  # El DAG se ejecuta una vez al día
    catchup=False,  # No intenta "ponerse al día" si algún día no se ejecutó
    max_active_runs=1,  # Solo permite una ejecución activa a la vez
    tags=["massive_data_management"],  # Etiqueta que usamos para identificar este DAG
) as dag:

    # Tarea 1: Ingesta cruda de datos sobre enfermedades infecciosas
    ingest_infectious_task = PythonOperator(
        task_id="raw_infectious_data",
        python_callable=raw_infectious_data,
    )

    # Tarea 2: Ingesta cruda de medicamentos relacionados con diabetes
    ingest_diabetes_task = PythonOperator(
        task_id="raw_diabetes_data",
        python_callable=raw_diabetes_data,
    )

    # Tarea 3: Ingesta cruda de personas actualmente en el espacio
    ingest_space_task = PythonOperator(
        task_id="raw_people_in_space",
        python_callable=raw_people_in_space,
    )

    # Tarea 4: Transformación y carga final de todos los datos procesados
    transform_and_load_task = PythonOperator(
        task_id="transform_all",
        python_callable=transform_all,
    )

    # Definimos el orden en que se ejecutan las tareas (de izquierda a derecha)
    ingest_infectious_task >> ingest_diabetes_task >> ingest_space_task >> transform_and_load_task
