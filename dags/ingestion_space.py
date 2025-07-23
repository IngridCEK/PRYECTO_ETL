import requests
from pymongo import MongoClient
from datetime import datetime

def fetch_people_in_space(**kwargs):
    try:
        # --- Extract ---
        url = "http://api.open-notify.org/astros.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # --- Transform ---
        people_summary = []
        for person in data.get("people", []):
            people_summary.append({
                "name": person.get("name", "N/A"),
                "craft": person.get("craft", "N/A"),
                "fetched_at": datetime.utcnow().isoformat()
            })

        # --- Load ---
        client = MongoClient("mongodb://mongo:27017/")
        db = client["etl_project_db"]
        collection = db["people_in_space"]
        collection.delete_many({})
        collection.insert_many(people_summary)

        # XCom push
        if kwargs.get("ti"):
            kwargs["ti"].xcom_push(key="people_in_space_count", value=len(people_summary))

    except Exception as e:
        print("Error en API Open Notify (personas en el espacio):", e)
        raise
