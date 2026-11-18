#!/usr/bin/env bash
# Muestra información técnica de un archivo de video
# Uso: ./inspect.sh <archivo>
set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Uso: $0 <archivo_video>"
  exit 1
fi

FILE="$1"
echo "── Información: $FILE ──────────────────────────────"
ffprobe -v quiet -print_format json -show_format -show_streams "$FILE" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
fmt = d.get('format', {})
print(f\"Formato:    {fmt.get('format_long_name', '?')}\")
print(f\"Duración:   {float(fmt.get('duration', 0)):.2f}s  ({float(fmt.get('duration', 0))/60:.1f} min)\")
print(f\"Tamaño:     {int(fmt.get('size', 0)) / 1_048_576:.1f} MB\")
print(f\"Bitrate:    {int(fmt.get('bit_rate', 0)) // 1000} kbps\")
for s in d.get('streams', []):
    t = s.get('codec_type', '?')
    c = s.get('codec_name', '?')
    if t == 'video':
        w, h = s.get('width', '?'), s.get('height', '?')
        fps_parts = s.get('r_frame_rate', '0/1').split('/')
        fps = int(fps_parts[0]) / max(int(fps_parts[1]), 1)
        print(f\"Video:      {c}  {w}x{h}  {fps:.2f}fps\")
    elif t == 'audio':
        sr = s.get('sample_rate', '?')
        ch = s.get('channels', '?')
        print(f\"Audio:      {c}  {sr}Hz  {ch}ch\")
"
