#!/usr/bin/env python3
"""Генератор MIDI-заготовок для Ableton: барабаны, бас, аккорды, арпеджио.

Задаёшь аккорды, темп и стиль — получаешь многодорожечный .mid
(и отдельные .mid на каждую партию). Перетаскиваешь в Ableton и вешаешь инструменты.

Аккорды: C, Am, F#m, Bb, G7, Cmaj7, Am7, Dsus2, Esus4, Bdim, Caug, Cadd9, Am9, C/E
(си можно писать и как B, и как H: Hm = Bm)
Стили: house, pop, trap, lofi, ambient, rock

Примеры:
    python midi_gen.py --chords "Am F C G" --bpm 124 --style house --bars 16
    python midi_gen.py --chords "Dm Bb F C" --bpm 140 --style trap --bars-per-chord 2
    python midi_gen.py --chords "Cmaj7 Am7 Dm7 G7" --bpm 80 --style lofi --out lofi.mid
"""
import argparse
import re
from pathlib import Path

import pretty_midi as pm

NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11, "H": 11}  # H = B (русская запись)
QUALITY = {
    "": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11], "m7": [0, 3, 7, 10],
    "sus2": [0, 2, 7], "sus4": [0, 5, 7], "dim": [0, 3, 6], "aug": [0, 4, 8], "add9": [0, 4, 7, 14],
    "m9": [0, 3, 7, 10, 14], "9": [0, 4, 7, 10, 14], "6": [0, 4, 7, 9], "m6": [0, 3, 7, 9],
    "5": [0, 7],
}
# General MIDI: в Ableton Drum Rack эти ноты = C1 (бочка), D1 (снейр), D#1 (клэп), F#1/A#1 (хэты)
KICK, SNARE, CLAP, CHH, OHH, RIM = 36, 38, 39, 42, 46, 37

# 16 шагов на такт: 1 = удар; цифра больше 1 — сила (velocity / 10)
DRUMS = {
    "house":   {KICK: "9000900090009000", CLAP: "0000900000009000", CHH: "0090009000900090",
                OHH: "0000000000000000"},
    "pop":     {KICK: "9000000090900000", SNARE: "0000900000009000", CHH: "7070707070707070"},
    "trap":    {KICK: "9000000000900000", SNARE: "0000000090000000",
                CHH: "7777777777777777"},
    "lofi":    {KICK: "9000000000900000", SNARE: "0000800000008000", CHH: "6060606060606060"},
    "rock":    {KICK: "9000000090900000", SNARE: "0000900000009000", CHH: "8080808080808080"},
    "ambient": {},
}
SETTINGS = {  # бас: ритм (шаги), октава; аккорды: ритм; арпеджио: есть/нет
    "house":   {"bass": "0090009000900090", "bass_oct": 2, "chords": "0000900000009000", "arp": True},
    "pop":     {"bass": "9000009000909000", "bass_oct": 2, "chords": "9000000090000000", "arp": True},
    "trap":    {"bass": "9000000000900000", "bass_oct": 1, "chords": "9000000000000000", "arp": False},
    "lofi":    {"bass": "9000000000900000", "bass_oct": 2, "chords": "9000000000000000", "arp": False},
    "rock":    {"bass": "9090909090909090", "bass_oct": 2, "chords": "9000000090000000", "arp": False},
    "ambient": {"bass": "9000000000000000", "bass_oct": 2, "chords": "9000000000000000", "arp": True},
}


def parse_chord(sym: str) -> tuple[int, list[int], int | None]:
    m = re.fullmatch(r"([A-H])([#b]?)([a-z0-9]*)(?:/([A-H][#b]?))?", sym.strip())
    if not m:
        raise ValueError(f"Не понимаю аккорд «{sym}»")
    root = NOTE[m.group(1)] + {"#": 1, "b": -1, "": 0}[m.group(2)]
    q = m.group(3)
    if q not in QUALITY:
        raise ValueError(f"Неизвестный тип аккорда «{q}» в «{sym}». Есть: {', '.join(k or 'мажор' for k in QUALITY)}")
    bass = None
    if m.group(4):
        b = m.group(4)
        bass = NOTE[b[0]] + {"#": 1, "b": -1}.get(b[1:], 0)
    return root % 12, QUALITY[q], bass


