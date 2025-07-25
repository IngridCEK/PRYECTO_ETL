# ETL Project with Airflow, MongoDB, and Streamlit

This project implements a complete ETL (Extract, Transform, Load) pipeline using Apache Airflow for orchestration, MongoDB for data storage, and Streamlit for data visualization. All components are containerized and managed using Docker Compose.

## Project Components

- **Apache Airflow**: Manages and schedules data workflows.
- **MongoDB**: Stores raw and processed data in a NoSQL format.
- **Streamlit**: Provides a graphical dashboard to explore the processed data.
- **Docker Compose**: Orchestrates all services in isolated containers.

---

## Prerequisites

- Docker and Docker Compose must be installed on the system.
- No folders or files need to be created manually. All necessary files are included in the provided project directory.

---

## Instructions to Run the System

### 1. Navigate to the Project Folder

Open a terminal and move to the root directory of the unzipped project:

```bash
cd ~/Documents/pryecto_etl/PRYECTO_ETL
<<<<<<< HEAD
=======

>>>>>>> 011ddc4 (Actualización con nuevos archivos y cambios (sin archivos eliminados))
```

### 2. Initialize the Airflow Database (only once)

```bash
docker compose run --rm webserver airflow db init
```

This command initializes the metadata database used by Airflow.

### 3. Create the Airflow Admin User (only once)

```bash
docker compose run --rm webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

These are the login credentials for accessing the Airflow web interface:

- **Username:** `admin`
- **Password:** `admin`

### 4. Build and Start All Containers

```bash
docker compose up -d
```

This command starts the following services in the background:

- **Airflow Webserver** – [http://localhost:8080](http://localhost:8080)
- **Airflow Scheduler**
- **MongoDB** – Exposed on port `27017`
- **Streamlit Dashboard** – [http://localhost:8501](http://localhost:8501)

---

## Usage Guide

### Access the Airflow Interface

1. Open your browser and go to: [http://localhost:8080](http://localhost:8080)
2. Log in with:
   - **Username:** `admin`
   - **Password:** `admin`
3. Locate the DAG named: `etl_pipeline`
4. Unpause the DAG and trigger it manually.
5. Wait until all tasks complete successfully (green status).

### Access the Streamlit Dashboard

Once the DAG finishes execution:

Open: [http://localhost:8501](http://localhost:8501)

This dashboard provides visualizations of the processed data, including:

- COVID-19 case counts per country
- List of diabetes medications with warnings
- Number of people in space per spacecraft

---

## Stopping the Services

To stop all running containers:

```bash
docker compose down
```

