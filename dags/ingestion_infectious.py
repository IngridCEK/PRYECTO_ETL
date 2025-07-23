import requests
from pymongo import MongoClient
from datetime import datetime

def fetch_infectious_data(**kwargs):
    try:
        # --- Extract ---
        url = "https://disease.sh/v3/covid-19/countries?yesterday=true&sort=cases"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        top_countries = data[:100]

        # --- Transform ---
        infectious_disease_summary = []
        for country in top_countries:
            infectious_disease_summary.append({
                "country": country.get("country"),
                "cases": country.get("cases"),
                "deaths": country.get("deaths"),
                "recovered": country.get("recovered"),
                "fetched_at": datetime.utcnow().isoformat()
            })

        # --- Load ---
        client = MongoClient("mongodb://mongo:27017/")
        db = client["etl_project_db"]
        collection = db["raw_infectious_diseases"]
        collection.delete_many({})
        collection.insert_many(infectious_disease_summary)

        if kwargs.get("ti"):
            kwargs["ti"].xcom_push(key="infectious_count", value=len(infectious_disease_summary))

    except Exception as e:
        print("Error en API disease.sh:", e)
        raise
