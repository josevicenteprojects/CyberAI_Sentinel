FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencias de sistema para wheels/nativos: cryptography, psycopg2, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      gcc \
      libssl-dev \
      libffi-dev \
      libpq-dev \
      pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instalar solo dependencias mínimas para la demo en Docker
COPY requirements.docker.txt ./
RUN pip install -r requirements.docker.txt

COPY . .

EXPOSE 8000

CMD ["python", "main_simple.py"]


