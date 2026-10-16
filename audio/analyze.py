#!/usr/bin/env python3
"""Анализ трека: темп, тональность, такты, акценты, громкость, лучшие отрезки для сниппетов.

Пример:
    python analyze.py трек.mp3
    python analyze.py трек.mp3 --lengths 15,30,60 --json анализ.json
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ash_audio import analysis as an  # noqa: E402
from ash_audio.io import load, loudness_report  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Анализ трека для монтажа и сниппетов")
    p.add_argument("input", help="аудио- или видеофайл")
    p.add_argument("--lengths", default="15,30,60", help="длины сниппетов в секундах, через запятую")
    p.add_argument("--top", type=int, default=3, help="сколько вариантов на каждую длину")
    p.add_argument("--bpm", type=float, help="темп, если знаешь точно (из Suno/Ableton)")
    p.add_argument("--json", help="куда сохранить полный результат (по умолчанию рядом с файлом)")
    args = p.parse_args()

    audio, sr = load(args.input)
    res = an.analyze(audio, sr, bpm=args.bpm)
    res["loudness"] = loudness_report(audio, sr)
    res["snippets"] = {}
    for length in [float(x) for x in args.lengths.split(",") if x.strip()]:
        if length <= res["duration_sec"]:
            res["snippets"][f"{length:g}s"] = an.best_segments(res, length, top=args.top)

    out = Path(args.json) if args.json else Path(args.input).with_suffix(".analysis.json")
    out.write_text(json.dumps(an.public(res), ensure_ascii=False, indent=2), encoding="utf-8")

    k = res["key"]
    print(f"Файл:         {args.input}")
    print(f"Длительность: {res['duration_sec']:.1f} с")
    print(f"Темп:         {res['bpm']:.1f} BPM (такт {60 / res['bpm'] * 4:.2f} с)")
    print(f"Тональность:  {k['key']} (уверенность {k['confidence']})")
    print(f"Громкость:    {res['loudness']['lufs']} LUFS, пик {res['loudness']['true_peak_dbtp']} dBTP")
    print(f"Тактов: {len(res['bars'])}, сильных акцентов: {len(res['accents'])}")
    for name, segs in res["snippets"].items():
        txt = ", ".join(f"{s['start']:.1f}–{s['end']:.1f} с" for s in segs)
        print(f"Лучшие отрезки {name}: {txt}")
    print(f"Полный отчёт: {out}")


if __name__ == "__main__":
    main()
