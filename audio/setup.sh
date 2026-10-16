#!/usr/bin/env bash
# Установка аудиоинструментов АСШ Студии (Linux / облачная среда / GitHub Actions / WSL).
# Нужны: ffmpeg и uv (https://docs.astral.sh/uv/).
#   bash setup.sh          — основное окружение .venv
#   bash setup.sh --midi   — плюс окружение .venv-midi для audio2midi.py
set -euo pipefail
cd "$(dirname "$0")"

command -v ffmpeg >/dev/null || { echo "Нужен ffmpeg: sudo apt-get install -y ffmpeg"; exit 1; }
command -v uv >/dev/null || { echo "Ставлю uv…"; curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"; }

echo "→ Основное окружение .venv"
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python torch torchaudio --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv/bin/python -r requirements.txt

if [[ "${1:-}" == "--midi" ]]; then
  echo "→ Окружение .venv-midi (аудио → MIDI)"
  uv venv --python 3.11 .venv-midi
  uv pip install --python .venv-midi/bin/python -r requirements-midi.txt
fi

echo "✓ Готово. Проверка: .venv/bin/python selftest.py"
