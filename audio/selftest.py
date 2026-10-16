#!/usr/bin/env python3
"""Самопроверка набора: синтезирует тестовый трек с известной структурой
(интро — куплет — припев — куплет — припев — аутро, 120 BPM, ля минор)
и прогоняет на нём все инструменты.

    python selftest.py            # быстрые проверки
    python selftest.py --full     # плюс стемы (Demucs), мастеринг по референсу и аудио→MIDI
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pretty_midi as pm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ash_audio.io import load, loudness_report, save  # noqa: E402
from midi_gen import build  # noqa: E402

SR = 44100
BPM = 120.0
BAR = 60 / BPM * 4


def drum_hit(kind: str, sr: int = SR) -> np.ndarray:
    rng = np.random.default_rng(1)
    if kind == "kick":
        t = np.arange(int(0.35 * sr)) / sr
        f = 50 + 120 * np.exp(-t * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 9)
    if kind in ("snare", "clap"):
        t = np.arange(int(0.2 * sr)) / sr
        return (rng.standard_normal(len(t)) * 0.7 + np.sin(2 * np.pi * 190 * t) * 0.5) * np.exp(-t * 22)
    t = np.arange(int(0.05 * sr)) / sr
    noise = rng.standard_normal(len(t))
    return np.diff(noise, prepend=0) * np.exp(-t * 80) * 0.4


def render(midi: pm.PrettyMIDI, gain: dict) -> np.ndarray:
    length = int((midi.get_end_time() + 1) * SR)
    out = np.zeros(length)
    kinds = {36: "kick", 38: "snare", 39: "clap", 42: "hat", 46: "hat"}
    for inst in midi.instruments:
        g = gain.get(inst.name, 0)
        if g == 0:
            continue
        if inst.is_drum:
            for n in inst.notes:
                hit = drum_hit(kinds.get(n.pitch, "hat")) * n.velocity / 127 * g
                a = int(n.start * SR)
                out[a:a + len(hit)] += hit[: max(0, length - a)]
        else:
            for n in inst.notes:
                a, b = int(n.start * SR), int(n.end * SR)
                t = np.arange(b - a) / SR
                f = pm.note_number_to_hz(n.pitch)
                env = np.minimum(1, t / 0.01) * np.exp(-t * 2)
                wave = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
                out[a:b] += wave * env * n.velocity / 127 * g
    return out


def make_track(path: Path) -> list[tuple[str, float, float]]:
    sections = [("intro", "Am F C G", 4, {"Chords": .25}),
                ("verse", "Am F C G", 8, {"Chords": .2, "Bass": .3, "Drums": .25}),
                ("chorus", "F G Em Am", 8, {"Chords": .35, "Bass": .5, "Drums": .6, "Arp": .25}),
                ("verse", "Am F C G", 8, {"Chords": .2, "Bass": .3, "Drums": .25}),
                ("chorus", "F G Em Am", 8, {"Chords": .35, "Bass": .5, "Drums": .6, "Arp": .25}),
                ("outro", "Am F C G", 4, {"Chords": .2})]
    parts, layout, t = [], [], 0.0
    for name, chords, bars, gain in sections:
        audio = render(build(chords.split(), BPM, "pop", bars, 1), gain)[: int(bars * BAR * SR)]
        parts.append(audio)
        layout.append((name, round(t, 2), round(t + bars * BAR, 2)))
        t += bars * BAR
    mono = np.concatenate(parts)
    mono = mono / np.max(np.abs(mono)) * 0.5
    save(np.vstack([mono, mono]).astype(np.float32), SR, path)
    return layout


def run(*cmd: str) -> str:
    r = subprocess.run([sys.executable, *cmd], capture_output=True, text=True, cwd=HERE)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        raise SystemExit(f"✗ Ошибка: {' '.join(cmd)}")
    return r.stdout


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--full", action="store_true")
    p.add_argument("--keep", help="папка, куда сохранить результаты проверки")
    args = p.parse_args()

    tmp = Path(args.keep) if args.keep else Path(tempfile.mkdtemp())
    tmp.mkdir(parents=True, exist_ok=True)
    track = tmp / "test_track.wav"
    layout = make_track(track)
    print("Тестовый трек:", ", ".join(f"{n} {a}–{b}" for n, a, b in layout))
    choruses = [(a, b) for n, a, b in layout if n == "chorus"]

    # 1. анализ
    print(run("analyze.py", str(track), "--lengths", "15,30"))
    res = json.loads(track.with_suffix(".analysis.json").read_text(encoding="utf-8"))
    assert abs(res["bpm"] - BPM) < 2 or abs(res["bpm"] - BPM * 2) < 4 or abs(res["bpm"] - BPM / 2) < 2, res["bpm"]
    assert res["key"]["tonic"] in ("A", "C"), res["key"]  # ля минор / до мажор — параллельные
    s15 = res["snippets"]["15s"][0]
    assert any(a - 0.1 <= s15["start"] and s15["end"] <= b + 0.1 for a, b in choruses), \
        f"лучший 15-секундный отрезок {s15} не попал в припев {choruses}"
    bar_offsets = [(t % BAR) for t in res["bars"]]
    assert all(min(o, BAR - o) < 0.1 for o in bar_offsets), "такты определены со сдвигом"
    print("✓ анализ: темп, тональность и припев найдены верно")

    # 2. сниппеты
    print(run("snippet.py", str(track), "--durations", "15,30", "--format", "mp3"))
    snip_dir = tmp / "test_track_snippets"
    for d in (15, 30):
        a, sr = load(snip_dir / f"test_track_{d}s.mp3")
        rep = loudness_report(a, sr)
        assert abs(rep["duration_sec"] - d) < 0.1, rep
        assert abs(rep["lufs"] + 14) < 0.7, rep
        assert rep["true_peak_dbtp"] <= -0.8, rep
    print("✓ сниппеты: длина точная, -14 LUFS, пики ниже -1 dBTP")

    # 3. мастеринг без референса
    print(run("master.py", str(track), "--format", "wav"))
    rep = loudness_report(*load(tmp / "test_track_master.wav"))
    assert abs(rep["lufs"] + 14) < 0.5 and rep["true_peak_dbtp"] <= -0.9, rep
    print("✓ мастеринг простой цепочкой")

    # 4. генератор MIDI
    print(run("midi_gen.py", "--chords", "Am F C G", "--style", "trap", "--bpm", "140",
              "--out", str(tmp / "idea.mid")))
    m = pm.PrettyMIDI(str(tmp / "idea.mid"))
    assert {i.name for i in m.instruments} == {"Drums", "Bass", "Chords"}, [i.name for i in m.instruments]
    print("✓ генератор MIDI")

    if args.full:
        ref = tmp / "reference.wav"
        a, sr = load(track)
        save(np.clip(a * 3.0, -1, 1), sr, ref)  # «громкий» образец
        print(run("master.py", str(track), "--reference", str(ref), "--out", str(tmp / "test_track_ref.wav")))
        rep = loudness_report(*load(tmp / "test_track_ref.wav"))
        assert rep["true_peak_dbtp"] <= -0.9, rep
        print("✓ мастеринг по референсу")
        print(run("stems.py", str(snip_dir / "test_track_15s.mp3"), "--format", "mp3"))
        print("✓ стемы")
        venv_py = HERE / ".venv-midi" / "bin" / "python"
        if venv_py.exists():
            r = subprocess.run([str(venv_py), "audio2midi.py", str(track), "--bpm", str(BPM)],
                               capture_output=True, text=True, cwd=HERE)
            print(r.stdout.strip() or r.stderr[-500:])
            assert r.returncode == 0
            print("✓ аудио → MIDI")
        else:
            print("… аудио → MIDI пропущено: нет окружения .venv-midi (запусти setup.sh)")
    print(f"\nВсе проверки пройдены. Файлы: {tmp}")


if __name__ == "__main__":
    main()
