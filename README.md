# stemdrop

A tiny local web app around [demucs](https://github.com/facebookresearch/demucs). Drop a song, get
**vocals / drums / bass / other** as 24-bit WAVs, plus an optional **beat.wav** (everything but the
vocals). Runs entirely on your machine. Nothing is uploaded anywhere.

![stemdrop](docs/screenshot.jpg)

## Setup

```
git clone https://github.com/carlitoswillis/stemdrop
cd stemdrop
./setup.sh      # makes .venv and installs demucs + flask (torch is big; give it a few minutes)
./run.sh        # opens on http://127.0.0.1:7860
```

Needs Python 3.10 to 3.13 and ffmpeg on PATH (demucs uses it to read mp3 / m4a).
The first split downloads the model weights (about 80 MB) once.

## Options

- **Model.** `htdemucs` is the default and the fastest. `htdemucs_ft` is the fine-tuned version:
  cleaner, about four times slower. `htdemucs_6s` adds guitar and piano stems.
- **Two stems only.** Vocals vs. everything else, in one pass.
- **beat.wav.** Sums drums + bass + other, scaled down only if the sum would clip.

Flags: `./run.sh --port 8000`, `./run.sh --device cpu|cuda`. The default is CPU unless CUDA is
present. Apple's MPS backend is not used because htdemucs crashes on it
(`Output channels > 65536 not supported`).

## Where the files go

`jobs/<id>/out/<model>/<song>/` next to the app. The *open folder* link in the UI opens it in
Finder or your file manager.

## Why

Stem separation in a DAW is either a Live 12.3 feature, a paid website, or a CLI. This is the CLI
with a drop zone, built for mashups: split, listen to each lane, grab the beat.
