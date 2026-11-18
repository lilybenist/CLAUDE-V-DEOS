#!/usr/bin/env python3
"""
ASMR Iced Matcha - Editor automatico con FFmpeg
Genera: exports/instagram/iced_matcha_asmr.mp4
"""
import subprocess, sys, json
from pathlib import Path

SCRATCH = Path("/tmp/claude-0/-home-user/f7a0dab6-70af-53ce-af07-b35648fb4128/scratchpad")
CONTENT = Path("/home/user/CLAUDE-V-DEOS/originals/footage/MATCHATOPÍA/CONTENIDO")
OUT_DIR = Path("/home/user/CLAUDE-V-DEOS/exports/instagram")
FONT = str(SCRATCH / "fonts/Fredoka-Medium.ttf")
TMP = SCRATCH / "edit_tmp"
TMP.mkdir(exist_ok=True)

W, H = 1080, 1920
FPS = 24

# ── Color grade ───────────────────────────────────────────────────────────────
GRADE = (
    "eq=brightness=0.03:contrast=1.1:saturation=0.85,"
    "vignette=angle=PI/4:mode=forward:eval=init"
)

# ── Scale filter: 4K portrait (auto-rotated) → 1080x1920 ─────────────────────
SCALE = (
    f"scale={W}:{H}:flags=lanczos"
    f":force_original_aspect_ratio=decrease,"
    f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black"
)


def run(cmd: str, label: str = "") -> bool:
    if label:
        print(f"  → {label}...", end=" ", flush=True)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    ok = r.returncode == 0
    if label:
        print("ok" if ok else "FAIL")
    if not ok:
        # Print last 600 chars of stderr for debugging
        print(f"    ERR: {r.stderr[-600:]}")
    return ok


def txt(text: str, y: int = None, fs: int = 70) -> str:
    """drawtext filter fragment"""
    if y is None:
        y = int(H * 0.74)
    # Escape special chars for FFmpeg drawtext
    text = text.replace("'", "\\'").replace(":", "\\:")
    return (
        f"drawtext=text='{text}':"
        f"fontfile={FONT}:fontcolor=white:fontsize={fs}:"
        f"x=(w-text_w)/2:y={y}:"
        f"shadowcolor=black@0.6:shadowx=2:shadowy=2"
    )


def process_clip(src: Path, out: Path, start: float, dur: float,
                 label: str, slow: float = 5.0, text_y: int = None) -> bool:
    """
    Trim → slow-motion → scale → grade → text overlay → fade in/out
    Returns duration of output clip in seconds.
    """
    out_dur = dur * slow
    fade_d = 0.35

    # Text appears at 0.6s and fades 0.6s before clip end
    t_in = 0.6
    t_out = max(out_dur - 0.8, t_in + 0.5)

    vf_parts = [
        f"trim=start={start}:duration={dur}",
        f"setpts=PTS-STARTPTS",
        f"setpts={slow:.2f}*PTS",
        SCALE,
        GRADE,
        txt(label, text_y),
        f"fade=t=in:st=0:d={fade_d}",
        f"fade=t=out:st={out_dur - fade_d}:d={fade_d}",
    ]
    vf = ",".join(vf_parts)

    # Audio: rubberband stretches audio to match video slow-down
    tempo = round(1.0 / slow, 4)
    af = (
        f"atrim=start={start}:duration={dur},"
        f"asetpts=N/SR/TB,"
        f"rubberband=tempo={tempo}"
    )

    cmd = (
        f'ffmpeg -y -i "{src}" '
        f'-filter_complex "[0:v]{vf}[vout];[0:a]{af}[aout]" '
        f'-map "[vout]" -map "[aout]" '
        f'-c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -r {FPS} '
        f'-c:a aac -b:a 128k -ar 48000 '
        f'"{out}"'
    )
    return run(cmd, f"clip {out.name}")


