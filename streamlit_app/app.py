import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

st.set_page_config(page_title="ETL Dashboard", layout="wide")

# Conexión a MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["etl_project_db"]

st.title(" ETL Dashboard - Proyecto de Gestión Masiva de Datos")

# --- COVID / Infectious ---
st.header("COVID-19: Casos por país")
data = list(db["processed_infectious_diseases"].find())
df = pd.DataFrame(data)
if not df.empty:
    top_n = st.slider("Mostrar los países con más casos", 5, 100, 10)
    top_countries = df.sort_values("cases", ascending=False).head(top_n)
    st.bar_chart(top_countries.set_index("country")["cases"])
    
    # Métricas corregidas
    st.metric("País con más casos", top_countries.iloc[0]["country"])
    st.metric("Número de casos", f"{top_countries.iloc[0]['cases']:,}")
# --- Diabetes Drugs ---
st.header("Medicamentos para Diabetes")
df2 = pd.DataFrame(list(db["processed_diabetes_drugs"].find()))
if not df2.empty:
    if st.checkbox("Mostrar solo medicamentos con advertencias serias"):
        df2 = df2[df2["is_serious_warning"] == True]
    st.dataframe(df2[["brand_name", "generic_name", "warnings"]].reset_index(drop=True))

# --- space ---
st.header(" Personas en el espacio")
df3 = pd.DataFrame(list(db["processed_people_in_space"].find()))
if not df3.empty:
    st.write("Cantidad por nave espacial:")
    counts = df3["craft"].value_counts().reset_index()
    counts.columns = ["craft", "count"]
    st.bar_chart(counts.set_index("craft"))
