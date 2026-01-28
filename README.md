# VideoCanvas
A project to convert videos to MIDI files which can be read by Roland Sound Canvas.

## Features
- Convert video files to Roland Sound Canvas-compatible MIDI format (Now with SC-8850 support)
- Frame skipping support to avoid MIDI jam
- A simple command-line interface

## Prerequisites
- uv package manager
- A Roland Sound Canvas compatible device for playback

## Installation
1. Clone this repository to your local machine.
2. Run `uv sync` to install dependencies.
3. Use `uv run main.py` to run the program.

## Usage
Check `uv run main.py -h`.

## Tips
When enabling SC-8850 support, using the frame-skipping feature is recommended to avoid MIDI jam. 

## License
This project is licensed under GPL-3.0.
