import requests
from pymongo import MongoClient  # Importamos MongoClient para conectarnos a la base de datos MongoDB
from datetime import datetime     # Para guardar la fecha y hora en que se obtuvieron los datos

# Función que realiza la ingesta (extracción + carga cruda) de personas actualmente en el espacio
def raw_people_in_space(ti):
    # Esta función se conecta a la API pública open-notify.org
    # para obtener la lista de astronautas actualmente en el espacio.
    # Luego guarda esa información sin transformar en una colección de MongoDB.

    try:
        # --- Extract ---

        # URL de la API que indica cuántas personas hay actualmente en el espacio
        api_url = "http://api.open-notify.org/astros.json"

        # Realizamos la solicitud GET
        response = requests.get(api_url)
        response.raise_for_status()                        # Si la API falla, lanzamos un error
        api_response_json = response.json()                # Convertimos la respuesta en formato JSON

        # Obtenemos la lista de personas desde la clave 'people'
        raw_astronaut_list = api_response_json.get("people", [])

        # --- Load ---

        # Conectamos a la base de datos MongoDB
        mongo_client = MongoClient("mongodb://mongo:27017/")
        database = mongo_client["etl_project_db"]
        space_collection = database["people_in_space"]  # Colección donde se guardarán los datos crudos

        # Insertamos cada persona tal como fue obtenida
        space_collection.delete_many({})                  # Limpiamos la colección antes de insertar nuevos datos
        space_collection.insert_many(raw_astronaut_list)  # Insertamos los datos crudos

        # Enviamos la cantidad de astronautas encontrados a XCom (útil si luego se quiere mostrar en dashboard)
        ti.xcom_push(key="people_in_space_count", value=len(raw_astronaut_list))

    except Exception as error:
        print("Error en API Open Notify (personas en el espacio):", error)
        raise

