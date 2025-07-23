import requests
from pymongo import MongoClient
from datetime import datetime

def fetch_diabetes_data(**kwargs):
    try:
        # --- Extract ---
        url = "https://api.fda.gov/drug/label.json"
        params = {
            "search": "purpose:diabetes",
            "limit": 100
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        drugs = data.get("results", [])

        # --- Transform ---
        drug_summary = []
        for drug in drugs:
            drug_summary.append({
                "brand_name": drug.get("openfda", {}).get("brand_name", ["N/A"])[0],
                "generic_name": drug.get("openfda", {}).get("generic_name", ["N/A"])[0],
                "purpose": drug.get("purpose", ["N/A"])[0],
                "warnings": drug.get("warnings", ["N/A"])[0],
                "fetched_at": datetime.utcnow().isoformat()
            })

        # --- Load ---
        client = MongoClient("mongodb://mongo:27017/")
        db = client["etl_project_db"]
        collection = db["raw_diabetes_drugs"]
        collection.delete_many({})
        collection.insert_many(drug_summary)

        if kwargs.get("ti"):
            kwargs["ti"].xcom_push(key="diabetes_count", value=len(drug_summary))

    except Exception as e:
        print("Error en API OpenFDA Drug Label:", e)
        raise