def make_title(out: Path, duration: float = 2.5) -> bool:
    """Black card with 'iced matcha' + 'asmr' in Fredoka"""
    t1 = txt("iced matcha", y=int(H * 0.44), fs=128)
    t2 = txt("asmr", y=int(H * 0.56), fs=52)
    fd = 0.4

    vf = (
        f"color=c=black:s={W}x{H}:r={FPS}:d={duration}[bg];"
        f"[bg]{t1},{t2},"
        f"fade=t=in:st=0:d={fd},"
        f"fade=t=out:st={duration - fd}:d={fd}[vout]"
    )

    cmd = (
        f'ffmpeg -y '
        f'-f lavfi -i "anullsrc=r=48000:cl=stereo:d={duration}" '
        f'-filter_complex "{vf}" '
        f'-map "[vout]" -map 0:a '
        f'-c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -r {FPS} '
        f'-c:a aac -b:a 128k -ar 48000 '
        f'"{out}"'
    )
    return run(cmd, "title card")


def concat_clips(clip_paths: list, out: Path) -> bool:
    """Write concat file and join all clips"""
    concat_file = TMP / "concat.txt"
    with open(concat_file, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")

    cmd = (
        f'ffmpeg -y -f concat -safe 0 -i "{concat_file}" '
        f'-c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p '
        f'-c:a aac -b:a 192k -ar 48000 '
        f'-movflags +faststart '
        f'"{out}"'
    )
    return run(cmd, "final concat")


# ── Edit sequence ─────────────────────────────────────────────────────────────
# (src_file, start_sec, duration_sec, text_label, slow_factor)
SEQUENCE = [
    # 0  Title card: generated separately
    # 1  Sifting matcha (IMG_0772) — top-down, beautiful powder
    ("IMG_0772.MOV", 2.0,  1.5,  "tamiza el matcha",          5.0),
    # 2  Kettle (IMG_0770) — gooseneck kettle
    ("IMG_0770.MOV", 3.5,  1.2,  "agua caliente, 70 C",       5.0),
    # 3  Whisking start (IMG_0774)
    ("IMG_0774.MOV", 2.5,  2.0,  "bate con el chasen",        5.0),
    # 4  Frothy whisking (IMG_0776)
    ("IMG_0776.MOV", 2.0,  1.5,  "hasta que espume",          5.0),
    # 5  Milk over ice (IMG_0779)
    ("IMG_0779.MOV", 1.0,  1.3,  "leche fria sobre hielo",    5.0),
    # 6  Pouring matcha (IMG_0780) — money shot
    ("IMG_0780.MOV", 2.0,  2.0,  "vierte el matcha",          5.0),
    # 7  Final glass (IMG_0781) — reveal at gentle slow
    ("IMG_0781.MOV", 1.0,  2.0,  "y disfruta",                2.5),
]


def main():
    print("== ASMR Iced Matcha Builder ==")
    clips = []

    # Title card
    title_out = TMP / "00_title.mp4"
    if not make_title(title_out, duration=2.5):
        print("Title card FAILED"); sys.exit(1)
    clips.append(title_out)

    # Process each clip
    for i, (fname, start, dur, label, slow) in enumerate(SEQUENCE, 1):
        src = CONTENT / fname
        out = TMP / f"{i:02d}_{fname.replace('.MOV', '')}.mp4"
        if not process_clip(src, out, start, dur, label, slow):
            print(f"Clip {fname} FAILED"); sys.exit(1)
        clips.append(out)

    # Final concat
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    final_out = OUT_DIR / "iced_matcha_asmr.mp4"
    if not concat_clips(clips, final_out):
        print("Concat FAILED"); sys.exit(1)

    # Report
    info = subprocess.run(
        f'ffprobe -v quiet -show_format "{final_out}"',
        shell=True, capture_output=True, text=True
    ).stdout
    dur_line = [l for l in info.split('\n') if 'duration' in l]
    size_line = [l for l in info.split('\n') if 'size' in l]
    print(f"\n✓ Listo: {final_out}")
    for l in dur_line + size_line:
        print(f"  {l.strip()}")


if __name__ == "__main__":
    main()
