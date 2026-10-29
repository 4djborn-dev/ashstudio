"""Анализ трека: темп, доли, такты, тональность, энергия, лучшие отрезки для сниппетов."""
from __future__ import annotations

import librosa
import numpy as np

KEY_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
# Профили Крумхансла — Кесслер
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
ANALYSIS_SR = 22050


def _mono(audio: np.ndarray, sr: int) -> np.ndarray:
    y = audio.mean(axis=0)
    if sr != ANALYSIS_SR:
        y = librosa.resample(y, orig_sr=sr, target_sr=ANALYSIS_SR)
    return y.astype(np.float32)


def estimate_key(y: np.ndarray) -> dict:
    chroma = librosa.feature.chroma_cqt(y=y, sr=ANALYSIS_SR).mean(axis=1)
    best = None
    for i in range(12):
        for mode, profile in (("major", MAJOR_PROFILE), ("minor", MINOR_PROFILE)):
            r = float(np.corrcoef(np.roll(profile, i), chroma)[0, 1])
            if best is None or r > best[0]:
                best = (r, i, mode)
    r, i, mode = best
    name = KEY_NAMES[i] + ("m" if mode == "minor" else "")
    # параллельная тональность: тот же набор нот (C ↔ Am), автоматика их часто путает
    rel = KEY_NAMES[(i + 9) % 12] + "m" if mode == "major" else KEY_NAMES[(i + 3) % 12]
    return {"key": name, "relative": rel, "tonic": KEY_NAMES[i], "mode": mode,
            "confidence": round(r, 3)}


def _bar_phase(beat_frames: np.ndarray, chroma: np.ndarray, low_env: np.ndarray,
               beats_per_bar: int = 4) -> int:
    """Какая доля — первая в такте.

    Аккорды обычно меняются на первой доле, и там же чаще всего бочка с басом.
    Атаку (громкость удара) не учитываем: снейр на 2 и 4 сбивает с толку.
    """
    idx = beat_frames[beat_frames < chroma.shape[1]]
    # хрома по долям: столбец 0 — до первой доли, столбец i+1 — от доли i до следующей
    sync = librosa.util.sync(chroma, idx, aggregate=np.median)
    sync = sync / (np.linalg.norm(sync, axis=0, keepdims=True) + 1e-9)
    change = 1 - np.sum(sync[:, 1:] * sync[:, :-1], axis=0)  # смена гармонии на доле i
    change = change[: len(idx)]
    change = change / (change.max() + 1e-9)
    low = low_env[np.minimum(idx, len(low_env) - 1)]
    scores = []
    for phase in range(beats_per_bar):
        sel = np.arange(phase, len(idx), beats_per_bar)
        sel = sel[sel < len(change)]
        scores.append(float(2 * change[sel].mean() + low[sel].mean()) if len(sel) else -1)
    return int(np.argmax(scores))


def estimate_tempo(onset_env: np.ndarray, hop: int, lo: float = 75, hi: float = 165) -> float:
    """Темп по темпограмме: самый сильный период, приведённый к диапазону lo–hi.

    Типичные ошибки автоматики — темп вдвое меньше или больше настоящего,
    поэтому результат складывается по октавам в «нормальный» диапазон.
    Для медленных баллад (< 75) или быстрого DnB (> 165) лучше задать --bpm вручную.
    """
    tg = librosa.feature.tempogram(onset_envelope=onset_env, sr=ANALYSIS_SR, hop_length=hop)
    ac = tg.mean(axis=1)
    freqs = librosa.tempo_frequencies(tg.shape[0], sr=ANALYSIS_SR, hop_length=hop)
    valid = (freqs >= 40) & (freqs <= 260)
    bpm = float(freqs[valid][np.argmax(ac[valid])])
    while bpm < lo:
        bpm *= 2
    while bpm >= hi:
        bpm /= 2
    return bpm


