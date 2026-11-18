#!/usr/bin/env python3
"""
Transcribe un video/audio usando faster-whisper y genera subtítulos SRT.
Uso: python3 transcribe.py <archivo> [idioma: es|en|auto]
"""
import sys
from pathlib import Path
from faster_whisper import WhisperModel

def seconds_to_srt_time(s: float) -> str:
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")

def transcribe(input_path: str, language: str = "auto"):
    path = Path(input_path)
    out_srt = path.with_suffix(".srt")

    print(f"Cargando modelo Whisper (tiny, CPU)...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")

    lang = None if language == "auto" else language
    print(f"Transcribiendo: {path.name}")
    segments, info = model.transcribe(input_path, language=lang, beam_size=5)

    print(f"  Idioma detectado: {info.language} ({info.language_probability:.0%})")

    with open(out_srt, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n")
            f.write(f"{seconds_to_srt_time(seg.start)} --> {seconds_to_srt_time(seg.end)}\n")
            f.write(f"{seg.text.strip()}\n\n")

    print(f"✓ Subtítulos guardados: {out_srt}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    lang = sys.argv[2] if len(sys.argv) > 2 else "auto"
    transcribe(sys.argv[1], lang)
