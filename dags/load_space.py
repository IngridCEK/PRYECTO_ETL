from airflow.operators.python import PythonOperator
from pymongo import MongoClient  # Importamos MongoClient para conectarnos a la base de datos MongoDB

# Función que realiza únicamente la carga de datos de personas en el espacio a MongoDB
def load_people_in_space(ti):  # ti: instancia de la tarea en Airflow, necesaria para acceder a XCom
    try:
        # --- Load ---

        # Recuperamos los datos transformados desde XCom, enviados por la tarea 'transform_all'
        people_summary = ti.xcom_pull(
            task_ids="transform_all",               # Aquí cambiamos porque la transformación está en transform_all.py
            key="transformed_people_data"           # Esta key debe coincidir con la que usaste en transform_all.py
        )

        # Verificamos si hay datos. Si no hay, mostramos un mensaje y salimos de la función.
        if not people_summary:
            print("No hay datos transformados de personas en el espacio para cargar.")
            return

        # Nos conectamos al contenedor de MongoDB usando la URI estándar definida en Docker
        client = MongoClient("mongodb://mongo:27017/")

        # Seleccionamos la base de datos usada en el proyecto
        db = client["etl_project_db"]

        # Accedemos a la colección donde guardaremos a las personas en el espacio
        collection = db["processed_people_in_space"]

        # Borramos todos los documentos anteriores para evitar registros duplicados
        collection.delete_many({})

        # Insertamos los nuevos documentos que recibimos desde XCom
        collection.insert_many(people_summary)

        # Enviamos por XCom la cantidad de personas cargadas
        # Esto puede ser útil si más adelante queremos mostrar el total en un dashboard o monitorear cuántos registros procesamos.
        # Aunque no es obligatorio para que funcione el flujo, decidí incluirlo por si en el futuro quiero mostrar ese dato visualmente.
        ti.xcom_push(key="people_in_space_count", value=len(people_summary))
        #len() devuelve el número de elementos que hay en la lista 

        # Cerramos la conexión a la base de datos por buenas prácticas
        client.close()

    except Exception as e:
        # Si ocurre algún error, mostramos el mensaje y volvemos a lanzar la excepción para que Airflow lo capture
        print("Error al cargar datos de personas en el espacio en MongoDB:", e)
        raise

# Función que retorna el operador de Airflow para incluir esta carga en el DAG
def get_operator(dag):
    return PythonOperator(
        task_id="load_people_in_space",           # Nombre de la tarea en el DAG
        python_callable=load_people_in_space,     # Función que se va a ejecutar
        provide_context=True,                     # Necesario para acceder a 'ti' en la función
        dag=dag                                   # DAG al que pertenece esta tarea
    )