def analyze(audio: np.ndarray, sr: int, beats_per_bar: int = 4, bpm: float | None = None) -> dict:
    y = _mono(audio, sr)
    hop = 512
    duration = len(y) / ANALYSIS_SR

    onset_env = librosa.onset.onset_strength(y=y, sr=ANALYSIS_SR, hop_length=hop)
    guess = bpm or estimate_tempo(onset_env, hop)
    _, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=ANALYSIS_SR,
                                             hop_length=hop, units="frames", bpm=guess,
                                             tightness=400)
    tempo = float(guess)
    if not bpm and len(beat_frames) >= 16:
        # уточнение: темпограмма грубая (шаг ~1 BPM), а ошибка в 1 BPM за минуту
        # сдвигает сетку на полдоли. Берём наклон прямой через найденные доли.
        times = librosa.frames_to_time(beat_frames, sr=ANALYSIS_SR, hop_length=hop)
        period = float(np.polyfit(np.arange(len(times)), times, 1)[0])
        refined = 60.0 / period
        if abs(refined - guess) / guess < 0.04:
            tempo = refined
            _, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=ANALYSIS_SR,
                                                     hop_length=hop, units="frames", bpm=tempo,
                                                     tightness=400)
            times = librosa.frames_to_time(beat_frames, sr=ANALYSIS_SR, hop_length=hop)
            tempo = 60.0 / float(np.polyfit(np.arange(len(times)), times, 1)[0])
    beat_times = librosa.frames_to_time(beat_frames, sr=ANALYSIS_SR, hop_length=hop)

    # энергия низов (бочка, бас) — для поиска первой доли такта
    spec = np.abs(librosa.stft(y, hop_length=hop))
    freqs = librosa.fft_frequencies(sr=ANALYSIS_SR)
    low_env = spec[freqs < 150].mean(axis=0)
    low_env = low_env / (low_env.max() + 1e-9)
    onset_n = onset_env / (onset_env.max() + 1e-9)

    chroma = librosa.feature.chroma_cqt(y=y, sr=ANALYSIS_SR, hop_length=hop)
    phase = _bar_phase(beat_frames, chroma, low_env, beats_per_bar) if len(beat_frames) >= 8 else 0
    bar_times = beat_times[phase::beats_per_bar]

    # энергия по секундам (для графика и монтажа)
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    rms_t = librosa.frames_to_time(np.arange(len(rms)), sr=ANALYSIS_SR, hop_length=hop)
    seconds = np.arange(0, int(np.ceil(duration)))
    energy = [float(rms[(rms_t >= s) & (rms_t < s + 1)].mean()) if np.any((rms_t >= s) & (rms_t < s + 1)) else 0.0
              for s in seconds]
    emax = max(energy) or 1.0
    energy = [round(e / emax, 3) for e in energy]

    # сильные акценты (удары, вступления) — точки для склеек видео
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=ANALYSIS_SR,
                                              hop_length=hop, backtrack=False)
    strengths = onset_n[onset_frames]
    strong = onset_frames[strengths >= np.quantile(strengths, 0.85)] if len(strengths) else onset_frames
    accents = librosa.frames_to_time(strong, sr=ANALYSIS_SR, hop_length=hop)

    return {
        "duration_sec": round(duration, 3),
        "bpm": round(tempo, 2),
        "beats_per_bar": beats_per_bar,
        "key": estimate_key(y),
        "beats": [round(float(t), 3) for t in beat_times],
        "bars": [round(float(t), 3) for t in bar_times],
        "accents": [round(float(t), 3) for t in accents],
        "energy_per_second": energy,
        "_internal": {"y": y, "hop": hop, "rms": rms, "rms_t": rms_t},
    }


def best_segments(analysis: dict, length: float, top: int = 3, min_gap: float | None = None) -> list[dict]:
    """Ищет лучшие отрезки нужной длины для сниппета (обычно припев).

    Оценка = громкость/плотность отрезка + насколько этот материал повторяется в треке
    (припев звучит несколько раз). Начало всегда на первой доле такта.
    """
    y = analysis["_internal"]["y"]
    hop = analysis["_internal"]["hop"]
    duration = analysis["duration_sec"]
    bars = [b for b in analysis["bars"] if b + length <= duration + 0.05]
    if not bars:
        return [{"start": 0.0, "end": round(min(length, duration), 3), "score": 0.0}]

    chroma = librosa.feature.chroma_cqt(y=y, sr=ANALYSIS_SR, hop_length=hop)
    rms = analysis["_internal"]["rms"]
    rms_t = analysis["_internal"]["rms_t"]
    t = librosa.frames_to_time(np.arange(chroma.shape[1]), sr=ANALYSIS_SR, hop_length=hop)

    def window(times, a, b):
        m = (times >= a) & (times < b)
        return m if m.any() else (times >= a)

    # профиль каждого кандидата: гармония (для поиска повторов) и громкость
    feats, loud = [], []
    for b in bars:
        v = chroma[:, window(t, b, b + length)].mean(axis=1)
        feats.append(v / (np.linalg.norm(v) + 1e-9))
        loud.append(float(rms[window(rms_t, b, b + length)].mean()))
    feats = np.array(feats)
    loud = np.array(loud)
    sim = feats @ feats.T
    rep = []
    for i, b in enumerate(bars):
        far = np.array([abs(b - o) >= length for o in bars])  # сравниваем только с другими частями
        rep.append(float(np.sort(sim[i][far])[-2:].mean()) if far.sum() >= 2 else 0.0)
    rep = np.array(rep)

    def z(x):
        return (x - x.mean()) / (x.std() + 1e-9)

    score = 0.6 * z(loud) + 0.4 * z(rep)
    # штраф за самое начало и самый конец (интро и аутро)
    for i, b in enumerate(bars):
        if b < 5 or b + length > duration - 3:
            score[i] -= 0.5

    gap = min_gap if min_gap is not None else length * 0.75
    picked = []
    for i in np.argsort(score)[::-1]:
        if all(abs(bars[i] - p["start"]) >= gap for p in picked):
            picked.append({"start": round(bars[i], 3), "end": round(bars[i] + length, 3),
                           "score": round(float(score[i]), 3)})
        if len(picked) >= top:
            break
    return picked


def snap_to_bar(time: float, bars: list[float]) -> float:
    if not bars:
        return time
    return float(min(bars, key=lambda b: abs(b - time)))


def public(analysis: dict) -> dict:
    """Результат без внутренних массивов — для сохранения в JSON."""
    return {k: v for k, v in analysis.items() if not k.startswith("_")}