def voice(root: int, intervals: list[int], center: int = 60) -> list[int]:
    """Расположение аккорда поближе к середине клавиатуры (плавное голосоведение)."""
    base = root + 12 * ((center - root) // 12)
    notes = [base + i for i in intervals]
    while max(notes) > center + 12:
        notes = [n - 12 for n in notes]
    return sorted(notes)


def steps(pattern: str):
    for i, ch in enumerate(pattern):
        if ch != "0":
            yield i, min(127, int(ch) * 13 + 10)


def build(chords: list[str], bpm: float, style: str, bars: int, bars_per_chord: int) -> pm.PrettyMIDI:
    midi = pm.PrettyMIDI(initial_tempo=bpm)
    step = 60.0 / bpm / 4  # шестнадцатая
    bar = step * 16
    st = SETTINGS[style]

    drums = pm.Instrument(program=0, is_drum=True, name="Drums")
    bass = pm.Instrument(program=38, name="Bass")
    keys = pm.Instrument(program=89 if style == "ambient" else 4, name="Chords")
    arp = pm.Instrument(program=81, name="Arp")

    for b in range(bars):
        t0 = b * bar
        sym = chords[(b // bars_per_chord) % len(chords)]
        root, ints, slash = parse_chord(sym)
        chord_notes = voice(root, ints)
        bass_note = (slash if slash is not None else root) + 12 * (st["bass_oct"] + 1)

        for note, pat in DRUMS[style].items():
            for i, vel in steps(pat):
                if style == "trap" and note == CHH and b % 2 == 1 and i >= 12:
                    # трэп-«дробь» хэтов в конце каждого второго такта
                    for k in range(3):
                        s = t0 + i * step + k * step / 3
                        drums.notes.append(pm.Note(vel - 20, note, s, s + step / 4))
                    continue
                drums.notes.append(pm.Note(vel, note, t0 + i * step, t0 + i * step + step / 2))

        bass_pat = list(steps(st["bass"]))
        for j, (i, vel) in enumerate(bass_pat):
            nxt = bass_pat[j + 1][0] if j + 1 < len(bass_pat) else 16
            length = (nxt - i) * step * (0.9 if style != "trap" else 1.0)
            bass.notes.append(pm.Note(vel, bass_note, t0 + i * step, t0 + i * step + length))

        chord_pat = list(steps(st["chords"]))
        for j, (i, vel) in enumerate(chord_pat):
            nxt = chord_pat[j + 1][0] if j + 1 < len(chord_pat) else 16
            if style in ("lofi", "ambient", "trap"):
                nxt = 16  # тянем аккорд весь такт
            for n in chord_notes:
                keys.notes.append(pm.Note(vel - 25, n, t0 + i * step, t0 + nxt * step * 0.98))

        if st["arp"]:
            seq = chord_notes + [chord_notes[0] + 12]
            rate = 2 if style == "ambient" else 1  # шаг арпеджио в шестнадцатых
            for k, i in enumerate(range(0, 16, rate)):
                n = seq[k % len(seq)] + 12
                arp.notes.append(pm.Note(70 + (10 if i % 4 == 0 else 0), n,
                                         t0 + i * step, t0 + (i + rate) * step * 0.95))

    for inst in (drums, bass, keys, arp):
        if inst.notes:
            midi.instruments.append(inst)
    return midi


def main() -> None:
    p = argparse.ArgumentParser(description="MIDI-заготовка трека для Ableton")
    p.add_argument("--chords", required=True, help='аккорды через пробел, например "Am F C G"')
    p.add_argument("--bpm", type=float, default=120)
    p.add_argument("--style", default="pop", choices=SETTINGS.keys())
    p.add_argument("--bars", type=int, default=16, help="длина в тактах")
    p.add_argument("--bars-per-chord", type=int, default=1)
    p.add_argument("--out", default="idea.mid")
    p.add_argument("--no-split", action="store_true", help="не сохранять партии отдельными файлами")
    args = p.parse_args()

    chords = args.chords.split()
    try:
        midi = build(chords, args.bpm, args.style, args.bars, args.bars_per_chord)
    except ValueError as e:
        raise SystemExit(f"✗ {e}")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    midi.write(str(out))
    print(f"✓ {out}: {', '.join(i.name for i in midi.instruments)} — {args.bars} тактов, {args.bpm:g} BPM")
    if not args.no_split:
        for inst in midi.instruments:
            single = pm.PrettyMIDI(initial_tempo=args.bpm)
            single.instruments.append(inst)
            part = out.with_name(f"{out.stem}_{inst.name.lower()}.mid")
            single.write(str(part))
            print(f"  ✓ {part.name}")


if __name__ == "__main__":
    main()
