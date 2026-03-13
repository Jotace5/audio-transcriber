"""
Transcriptor de audio a texto usando Whisper API (OpenAI)
=========================================================
Uso:
  1. Poné tus archivos MP3 en la carpeta "input/"
  2. Ejecutá: python transcribe.py
  3. Los textos transcriptos van a aparecer en "output/"

Requisitos:
  pip install openai noisereduce imageio-ffmpeg soundfile numpy
"""

import os
import sys
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
import noisereduce as nr
import imageio_ffmpeg
from openai import OpenAI

# --- Configuración ---
LANGUAGE = "es"  # Cambiar a "en" para inglés
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
CLEANED_DIR = Path("cleaned")
MAX_FILE_SIZE_MB = 25
FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()


def setup_dirs():
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    CLEANED_DIR.mkdir(exist_ok=True)


def get_audio_files():
    extensions = {".mp3", ".mp4", ".m4a", ".wav", ".webm", ".ogg"}
    files = [f for f in INPUT_DIR.iterdir() if f.suffix.lower() in extensions]
    return sorted(files)


def ask_noise_reduction(files):
    """
    Pregunta al usuario cómo quiere manejar la reducción de ruido.
    Retorna un dict {filename: True/False} por cada archivo.
    """
    print("🔇 ¿Querés aplicar reducción de ruido a los audios?")
    print()
    print("  [1] Sí, a todos los archivos")
    print("  [2] No, a ninguno")
    print("  [3] Dejame elegir archivo por archivo")
    print()

    while True:
        choice = input("Elegí una opción (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            break
        print("  Opción no válida. Ingresá 1, 2 o 3.")

    if choice == "1":
        return {f.name: True for f in files}

    if choice == "2":
        return {f.name: False for f in files}

    # Opción 3: elegir por archivo
    print()
    result = {}
    for f in files:
        while True:
            ans = input(f"  ¿Reducir ruido en '{f.name}'? (s/n): ").strip().lower()
            if ans in ("s", "n", "si", "no", "sí"):
                result[f.name] = ans in ("s", "si", "sí")
                break
            print("    Ingresá 's' o 'n'.")
    return result


def audio_to_wav(filepath):
    """
    Convierte cualquier formato de audio a WAV mono 16kHz usando ffmpeg.
    Retorna el path al WAV temporal.
    """
    tmp_wav = CLEANED_DIR / f"{filepath.stem}_tmp.wav"
    subprocess.run(
        [FFMPEG_PATH, "-y", "-i", str(filepath), "-ar", "16000", "-ac", "1", str(tmp_wav)],
        capture_output=True,
    )
    return tmp_wav


def reduce_noise(filepath):
    """
    Aplica reducción de ruido.
    Retorna el path al archivo limpio.
    """
    cleaned_path = CLEANED_DIR / f"{filepath.stem}_clean.wav"

    # Convertir a WAV primero (funciona con cualquier formato)
    tmp_wav = audio_to_wav(filepath)

    # Leer WAV con soundfile
    data, sample_rate = sf.read(tmp_wav)
    tmp_wav.unlink()  # Borrar temporal

    # Convertir a mono si es estéreo
    if data.ndim > 1:
        data = np.mean(data, axis=1)

    # Aplicar reducción de ruido
    cleaned = nr.reduce_noise(y=data, sr=sample_rate)

    # Guardar como WAV
    sf.write(str(cleaned_path), cleaned, sample_rate)
    return cleaned_path


def transcribe_file(client, filepath):
    file_size_mb = filepath.stat().st_size / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        print(f"  ⚠️  Archivo muy grande ({file_size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB). Saltando...")
        return None

    with open(filepath, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=LANGUAGE,
        )
    return result.text


def main():
    # Verificar API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ Falta la API key. Configurala así:")
        print()
        print("  Windows:  set OPENAI_API_KEY=sk-tu-key-aqui")
        print("  Mac/Linux: export OPENAI_API_KEY=sk-tu-key-aqui")
        print()
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    setup_dirs()

    # Buscar archivos
    files = get_audio_files()
    if not files:
        print(f"📂 No se encontraron archivos de audio en '{INPUT_DIR}/'")
        print(f"   Poné tus MP3 ahí y volvé a ejecutar.")
        sys.exit(0)

    print(f"🎙️  Encontrados {len(files)} archivo(s) para transcribir\n")

    # Preguntar sobre reducción de ruido
    noise_choices = ask_noise_reduction(files)
    print()

    ok = 0
    errors = 0
    cleaned_files = []

    for i, filepath in enumerate(files, 1):
        filename = filepath.name
        output_path = OUTPUT_DIR / f"{filepath.stem}.txt"
        use_nr = noise_choices.get(filename, False)

        label = "🔇+🎙️" if use_nr else "🎙️"
        print(f"[{i}/{len(files)}] {label} {filename}...", end=" ", flush=True)

        try:
            # Paso 1: reducir ruido si el usuario lo pidió
            file_to_transcribe = filepath
            if use_nr:
                print("limpiando ruido...", end=" ", flush=True)
                file_to_transcribe = reduce_noise(filepath)
                cleaned_files.append(file_to_transcribe)

            # Paso 2: transcribir
            print("transcribiendo...", end=" ", flush=True)
            text = transcribe_file(client, file_to_transcribe)

            if text is None:
                errors += 1
                continue

            output_path.write_text(text, encoding="utf-8")
            print(f"✅ → {output_path.name}")
            ok += 1

        except Exception as e:
            print(f"❌ Error: {e}")
            errors += 1

    # Limpiar archivos temporales
    for f in cleaned_files:
        try:
            f.unlink()
        except OSError:
            pass

    print(f"\n{'='*40}")
    print(f"✅ Transcriptos: {ok}")
    if errors:
        print(f"❌ Errores: {errors}")
    print(f"📁 Resultados en: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()