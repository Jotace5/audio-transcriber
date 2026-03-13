"""
Audio to Text Transcriber using Whisper API (OpenAI)
=========================================================
Usage:
  1. Put your MP3 files in the "input/" folder
  2. Run: python transcribe.py
  3. The transcribed texts will appear in "output/"

Requirements:
  pip install openai
"""

import os
import sys
from pathlib import Path
from openai import OpenAI

# --- Configuration ---
# LANGUAGE = "es"  # Change to "en" for English # Uncomment if you want to force a language
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
MAX_FILE_SIZE_MB = 25


def setup_dirs():
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)


def get_audio_files():
    extensions = {".mp3", ".mp4", ".m4a", ".wav", ".webm", ".ogg"}
    files = [f for f in INPUT_DIR.iterdir() if f.suffix.lower() in extensions]
    return sorted(files)


def transcribe_file(client, filepath):
    file_size_mb = filepath.stat().st_size / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        print(f"  File too large ({file_size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB). Skipping...")
        return None

    with open(filepath, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=LANGUAGE,
        )
    return result.text


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Missing API key. Configure it like this:")
        print()
        print("  Windows:  set OPENAI_API_KEY=sk-your-key-here")
        print("  Mac/Linux: export OPENAI_API_KEY=sk-your-key-here")
        print()
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    setup_dirs()

    files = get_audio_files()
    if not files:
        print(f"No audio files found in '{INPUT_DIR}/'")
        print(f"Put your MP3s there and run again.")
        sys.exit(0)

    print(f"Found {len(files)} file(s) to transcribe")
    print()

    ok = 0
    errors = 0

    for i, filepath in enumerate(files, 1):
        filename = filepath.name
        output_path = OUTPUT_DIR / f"{filepath.stem}.txt"

        print(f"[{i}/{len(files)}] {filename}...", end=" ", flush=True)

        try:
            text = transcribe_file(client, filepath)

            if text is None:
                errors += 1
                continue

            output_path.write_text(text, encoding="utf-8")
            print(f"OK -> {output_path.name}")
            ok += 1

        except Exception as e:
            print(f"Error: {e}")
            errors += 1

    print()
    print("=" * 40)
    print(f"Transcribed: {ok}")
    if errors:
        print(f"Errors: {errors}")
    print(f"Results in: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()