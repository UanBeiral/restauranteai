# app/bread-meat-delivery-backend/Dockerfile
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# deps do sistema (curl p/ healthcheck; libs SSL/ffi p/ wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libssl-dev libffi-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# deps Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# código
COPY app ./app

EXPOSE 8000
CMD ["gunicorn","app.main:app","-k","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:8000","--workers","2","--timeout","120"]
