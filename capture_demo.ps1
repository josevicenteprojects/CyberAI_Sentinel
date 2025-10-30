$ErrorActionPreference = 'Stop'

function Get-FFmpegPath {
  $path = (Get-Command ffmpeg -ErrorAction SilentlyContinue).Path
  if ($path) { return $path }
  try {
    winget --version | Out-Null
    winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements -h | Out-Null
    Start-Sleep -Seconds 3
  } catch {}
  return (Get-Command ffmpeg -ErrorAction SilentlyContinue).Path
}

Push-Location "$PSScriptRoot"
try {
  # Arrancar servicios
  if (Test-Path './start.ps1') { ./start.ps1; Start-Sleep -Seconds 8 }

  # Abrir Swagger
  Start-Process 'http://localhost:8000/docs'

  # Carpetas docs
  $dirs = @('docs','docs/gifs','docs/capturas')
  foreach ($d in $dirs) { if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null } }

  # ffmpeg
  $ff = Get-FFmpegPath
  if (-not $ff) { Write-Host 'ffmpeg no disponible. Instálalo y reintenta.'; exit 1 }

  $mp4 = 'docs/gifs/demo.mp4'
  $palette = 'docs/gifs/palette.png'
  $gif = 'docs/gifs/demo_20s.gif'

  & $ff -y -f gdigrab -framerate 30 -i desktop -t 00:00:25 $mp4
  & $ff -y -i $mp4 -vf 'fps=15,scale=1280:-1:flags=lanczos,palettegen' $palette
  & $ff -y -i $mp4 -i $palette -lavfi 'fps=15,scale=1280:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=sierra2_4a' $gif

  Write-Host "GIF generado en: $(Resolve-Path $gif)"
}
finally { Pop-Location }
