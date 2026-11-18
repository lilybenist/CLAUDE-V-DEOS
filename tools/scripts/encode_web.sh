#!/usr/bin/env bash
# Exporta un video optimizado para web (H.264/AAC, compatible YouTube/Instagram)
# Uso: ./encode_web.sh <entrada> <salida> [calidad: 18-28, default 22]
set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"
CRF="${3:-22}"

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
  echo "Uso: $0 <entrada> <salida> [crf: 18-28]"
  echo "  crf 18 = alta calidad (~grande), 28 = menor calidad (~pequeño)"
  exit 1
fi

ffmpeg -i "$INPUT" \
  -c:v libx264 -crf "$CRF" -preset slow \
  -profile:v high -level 4.1 \
  -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  "$OUTPUT"

echo "✓ Exportado: $OUTPUT"
ffprobe -v quiet -show_format "$OUTPUT" | grep -E "duration|size|bit_rate"
