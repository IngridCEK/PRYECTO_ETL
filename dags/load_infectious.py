from airflow.operators.python import PythonOperator
from pymongo import MongoClient  # Usamos esta librería para conectarnos a MongoDB desde Python

# Configuración para acceder a la base de datos MongoDB
mongo = "mongodb://mongo:27017"         # URI de conexión, basada en el contenedor Docker
name = "etl_project_db"                 # Nombre de la base de datos
collection = "infectious_diseases"      # Nombre de la colección (tabla) donde vamos a guardar los datos

# Esta función carga los datos transformados (de enfermedades infecciosas) a MongoDB
def load_infectious_data_callable(ti):  # ti: instancia de la tarea de Airflow, necesaria para usar XCom
    # Recuperamos los datos que se transformaron en la tarea transform_all (vía XCom)
    transformed_data = ti.xcom_pull(
        task_ids='transform_all',                      # Los datos vienen del script transform_all.py
        key='transformed_infectious_data'              # Esta clave debe coincidir con la usada en transform_all.py
    )

    # Si no hay datos, simplemente mostramos un mensaje y no hacemos nada
    if not transformed_data:
        print("No hay datos transformados para cargar.")
        return

    # Nos conectamos a MongoDB
    client = MongoClient(mongo)
    db = client[name]
    collection_obj = db[collection]  # Accedemos a la colección específica (infectious_diseases)

    # Insertamos los datos solo si son una lista válida
    if isinstance(transformed_data, list) and transformed_data:
        collection_obj.delete_many({})       # Limpiamos datos anteriores para evitar duplicados
        collection_obj.insert_many(transformed_data)  # Insertamos todos los nuevos datos
        print(f"{len(transformed_data)} registros insertados en MongoDB.")
    else:
        print("Los datos transformados no están en el formato esperado.")

    # Cerramos la conexión como buena práctica
    client.close()

# Esta función retorna el operador de Airflow ya configurado para usarse en el DAG
def get_operator(dag):
    return PythonOperator(
        task_id='load_infectious_data',             # Nombre de la tarea en el DAG
        python_callable=load_infectious_data_callable,  # Función que se va a ejecutar
        provide_context=True,                       # Necesario para que Airflow pase 'ti'
        dag=dag
    )

