#!/usr/bin/env python3
"""Extract representative JPEG frames and metadata from a local video."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run_json(command: list[str]) -> dict:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--frames", type=int, default=12)
    args = parser.parse_args()

    if not args.video.is_file():
        raise SystemExit(f"Vídeo não encontrado: {args.video}")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg e ffprobe são necessários para extrair quadros.")
    args.output.mkdir(parents=True, exist_ok=True)

    probe = run_json([
        "ffprobe", "-v", "error", "-show_format", "-show_streams",
        "-of", "json", str(args.video),
    ])
    duration = float(probe.get("format", {}).get("duration") or 0)
    frame_count = max(1, min(args.frames, 24))
    if duration > 0:
        timestamps = [duration * index / frame_count for index in range(frame_count)]
    else:
        timestamps = [0.0]

    frames = []
    for index, timestamp in enumerate(timestamps):
        target = args.output / f"frame-{index + 1:02d}-{timestamp:.2f}s.jpg"
        subprocess.run([
            "ffmpeg", "-v", "error", "-ss", f"{timestamp:.3f}", "-i", str(args.video),
            "-frames:v", "1", "-q:v", "2", "-y", str(target),
        ], check=True)
        if target.is_file():
            frames.append({"index": index + 1, "timestampSeconds": round(timestamp, 3), "path": str(target.resolve())})

    streams = probe.get("streams", [])
    manifest = {
        "protocol": "plateia-video-sampling/1.0",
        "source": str(args.video.resolve()),
        "durationSeconds": duration,
        "hasAudio": any(stream.get("codec_type") == "audio" for stream in streams),
        "hasVideo": any(stream.get("codec_type") == "video" for stream in streams),
        "samplingIsRepresentativeNotExhaustive": True,
        "frames": frames,
    }
    manifest_path = args.output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
