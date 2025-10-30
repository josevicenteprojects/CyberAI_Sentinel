# CyberAI Sentinel - Quickstart

## 1. Arranque en 1 comando

```bash
# Windows
./start.ps1

# Linux/Mac
./start.sh
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## 2. Variables de entorno

```bash
cp config.env.example config.env
# Edita DB_NAME, DB_USER, DB_PASSWORD si es necesario
```

## 3. Colección Postman

Importa `docs/CyberAI_Sentinel.postman_collection.json` y ejecuta las requests:
- GET `/health`
- GET `/api/v1/ml/models`
- POST `/api/v1/security/analyze`

## 4. Troubleshooting rápido
- Si la API responde 500 en endpoints que usan BD, verifica que `postgres` esté healthy (docker compose ps) y que las variables DB_* coincidan.
- Verifica puertos 8000 y 5432 libres.
