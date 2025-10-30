#!/usr/bin/env bash
set -euo pipefail

if [ ! -f "config.env" ]; then
  echo "config.env no encontrado. Copiando config.env.example..."
  cp config.env.example config.env
fi

echo "Construyendo imágenes..."
docker compose build

echo "Levantando servicios..."
docker compose up -d

echo "Servicios levantados. API: http://localhost:8000  Docs: http://localhost:8000/docs"


