# CLAUDE-V-DEOS — Entorno de Edición de Video

## Estructura

```
originals/      → Videos fuente (NO se sube a git)
  footage/      → Grabaciones propias
  downloaded/   → Descargados con yt-dlp

projects/       → Un directorio por proyecto
  <nombre>/
    scripts/    → Scripts de edición para ese proyecto
    notes.md    → Notas y timeline

resources/      → Assets reutilizables (SÍ en git si son pequeños)
  fonts/
  music/
  sfx/
  overlays/     → Logos, watermarks, transiciones
  luts/         → LUTs de color

exports/        → Renders finales
  youtube/
  instagram/
  master/       → Alta calidad (NO en git)

temp/           → Archivos intermedios (NO en git)
tools/          → Scripts y presets de codificación
```

## Herramientas disponibles

| Herramienta | Versión | Uso |
|-------------|---------|-----|
| FFmpeg | 6.1.1 | Codificación, corte, filtros |
| yt-dlp | 2026.10.26 | Descarga de plataformas |
| MoviePy | 2.1.2 | Edición programática Python |
| PyAV | 19.0.2 | Lectura/escritura video Python |
| faster-whisper | — | Transcripción y subtítulos |

## Scripts de utilidad

```bash
# Inspeccionar un video
bash tools/scripts/inspect.sh originals/footage/mi_video.mp4

# Exportar para web
bash tools/scripts/encode_web.sh originals/footage/entrada.mp4 exports/youtube/salida.mp4 22

# Transcribir a SRT
python3 tools/scripts/transcribe.py originals/footage/mi_video.mp4 es

# Descargar video de YouTube
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" \
  -o "originals/downloaded/%(title)s.%(ext)s" <URL>
```

## Reglas importantes

- **Nunca** commitear videos originales (`originals/` está en .gitignore)
- Los renders finales pesados van en `exports/master/` (también ignorado)
- El directorio `temp/` es desechable
- Commitear solo: scripts, presets, notas de proyecto, assets pequeños
