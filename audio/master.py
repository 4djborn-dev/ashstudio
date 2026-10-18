#!/usr/bin/env python3
"""Мастеринг трека.

С референсом — Matchering: подгоняет тембр, громкость и ширину под трек-образец.
Без референса — мягкая цепочка: срез инфраниза, лёгкая компрессия, громкость и лимитер.

Примеры:
    python master.py мой_трек.wav --reference образец.mp3
    python master.py мой_трек.wav --lufs -14            # для соцсетей и стримингов
    python master.py мой_трек.wav --lufs -9 --format wav  # «громкий клубный» вариант
"""
import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ash_audio.dynamics import normalize  # noqa: E402
from ash_audio.io import load, loudness_report, lufs, save  # noqa: E402


def simple_chain(audio, sr):
    from pedalboard import Compressor, HighpassFilter, Pedalboard
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=28),
        Compressor(threshold_db=-20, ratio=1.8, attack_ms=25, release_ms=200),
    ])
    return board(audio, sr)


def main() -> None:
    p = argparse.ArgumentParser(description="Мастеринг: по референсу или простой цепочкой")
    p.add_argument("input")
    p.add_argument("--reference", help="трек-образец звучания")
    p.add_argument("--lufs", type=float, default=None,
                   help="целевая громкость; без референса по умолчанию -14, "
                        "с референсом — громкость как у образца")
    p.add_argument("--ceiling", type=float, default=-1.0, help="потолок пиков, dBTP")
    p.add_argument("--format", default="wav", choices=["wav", "mp3", "m4a", "flac"])
    p.add_argument("--out", help="файл результата")
    args = p.parse_args()

    src = Path(args.input)
    out = Path(args.out) if args.out else src.with_name(f"{src.stem}_master.{args.format}")
    before = loudness_report(*load(src))

    if args.reference:
        import matchering as mg
        mg.log(lambda *a: None)
        with tempfile.TemporaryDirectory() as tmp:
            tgt, ref, res = Path(tmp) / "t.wav", Path(tmp) / "r.wav", Path(tmp) / "m.wav"
            save(*load(src), tgt)
            save(*load(args.reference), ref)
            mg.process(target=str(tgt), reference=str(ref), results=[mg.pcm24(str(res))])
            audio, sr = load(res)
        print(f"Мастеринг по референсу «{Path(args.reference).name}»")
    else:
        audio, sr = load(src)
        audio = simple_chain(audio, sr)
        print("Мастеринг простой цепочкой (без референса)")
        if args.lufs is None:
            args.lufs = -14.0

    if args.lufs is None:
        # громкость как у образца, но истинные пики всё равно держим под потолком
        # (лимитер Matchering следит только за сэмплами, межсэмпловые пики проскакивают)
        args.lufs = lufs(audio, sr)
    audio = normalize(audio, sr, target_lufs=args.lufs, ceiling_dbtp=args.ceiling)
    save(audio, sr, out)
    after = loudness_report(audio, sr)
    print(f"До:    {before['lufs']} LUFS, пик {before['true_peak_dbtp']} dBTP")
    print(f"После: {after['lufs']} LUFS, пик {after['true_peak_dbtp']} dBTP")
    print(f"✓ {out}")


if __name__ == "__main__":
    main()
