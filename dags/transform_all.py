from pymongo import MongoClient
from datetime import datetime

def transform_all(**kwargs):
    client = MongoClient("mongodb://mongo:27017/")
    db = client["etl_project_db"]

    # --- Transform Infectious Diseases ---
    raw_infectious = db["raw_infectious_diseases"].find()
    infectious_processed = []
    for record in raw_infectious:
        if not record.get("cases") or not record.get("deaths"):
            continue
        fatality_rate = record["deaths"] / record["cases"] if record["cases"] else 0
        infectious_processed.append({
            "country": record["country"],
            "cases": record["cases"],
            "deaths": record["deaths"],
            "recovered": record["recovered"],
            "fatality_rate": round(fatality_rate, 4),
            "is_critical": record["cases"] > 1_000_000,
            "transformed_at": datetime.utcnow().isoformat()
        })
    db["processed_infectious_diseases"].delete_many({})
    db["processed_infectious_diseases"].insert_many(infectious_processed)

    # --- Transform Diabetes Drugs ---
    raw_diabetes = db["raw_diabetes_drugs"].find()
    diabetes_processed = []
    for drug in raw_diabetes:
        warning = drug.get("warnings", "")
        warning_flag = "serious" in warning.lower()
        diabetes_processed.append({
            "brand_name": drug.get("brand_name", "N/A"),
            "generic_name": drug.get("generic_name", "N/A"),
            "purpose": drug.get("purpose", "N/A"),
            "warnings": warning,
            "is_serious_warning": warning_flag,
            "warning_length": len(warning),
            "transformed_at": datetime.utcnow().isoformat()
        })
    db["processed_diabetes_drugs"].delete_many({})
    db["processed_diabetes_drugs"].insert_many(diabetes_processed)

    # --- Transform People in Space ---
    raw_space = list(db["people_in_space"].find())
    space_processed = []
    craft_counts = {}
    for person in raw_space:
        craft = person.get("craft", "unknown")
        craft_counts[craft] = craft_counts.get(craft, 0) + 1
    for person in raw_space:
        space_processed.append({
            "name": person.get("name", "N/A"),
            "craft": person.get("craft", "unknown"),
            "crew_size": craft_counts.get(person.get("craft", "unknown"), 1),
            "is_iss": person.get("craft", "").lower() == "iss",
            "transformed_at": datetime.utcnow().isoformat()
        })
    db["processed_people_in_space"].delete_many({})
    db["processed_people_in_space"].insert_many(space_processed)
