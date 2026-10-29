#!/usr/bin/env python3
"""Нарезка трека под соцсети: точная длина, старт с такта, фейды, громкость под платформы.

По умолчанию сам находит лучший отрезок (обычно припев).

Примеры:
    python snippet.py трек.mp3                         # 15, 30 и 60 с, авто-выбор отрезка
    python snippet.py трек.mp3 --durations 30 --start 45.2
    python snippet.py трек.mp3 --durations 15 --format wav --lufs -14
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ash_audio import analysis as an  # noqa: E402
from ash_audio.dynamics import fade, normalize  # noqa: E402
from ash_audio.io import load, loudness_report, save  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Сниппеты трека для Shorts / Reels / VK Клипов")
    p.add_argument("input")
    p.add_argument("--durations", default="15,30,60", help="длины в секундах, через запятую")
    p.add_argument("--start", type=float, help="начало вручную (с); иначе — автоматически")
    p.add_argument("--no-snap", action="store_true", help="не подгонять начало к первой доле такта")
    p.add_argument("--bpm", type=float, help="темп, если знаешь точно")
    p.add_argument("--preroll", type=float, default=0.03,
                   help="начать чуть раньше доли, чтобы не срезать атаку удара, с")
    p.add_argument("--fade-in", type=float, default=0.01, help="появление, с")
    p.add_argument("--fade-out", type=float, default=1.5, help="затухание, с")
    p.add_argument("--lufs", type=float, default=-14.0, help="целевая громкость (соцсети: -14)")
    p.add_argument("--ceiling", type=float, default=-1.0, help="потолок пиков, dBTP")
    p.add_argument("--format", default="mp3", choices=["mp3", "wav", "m4a", "flac"])
    p.add_argument("--out", help="папка для результата (по умолчанию <имя>_snippets)")
    args = p.parse_args()

    src = Path(args.input)
    out_dir = Path(args.out) if args.out else src.with_name(src.stem + "_snippets")
    audio, sr = load(src)
    info = an.analyze(audio, sr, bpm=args.bpm)
    total = info["duration_sec"]

    report = {"source": str(src), "bpm": info["bpm"], "key": info["key"]["key"], "snippets": []}
    for d in [float(x) for x in args.durations.split(",") if x.strip()]:
        if d > total:
            print(f"⚠ {d:g} с длиннее трека ({total:.1f} с) — пропускаю")
            continue
        if args.start is not None:
            start = args.start if args.no_snap else an.snap_to_bar(args.start, info["bars"])
        else:
            start = an.best_segments(info, d, top=1)[0]["start"]
        if not args.no_snap:
            start -= args.preroll
        start = max(0.0, min(start, total - d))
        a, b = int(round(start * sr)), int(round((start + d) * sr))
        clip = audio[:, a:b]
        clip = fade(clip, sr, fade_in=args.fade_in, fade_out=args.fade_out)
        clip = normalize(clip, sr, target_lufs=args.lufs, ceiling_dbtp=args.ceiling)
        out = save(clip, sr, out_dir / f"{src.stem}_{d:g}s.{args.format}")
        rep = loudness_report(clip, sr)
        # акценты внутри отрезка, со смещением от его начала — точки для склеек видео
        cuts = [round(t - start, 3) for t in info["accents"] if start <= t < start + d]
        beats = [round(t - start, 3) for t in info["beats"] if start <= t < start + d]
        report["snippets"].append({"file": out.name, "start": round(start, 3), "duration": d,
                                   **rep, "beats": beats, "accents": cuts})
        print(f"✓ {out.name}: {start:.2f}–{start + d:.2f} с, {rep['lufs']} LUFS, пик {rep['true_peak_dbtp']} dBTP")

    (out_dir / "snippets.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Готово: {out_dir}")


if __name__ == "__main__":
    main()
