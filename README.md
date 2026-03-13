# Audio Transcriber

Batch transcribe audio files (MP3, OGG, WAV, M4A) to text using OpenAI's Whisper API, with optional noise reduction powered by `noisereduce`.

Built for non-technical users — includes one-click setup and run scripts for Windows.

## Features

- Batch transcription of multiple audio files
- Interactive noise reduction (all files, none, or choose per file)
- Supports MP3, OGG, M4A, WAV, WEBM, MP4
- Simple Windows `.bat` scripts for setup and execution
- API key stored locally in `.env` file

## Quick Start (Windows)

1. Install [Python](https://www.python.org/downloads/) — check **"Add Python to PATH"** during installation
2. Download or clone this repo
3. Double-click `SETUP.bat` — installs dependencies and prompts for your OpenAI API key
4. Place audio files in the `input/` folder
5. Double-click `TRANSCRIBIR.bat`
6. Transcriptions appear in `output/` as `.txt` files

## Manual Setup

```bash
pip install openai noisereduce imageio-ffmpeg soundfile numpy
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

1. Scans `input/` for audio files
2. Asks whether to apply noise reduction (uses `noisereduce` + `imageio-ffmpeg` for format conversion)
3. Sends each file to OpenAI's Whisper API for transcription
4. Saves results as `.txt` files in `output/`

## Configuration

Edit these variables at the top of `transcribe.py`:

| Variable | Default | Description |
|---|---|---|
| `LANGUAGE` | `"es"` | Transcription language (`"es"`, `"en"`, etc.) |
| `MAX_FILE_SIZE_MB` | `25` | Max file size (Whisper API limit) |

## Cost

Whisper API costs ~$0.006 USD per minute of audio. 10 hours of audio ≈ $3.60 USD.

## Project Structure

```
transcriber/
├── SETUP.bat          # One-time setup (Windows)
├── TRANSCRIBIR.bat    # Run transcription (Windows)
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
