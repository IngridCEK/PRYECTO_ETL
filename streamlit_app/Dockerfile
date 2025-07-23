FROM python:3.10

RUN apt-get update && apt-get install -y gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
