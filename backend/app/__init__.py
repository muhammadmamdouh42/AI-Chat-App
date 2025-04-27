from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI

# Environment & logging
load_dotenv(find_dotenv())

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

logger = logging.getLogger("app")
logger.info("Logging initialised at %s level", LOG_LEVEL)

# FastAPI instance
app = FastAPI(
    title="AI Chat backend",
    version="1.0.0",
    docs_url="/",
)

from app.settings import UPLOAD_DIR

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
logger.debug("UPLOAD_DIR set to %s", UPLOAD_DIR)
