"""stemdrop: a tiny local web UI around demucs.

Drop an audio file, get vocals / drums / bass / other (and a beat = everything but vocals).
Runs entirely on your machine. No accounts, no uploads to anyone.
"""
import argparse, json, os, re, shutil, subprocess, sys, threading, time, uuid
from pathlib import Path

import numpy as np
import soundfile as sf
from flask import Flask, abort, jsonify, request, send_from_directory, send_file

ROOT = Path(__file__).resolve().parent
JOBS = ROOT / "jobs"
JOBS.mkdir(exist_ok=True)
STEMS = ["vocals", "drums", "bass", "other"]


def detect_engine():
    """demucs-mlx (Apple Silicon, no torch) if present, else PyTorch demucs."""
    try:
        import demucs_mlx  # noqa: F401
        return "mlx"
    except Exception:
        pass
    try:
        import demucs  # noqa: F401
        return "torch"
    except Exception:
        return None


ENGINE = detect_engine()
MODELS = {
    "htdemucs": "standard, fastest",
    "htdemucs_ft": "fine-tuned, cleaner, ~4x slower",
    "htdemucs_6s": "6 stems: adds guitar + piano",
}

app = Flask(__name__, static_folder=str(ROOT / "static"), static_url_path="/static")
jobs = {}          # id -> dict(status, progress, log, files, error, name, started)
lock = threading.Lock()


def pick_device(requested):
    if ENGINE == "mlx":
        return "apple gpu (mlx)"
    if requested != "auto":
        return requested
    # Apple's MPS backend fails inside htdemucs ("Output channels > 65536 not supported"),
    # and CUDA is the only GPU path that reliably works. CPU is the safe default.
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


def write_beat(stem_dir: Path):
    """Sum every stem except vocals into beat.wav, scaled down only if it would clip."""
    parts = [p for p in stem_dir.glob("*.wav") if p.stem not in ("vocals", "beat", "no_vocals")]
    if not parts:
        return None
    mix, sr = None, None
    for p in parts:
        x, sr = sf.read(p, dtype="float32", always_2d=True)
        mix = x if mix is None else mix[: len(x)] + x[: len(mix)]
    peak = float(np.max(np.abs(mix))) if len(mix) else 0.0
    if peak > 0.98:
        mix = mix * (0.98 / peak)
    out = stem_dir / "beat.wav"
    sf.write(out, mix, sr, subtype="PCM_24")
    return out


def collapse_to_two_stems(stem_dir: Path):
    """Emulate demucs --two-stems for engines without it: keep vocals.wav, sum the rest into no_vocals.wav."""
    parts = [p for p in stem_dir.glob("*.wav") if p.stem != "vocals"]
    mix, sr = None, None
    for p in parts:
        x, sr = sf.read(p, dtype="float32", always_2d=True)
        mix = x if mix is None else mix[: len(x)] + x[: len(mix)]
    if mix is None:
        return
    peak = float(np.max(np.abs(mix))) if len(mix) else 0.0
    if peak > 0.98:
        mix = mix * (0.98 / peak)
    sf.write(stem_dir / "no_vocals.wav", mix, sr, subtype="PCM_24")
    for p in parts:
        p.unlink()


