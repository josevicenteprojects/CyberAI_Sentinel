$ErrorActionPreference = "Stop"

if (-not (Test-Path -Path "config.env")) {
  Write-Host "config.env no encontrado. Copiando config.env.example..."
  Copy-Item -Path "config.env.example" -Destination "config.env"
}

Write-Host "Construyendo imágenes..."
docker compose build

Write-Host "Levantando servicios..."
docker compose up -d

Write-Host "Servicios levantados. API: http://localhost:8000  Docs: http://localhost:8000/docs"


