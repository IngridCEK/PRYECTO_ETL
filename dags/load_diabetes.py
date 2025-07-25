from airflow.operators.python import PythonOperator
from pymongo import MongoClient  # Importamos MongoClient para conectarnos a la base de datos MongoDB

# Función que realiza únicamente la carga de datos de personas en el espacio a MongoDB
def load_people_in_space(ti):  # ti: instancia de la tarea en Airflow, necesaria para acceder a XCom
    try:
        # --- Load ---

        # Recuperamos los datos transformados desde XCom, enviados por la tarea transform_all (archivo transform_all.py)
        people_summary = ti.xcom_pull(
            task_ids="transform_all",                # Aquí indicamos que los datos vienen del transform_all.py
            key="transformed_people_data"            # Esta clave debe coincidir con la usada en ti.xcom_push() dentro de transform_all.py
        )

        # Verificamos si los datos existen. Si no hay, simplemente salimos
        if not people_summary:
            print("No hay datos transformados de personas en el espacio para cargar.")
            return

        # Conectamos a la base de datos MongoDB (desde el contenedor definido en docker-compose)
        client = MongoClient("mongodb://mongo:27017/")

        # Accedemos a la base de datos principal del proyecto
        db = client["etl_project_db"]

        # Elegimos la colección específica para personas en el espacio
        collection = db["people_in_space"]

        # Borramos documentos anteriores para evitar duplicados
        collection.delete_many({})

        # Insertamos los nuevos datos transformados en MongoDB
        collection.insert_many(people_summary)

        # Enviamos la cantidad de registros insertados por XCom
        # Esto lo hago para poder usar ese dato luego en dashboards, o simplemente monitorear que todo esté funcionando bien
        ti.xcom_push(key="people_in_space_count", value=len(people_summary))

        # Cerramos la conexión por buenas prácticas
        client.close()

    except Exception as e:
        # Si hay errores, los mostramos para que Airflow los registre
        print("Error al cargar datos de personas en el espacio en MongoDB:", e)
        raise

# Esta función devuelve un operador PythonOperator ya configurado, listo para ser añadido al DAG
def get_operator(dag):
    return PythonOperator(
        task_id="load_people_in_space",           # Nombre único de la tarea en el DAG
        python_callable=load_people_in_space,     # Función que se ejecutará en esta tarea
        provide_context=True,                     # Esto permite que Airflow le pase el contexto a la función, como ti
        dag=dag                                   # Referencia al DAG al que pertenece esta tarea
    )
