"""Загрузка, сохранение и измерение громкости.

Все инструменты работают с массивом формы (каналы, сэмплы) в float32.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

DEFAULT_SR = 44100


def load(path: str | os.PathLike, sr: int = DEFAULT_SR) -> tuple[np.ndarray, int]:
    """Читает любой аудиофайл (wav, mp3, m4a, flac, ogg, даже видео) в стерео float32.

    Декодирует через ffmpeg, чтобы одинаково работать с любыми форматами.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    if shutil.which("ffmpeg") is None:
        audio, file_sr = sf.read(str(path), dtype="float32", always_2d=True)
        audio = audio.T
        if file_sr != sr:
            audio = resample_poly(audio, sr, file_sr, axis=1).astype(np.float32)
    else:
        cmd = [
            "ffmpeg", "-v", "error", "-i", str(path), "-vn",
            "-f", "f32le", "-acodec", "pcm_f32le", "-ac", "2", "-ar", str(sr), "-",
        ]
        raw = subprocess.run(cmd, check=True, capture_output=True).stdout
        audio = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).T.copy()
    if audio.shape[0] == 1:
        audio = np.vstack([audio, audio])
    if audio.shape[1] == 0:
        raise ValueError(f"В файле нет звука: {path}")
    return audio, sr


def save(audio: np.ndarray, sr: int, path: str | os.PathLike, bitrate: str | None = None) -> Path:
    """Сохраняет по расширению: .wav (24 бит), .flac, .mp3 (320k), .m4a/.aac (256k)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower()
    audio = np.clip(audio, -1.0, 1.0)
    if ext in (".wav", ".flac"):
        sf.write(str(path), audio.T, sr, subtype="PCM_24")
        return path
    codecs = {".mp3": ("libmp3lame", bitrate or "320k"), ".m4a": ("aac", bitrate or "256k"),
              ".aac": ("aac", bitrate or "256k")}
    if ext not in codecs:
        raise ValueError(f"Неизвестный формат: {ext}. Используй .wav, .flac, .mp3 или .m4a")
    codec, br = codecs[ext]
    with tempfile.TemporaryDirectory() as tmp:
        tmp_wav = Path(tmp) / "tmp.wav"
        sf.write(str(tmp_wav), audio.T, sr, subtype="PCM_24")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp_wav),
                        "-c:a", codec, "-b:a", br, str(path)], check=True)
    return path


def lufs(audio: np.ndarray, sr: int) -> float:
    """Интегральная громкость по стандарту ITU-R BS.1770 (как у YouTube, Spotify, VK)."""
    meter = pyln.Meter(sr)
    return float(meter.integrated_loudness(audio.T))


def true_peak_db(audio: np.ndarray, sr: int) -> float:
    """Истинный пик в dBTP (с передискретизацией x4)."""
    over = resample_poly(audio, 4, 1, axis=1)
    peak = float(np.max(np.abs(over)))
    return 20 * np.log10(max(peak, 1e-9))


def db_to_gain(db: float) -> float:
    return float(10 ** (db / 20))


def loudness_report(audio: np.ndarray, sr: int) -> dict:
    return {
        "lufs": round(lufs(audio, sr), 2),
        "true_peak_dbtp": round(true_peak_db(audio, sr), 2),
        "duration_sec": round(audio.shape[1] / sr, 3),
    }
