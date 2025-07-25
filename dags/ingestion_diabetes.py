import requests
from pymongo import MongoClient  # Importamos MongoClient para conectarnos a la base de datos MongoDB
from datetime import datetime     # Para guardar la fecha y hora en que se obtuvieron los datos

# Función que realiza solo la ingesta (extracción y carga cruda) de datos de enfermedades infecciosas
def raw_infectious_data(ti):
    # Esta función se conecta a la API pública disease.sh para obtener datos de COVID por país.
    # Luego guarda esos datos crudos en MongoDB para ser transformados más adelante (en transform_all.py).
    # Finalmente, envía por XCom la cantidad de registros que se procesaron.

    try:
        # --- Extract ---

        # URL de la API con los casos de COVID por país (ordenados por casos)
        api_url = "https://disease.sh/v3/covid-19/countries?yesterday=true&sort=cases"

        # Realizamos una solicitud GET a la API
        response = requests.get(api_url)
        response.raise_for_status()                        # Si ocurre un error con la API, se detiene aquí
        api_response_json = response.json()                # Convertimos la respuesta a formato JSON

        # Seleccionamos solo los 100 países con más casos (para no saturar la base de datos)
        top_100_countries = api_response_json[:100]

        # --- Load ---

        # Conexión a la base de datos MongoDB
        mongo_client = MongoClient("mongodb://mongo:27017/")
        database = mongo_client["etl_project_db"]
        infectious_collection = database["raw_infectious_diseases"]  # Colección donde guardamos datos crudos

        infectious_collection.delete_many({})                     # Eliminamos registros anteriores (si existen)
        infectious_collection.insert_many(top_100_countries)      # Insertamos los nuevos documentos crudos

        # Usamos XCom para comunicar cuántos registros se ingresaron (útil para monitoreo en Airflow)
        ti.xcom_push(key="infectious_count", value=len(top_100_countries))

    except Exception as error:
        # Si ocurre algún error en cualquier parte del proceso, lo imprimimos y lanzamos la excepción
        print("Error en API disease:", error)
        raise