def run_job(job_id, src: Path, model, two_stems, device, make_beat):
    job = jobs[job_id]
    out_dir = JOBS / job_id / "out"
    if ENGINE == "mlx":
        cmd = [sys.executable, "-m", "demucs_mlx", "-n", model, "-o", str(out_dir), str(src)]
    elif ENGINE == "torch":
        cmd = [sys.executable, "-m", "demucs", "-d", device, "-n", model, "-o", str(out_dir)]
        if two_stems:
            cmd += ["--two-stems", "vocals"]
        cmd.append(str(src))
    else:
        job.update(status="error", error="no separation engine installed: run ./setup.sh")
        return
    job.update(status="running", started=time.time(), log=[" ".join(cmd)])
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, bufsize=1, universal_newlines=True)
        buf = ""
        while True:
            ch = proc.stdout.read(1)
            if ch == "" and proc.poll() is not None:
                break
            if ch in ("\r", "\n"):
                line = buf.strip(); buf = ""
                if not line:
                    continue
                m = re.search(r"(\d+)%\|", line) or re.search(r"(\d+)/(\d+)", line)
                if m and m.group(0).startswith(("100%", "0%")) and ENGINE == "mlx":
                    m = None  # mlx only reports whole tracks; keep the bar indeterminate
                if m:
                    if m.lastindex == 2:
                        done, total = int(m.group(1)), int(m.group(2))
                        job["progress"] = round(100 * done / max(total, 1))
                    else:
                        job["progress"] = int(m.group(1))
                    if job["progress"] > 0:
                        job.pop("note", None)
                elif line.startswith("Downloading"):
                    job["note"] = "downloading model weights (first run only)"
                    job["log"].append(line)
                else:
                    job["log"] = (job["log"] + [line])[-40:]
            else:
                buf += ch
        if proc.returncode != 0:
            raise RuntimeError("demucs exited with code %d\n%s" % (proc.returncode, "\n".join(job["log"][-8:])))
        base = out_dir / model if ENGINE == "torch" else out_dir
        stem_dir = next(p for p in base.glob("*") if p.is_dir())
        if two_stems and ENGINE == "mlx":
            collapse_to_two_stems(stem_dir)
        if make_beat and not two_stems:
            write_beat(stem_dir)
        files = sorted(p.name for p in stem_dir.glob("*.wav"))
        order = {n: i for i, n in enumerate(["vocals", "beat", "no_vocals", "drums", "bass", "other", "guitar", "piano"])}
        files.sort(key=lambda f: order.get(Path(f).stem, 99))
        durations = {}
        for f in files:
            try:
                durations[f] = round(sf.info(stem_dir / f).duration, 1)
            except Exception:  # noqa: BLE001
                pass
        job.update(status="done", progress=100, files=files, durations=durations, stem_dir=str(stem_dir),
                   seconds=round(time.time() - job["started"]))
    except Exception as e:  # noqa: BLE001
        job.update(status="error", error=str(e))


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/info")
def info():
    return jsonify(models=MODELS, device=pick_device(app.config["DEVICE"]), engine=ENGINE)


@app.post("/api/split")
def split():
    f = request.files.get("file")
    if not f or not f.filename:
        abort(400, "no file")
    model = request.form.get("model", "htdemucs")
    if model not in MODELS:
        abort(400, "unknown model")
    two_stems = request.form.get("two_stems") == "1"
    make_beat = request.form.get("beat", "1") == "1"
    job_id = uuid.uuid4().hex[:10]
    d = JOBS / job_id; d.mkdir(parents=True)
    safe = re.sub(r"[^\w.\- ()\[\]]+", "_", f.filename)[:120]
    src = d / safe
    f.save(src)
    jobs[job_id] = dict(id=job_id, name=safe, status="queued", progress=0, log=[], files=[], model=model)
    threading.Thread(target=run_job, args=(job_id, src, model, two_stems, pick_device(app.config["DEVICE"]), make_beat),
                     daemon=True).start()
    return jsonify(id=job_id)


@app.get("/api/jobs")
def job_list():
    return jsonify([{k: v for k, v in j.items() if k != "stem_dir"} for j in jobs.values()])


@app.get("/api/jobs/<job_id>")
def job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        abort(404)
    return jsonify({k: v for k, v in job.items() if k != "stem_dir"})


@app.get("/api/jobs/<job_id>/file/<name>")
def job_file(job_id, name):
    job = jobs.get(job_id)
    if not job or job.get("status") != "done" or name not in job["files"]:
        abort(404)
    return send_from_directory(job["stem_dir"], name, as_attachment=request.args.get("dl") == "1",
                               download_name=f"{Path(job['name']).stem} - {name}")


@app.get("/api/jobs/<job_id>/folder")
def job_folder(job_id):
    job = jobs.get(job_id)
    if not job or job.get("status") != "done":
        abort(404)
    if sys.platform == "darwin":
        subprocess.Popen(["open", job["stem_dir"]])
    elif sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", job["stem_dir"]])
    else:
        os.startfile(job["stem_dir"])  # type: ignore[attr-defined]
    return jsonify(ok=True, path=job["stem_dir"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=7860)
    ap.add_argument("--device", default="auto", help="auto | cpu | cuda | mps")
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    app.config["DEVICE"] = args.device
    print(f"\n  stemdrop  →  http://{args.host}:{args.port}   (engine: {ENGINE}, device: {pick_device(args.device)})\n")
    app.run(host=args.host, port=args.port, debug=False, threaded=True)
