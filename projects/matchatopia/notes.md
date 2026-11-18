# MATCHATOPÍA — Iced Matcha ASMR

## Footage
- 10 clips 4K 120fps HEVC (iPad), en `originals/footage/MATCHATOPÍA/CONTENIDO/`
- 2 videos de referencia, en `originals/footage/MATCHATOPÍA/REFERENCIAS/`

## Secuencia del video
| # | Clip       | Escena                     | Duración slow (5×) |
|---|------------|----------------------------|---------------------|
| 0 | título     | "iced matcha / asmr"       | 2.5s                |
| 1 | IMG_0772   | Tamizando matcha (top-down)| 7.5s                |
| 2 | IMG_0770   | Kettle calentando agua     | 6s                  |
| 3 | IMG_0774   | Vertiendo agua en chawan   | 10s                 |
| 4 | IMG_0776   | Batiendo con chasen        | 7.5s                |
| 5 | IMG_0779   | Leche fría sobre hielo     | 6.5s                |
| 6 | IMG_0780   | Vertiendo matcha en vaso   | 10s                 |
| 7 | IMG_0781   | Resultado final            | 5s (2.5× slow)      |

**Total: ~55 segundos**

## Parámetros técnicos
- Output: 1080×1920, H.264, 24fps
- Slow-motion: 5× (120fps → 24fps)
- Tipografía: Fredoka Medium
- Color: eq brightness+0.03 / contrast 1.1 / saturation 0.85 + vignette
- Audio: rubberband tempo=0.2 (manteniendo pitch)

## Para regenerar
```bash
python3 tools/scripts/build_matcha.py
```
Output: `exports/instagram/iced_matcha_asmr.mp4`
