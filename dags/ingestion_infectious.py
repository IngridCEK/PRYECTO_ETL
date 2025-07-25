import requests
from pymongo import MongoClient ## Importamos MongoClient para conectarnos a la base de datos MongoDB
from datetime import datetime

# Definimos la función principal de ETL para enfermedades infecciosas
def raw_infectious_data(ti):
    #ti: Instancia de la tarea de Airflow, utilizada para manejar XCom entre tareas
    try:
        # --- Extract ---
        # # Definimos la URL de la API disease.sh para casos de COVID por país
        url = "https://disease.sh/v3/covid-19/countries?yesterday=true&sort=cases"
        response = requests.get(url) 
        # Hacemos una solicitud GET a la API
        response.raise_for_status()
        data = response.json() ## Convertimos la respuesta en formato JSON
        top_countries = data[:100]# # Seleccionamos solo los primeros 100 países con más casos

        # --- Transform ---
        infectious_disease_summary = []
        # # Recorremos cada país en el top 100
        for country in top_countries:
            infectious_disease_summary.append({
                #  Extraemos los datos importantes de cada país
                "country": country.get("country"),
                "cases": country.get("cases"),
                "deaths": country.get("deaths"),
                "recovered": country.get("recovered"),
                "fetched_at": datetime.utcnow().isoformat()
            })

        # --- Load ---
        client = MongoClient("mongodb://mongo:27017/")
        db = client["etl_project_db"] #  Accedemos a la base de datos usada en el proyecto
        collection = db["raw_infectious_diseases"]
        collection.delete_many({})
        collection.insert_many(infectious_disease_summary) ## Insertamos la nueva lista de documentos (ya transformados)

        # # Si se ejecuta desde Airflow y se proporciona `ti`, enviamos la cantidad de registros procesados a XCom
        ti.xcom_push(key="infectious_count", value=len(infectious_disease_summary))

    except Exception as e:
        print("Error en API disease.sh:", e)
        raise
