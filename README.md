# Audio Transcriber

Batch transcribe audio files (MP3, OGG, WAV, M4A) to text using OpenAI's Whisper API with automatic language detection.

Built for non-technical users — a single `RUN.bat` handles everything: setup, configuration, and transcription.

## Features

- Batch transcription of multiple audio files
- Automatic language detection (no config needed)
- Supports MP3, OGG, M4A, WAV, WEBM, MP4
- Single-file Windows script with auto-setup and persistent menu
- API key stored locally in `.env` file

## Quick Start (Windows)

1. Download or clone this repo
2. Double-click `RUN.bat`
   - First run: guides you through Python installation, installs dependencies, and prompts for your OpenAI API key
   - Subsequent runs: goes straight to the menu
3. Place audio files in the `input/` folder
4. Choose **[1] Transcribe files** from the menu
5. Transcriptions appear in `output/` as `.txt` files

## Manual Setup

```bash
pip install openai
```

Set your API key:

```bash
# Windows
set OPENAI_API_KEY=sk-your-key-here

# Mac / Linux
export OPENAI_API_KEY=sk-your-key-here
```

Run:

```bash
python transcribe.py
```

## How It Works

1. Checks for Python, dependencies, and API key (installs/configures as needed)
2. Scans `input/` for audio files
3. Sends each file to OpenAI's Whisper API for transcription (language auto-detected)
4. Saves results as `.txt` files in `output/`
5. Returns to menu for another round or exit

## Cost

Whisper API costs ~$0.006 USD per minute of audio. 10 hours of audio ≈ $3.60 USD.

## Project Structure

```
transcriber/
├── RUN.bat            # Setup + run (Windows)
├── transcribe.py      # Main script
├── .gitignore
├── input/             # Place audio files here
└── output/            # Transcriptions appear here
```

## Requirements

- Python 3.10+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## License

MIT