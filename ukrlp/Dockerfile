FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY client ./client
COPY worker ./worker

CMD ["python", "-m", "worker.temporal_worker"]
