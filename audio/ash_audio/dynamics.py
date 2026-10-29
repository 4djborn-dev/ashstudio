"""Нормализация громкости с лимитером, фейды."""
from __future__ import annotations

import numpy as np
from pedalboard import Limiter, Pedalboard

from .io import db_to_gain, lufs, true_peak_db


def normalize(audio: np.ndarray, sr: int, target_lufs: float = -14.0,
              ceiling_dbtp: float = -1.0, max_iter: int = 4) -> np.ndarray:
    """Доводит трек до целевой громкости и не даёт пикам выйти за потолок.

    Сначала поднимает или опускает громкость, затем лимитер срезает пики,
    и цикл повторяется, пока громкость и пик не попадут в цель.
    """
    out = audio.astype(np.float32)
    for _ in range(max_iter):
        current = lufs(out, sr)
        if not np.isfinite(current):
            return out  # тишина
        out = out * db_to_gain(target_lufs - current)
        if true_peak_db(out, sr) > ceiling_dbtp:
            # порог ниже потолка, чтобы оставить запас на межсэмпловые пики
            board = Pedalboard([Limiter(threshold_db=ceiling_dbtp - 0.5, release_ms=80)])
            out = board(out, sr)
        if abs(lufs(out, sr) - target_lufs) < 0.3 and true_peak_db(out, sr) <= ceiling_dbtp + 0.05:
            break
    tp = true_peak_db(out, sr)
    if tp > ceiling_dbtp:  # финальная страховка: чуть тише, но без перегруза
        out = out * db_to_gain(ceiling_dbtp - tp)
    return out


def fade(audio: np.ndarray, sr: int, fade_in: float = 0.0, fade_out: float = 0.0) -> np.ndarray:
    """Плавное появление и затухание (кривая равной мощности)."""
    out = audio.copy()
    n = out.shape[1]
    if fade_in > 0:
        k = min(int(fade_in * sr), n)
        out[:, :k] *= np.sin(np.linspace(0, np.pi / 2, k)) ** 2
    if fade_out > 0:
        k = min(int(fade_out * sr), n)
        out[:, n - k:] *= np.cos(np.linspace(0, np.pi / 2, k)) ** 2
    return out
