name: Crear clips de video

on:
  push:
    paths:
      - 'videos/**'

jobs:
  procesar:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Instalar FFmpeg
        run: sudo apt-get install ffmpeg

      - name: Instalar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Ejecutar script
        run: python scripts/auto_clips.py

      - name: Subir clips
        uses: actions/upload-artifact@v4
        with:
          name: clips
          path: output/
