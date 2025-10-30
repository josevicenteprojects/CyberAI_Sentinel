# Guía de Capturas y GIF (CyberAI Sentinel)

## 1) Grabación (recomendado OBS Studio)
- Escena: Captura de ventana del navegador en 1080p
- FPS: 30
- Formato: MP4 (h264 + AAC)
- Duración objetivo: 20–30s

Secuencia sugerida:
1) Abrir http://localhost:8000/docs (Swagger)
2) Ejecutar GET /health
3) Ejecutar GET /api/v1/ml/models
4) Ejecutar POST /api/v1/security/analyze con el payload de ejemplo

## 2) Conversión MP4 → GIF (ffmpeg)
Genera paleta y aplica para colores óptimos (dos pasos):

```bash
# Windows PowerShell
ffmpeg -y -i .\docs\gifs\demo.mp4 -vf "fps=15,scale=1280:-1:flags=lanczos,palettegen" .\docs\gifs\palette.png
ffmpeg -y -i .\docs\gifs\demo.mp4 -i .\docs\gifs\palette.png -lavfi "fps=15,scale=1280:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=sierra2_4a" .\docs\gifs\demo_20s.gif

# Linux/Mac
ffmpeg -y -i ./docs/gifs/demo.mp4 -vf "fps=15,scale=1280:-1:flags=lanczos,palettegen" ./docs/gifs/palette.png
ffmpeg -y -i ./docs/gifs/demo.mp4 -i ./docs/gifs/palette.png -lavfi "fps=15,scale=1280:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=sierra2_4a" ./docs/gifs/demo_20s.gif
```

Opcional (recortar inicio/fin):
```bash
ffmpeg -ss 00:00:02 -t 00:00:22 -i ./docs/gifs/demo.mp4 -c copy ./docs/gifs/demo_trim.mp4
```

## 3) Convenciones de nombres
- Capturas (PNG):
  - `docs/capturas/01_swagger.png`
  - `docs/capturas/02_health.png`
  - `docs/capturas/03_ml_models.png`
  - `docs/capturas/04_analyze_request.png`
- GIF final: `docs/gifs/demo_20s.gif`

## 4) Checklist de calidad
- Resolución 1280×720 o 1920×1080
- Texto legible sin zoom excesivo
- Duración 20–30s
- Tamaño < 8–10 MB si es posible
