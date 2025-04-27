"""Centralised project settings."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Final

# Directories
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
DATA_DIR: Final[Path] = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

UPLOAD_DIR: Final[Path] = BASE_DIR / "uploads"

# Vector store
VECTORSTORE_DIR: Final[Path] = DATA_DIR / "chroma"

# Upload constraints
ALLOWED_EXTS: Final[set[str]] = {".txt", ".pdf"}
ALLOWED_MIME_TYPES: Final[set[str]] = {"text/plain", "application/pdf"}

# OpenAI
OPENAI_MODEL_NAME: Final[str] = os.getenv("OPENAI_MODEL", "openai:gpt-4o-mini")
