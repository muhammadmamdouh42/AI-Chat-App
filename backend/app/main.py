from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from fastapi import Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

from app import app as fastapi_app
from app.agent import agent
from app.settings import ALLOWED_EXTS, ALLOWED_MIME_TYPES, UPLOAD_DIR
from app.vectorstore import vectorstore

logger = logging.getLogger(__name__)

# Helpers
def _validate_file(upload: UploadFile) -> None:
    ext_ok = Path(upload.filename).suffix.lower() in ALLOWED_EXTS
    mime_ok = upload.content_type in ALLOWED_MIME_TYPES
    if not (ext_ok and mime_ok):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Unsupported file '{upload.filename}'. "
                "Only .txt and .pdf are accepted."
            ),
        )


async def _save_file(upload: UploadFile) -> Path:
    dest_path = UPLOAD_DIR / Path(upload.filename).name

    # Stream in 8 KiB chunks – saves RAM on big files
    with dest_path.open("wb") as buffer:
        while chunk := await upload.read(8192):
            buffer.write(chunk)
    await upload.close()

    logger.info("Uploaded %s → %s", upload.filename, dest_path)
    return dest_path


# Routes
@fastapi_app.post("/upload", response_class=JSONResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """Receive multiple files, persist them, then ingest to the vectorstore."""
    saved_paths: List[str] = []

    for upload in files:
        _validate_file(upload)
        saved_paths.append(str(await _save_file(upload)))

    vectorstore.load_documents(saved_paths)
    return {"uploaded": saved_paths}


class PromptIn(BaseModel):
    prompt: str

    @field_validator("prompt")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Prompt cannot be empty.")
        return v


class AnswerOut(BaseModel):
    answer: str


@fastapi_app.post("/ask", response_model=AnswerOut)
async def answer_prompt(data: PromptIn, _: None = Depends()):
    """Chat with the agent. A constant thread_id is used for demo purposes."""
    reply = agent.chat(data.prompt, thread_id="1")
    return AnswerOut(answer=reply)
