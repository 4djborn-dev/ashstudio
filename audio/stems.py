#!/usr/bin/env python3
"""Разделение трека на стемы нейросетью Demucs (htdemucs).

Режимы:
    4 стема:  вокал, барабаны, бас, остальное (по умолчанию)
    --vocals: только вокал и минус (быстрее)

Примеры:
    python stems.py трек.mp3
    python stems.py трек.mp3 --vocals --format wav
    python stems.py трек.mp3 --model htdemucs_ft     # точнее, но в 4 раза дольше
"""
import argparse
import shutil
import sys
from pathlib import Path

NAMES_RU = {"vocals": "вокал", "drums": "барабаны", "bass": "бас", "other": "остальное",
            "no_vocals": "минус"}


def main() -> None:
    p = argparse.ArgumentParser(description="Стемы через Demucs")
    p.add_argument("input")
    p.add_argument("--vocals", action="store_true", help="только вокал + минус")
    p.add_argument("--model", default="htdemucs", help="htdemucs (быстро) или htdemucs_ft (точнее)")
    p.add_argument("--format", default="wav", choices=["wav", "mp3", "flac"])
    p.add_argument("--out", help="папка результата (по умолчанию <имя>_stems)")
    p.add_argument("--jobs", type=int, default=2, help="потоков процессора")
    args = p.parse_args()

    import demucs.separate  # тяжёлый импорт — только когда нужен

    src = Path(args.input)
    out_dir = Path(args.out) if args.out else src.with_name(src.stem + "_stems")
    tmp = out_dir / "_demucs"
    cmd = ["-n", args.model, "-o", str(tmp), "-j", str(args.jobs), "--filename", "{stem}.{ext}"]
    if args.vocals:
        cmd += ["--two-stems", "vocals"]
    if args.format == "mp3":
        cmd += ["--mp3", "--mp3-bitrate", "320"]
    elif args.format == "flac":
        cmd += ["--flac"]
    else:
        cmd += ["--int24"]
    cmd.append(str(src))
    print(f"Разделяю «{src.name}» моделью {args.model}… (на процессоре это несколько минут)")
    demucs.separate.main(cmd)

    produced = tmp / args.model
    for f in sorted(produced.glob("*.*")):
        ru = NAMES_RU.get(f.stem, f.stem)
        target = out_dir / f"{src.stem}_{ru}{f.suffix}"
        shutil.move(str(f), target)
        print(f"✓ {target.name}")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"Готово: {out_dir}")


if __name__ == "__main__":
    sys.exit(main())
