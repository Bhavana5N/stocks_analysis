#!/usr/bin/env bash
set -euo pipefail
export $(grep -v '^#' .env | xargs) || true
python - <<'PY'
from pathlib import Path
p = Path('api/app/static'); p.mkdir(parents=True, exist_ok=True)
PY
uvicorn app.main:app --reload --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}"
