#!/usr/bin/env python3
"""Аудио → MIDI (нейросеть Basic Pitch от Spotify).

Лучше всего работает на отдельной партии: сначала выдели стем (stems.py),
потом сними с него ноты. Полученный .mid перетаскивается в Ableton.

Работает в отдельном окружении (.venv-midi), см. README.

Примеры:
    python audio2midi.py трек_вокал.wav --preset vocal --bpm 120
    python audio2midi.py трек_бас.wav --preset bass --bpm 120
    python audio2midi.py пианино.wav
"""
import argparse
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

PRESETS = {
    # мин. частота, макс. частота, порог атаки, порог ноты, мин. длина ноты (мс)
    "vocal": (80, 1100, 0.6, 0.4, 120),
    "bass": (30, 350, 0.5, 0.3, 90),
    "keys": (27, 4200, 0.5, 0.3, 60),
    "lead": (150, 2500, 0.55, 0.35, 80),
}


def main() -> None:
    p = argparse.ArgumentParser(description="Снять ноты с аудио в MIDI")
    p.add_argument("input")
    p.add_argument("--preset", default="keys", choices=PRESETS.keys(),
                   help="vocal — мелодия голоса, bass — бас, keys — аккорды/клавиши, lead — соло")
    p.add_argument("--bpm", type=float, default=120.0, help="темп трека (возьми из analyze.py)")
    p.add_argument("--out", help="файл .mid")
    args = p.parse_args()

    from basic_pitch import ICASSP_2022_MODEL_PATH
    from basic_pitch.inference import predict

    fmin, fmax, onset, frame, min_len = PRESETS[args.preset]
    _, midi, notes = predict(
        args.input, ICASSP_2022_MODEL_PATH,
        onset_threshold=onset, frame_threshold=frame, minimum_note_length=min_len,
        minimum_frequency=fmin, maximum_frequency=fmax,
        melodia_trick=True, midi_tempo=args.bpm,
    )
    src = Path(args.input)
    out = Path(args.out) if args.out else src.with_name(f"{src.stem}_{args.preset}.mid")
    name = f"{src.stem} ({args.preset})"
    try:
        name.encode("latin-1")  # имена дорожек в MIDI не поддерживают кириллицу
    except UnicodeEncodeError:
        name = args.preset
    for inst in midi.instruments:
        inst.name = name
    midi.write(str(out))
    print(f"✓ {out} — нот: {len(notes)}")


if __name__ == "__main__":
    main()
