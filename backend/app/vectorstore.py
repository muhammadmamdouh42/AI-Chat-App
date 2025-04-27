from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from app.settings import VECTORSTORE_DIR

logger = logging.getLogger(__name__)


class Vectorstore:

    _SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)

    def __init__(self) -> None:
        embeddings = OpenAIEmbeddings()
        self._db = Chroma(
            persist_directory=str(VECTORSTORE_DIR),
            embedding_function=embeddings,
        )
        logger.info("Vectorstore initialised → %s", VECTORSTORE_DIR)

    # Public API
    def load_documents(self, paths: Iterable[str | Path]) -> None:
        all_chunks: List = []

        for raw_path in paths:
            path = Path(raw_path)
            if not path.exists():
                logger.warning("%s does not exist – skipping.", path)
                continue

            match path.suffix.lower():
                case ".pdf":
                    loader = PyPDFLoader(str(path))
                case ".txt":
                    loader = TextLoader(str(path), encoding="utf-8")
                case _:
                    logger.warning("%s: unsupported file type – skipping.", path.name)
                    continue

            try:
                chunks = loader.load_and_split(self._SPLITTER)
                all_chunks.extend(chunks)
                logger.debug("%s → %s chunks", path.name, len(chunks))
            except Exception:
                logger.exception("Failed to process %s", path.name)

        if not all_chunks:
            logger.info("No valid documents were added.")
            return

        self._db.add_documents(all_chunks)
        logger.info(
            "Added %s chunks – store now holds %s docs.",
            len(all_chunks),
            self._db._collection.count(),
        )

    def get_retriever(self):
        """Return a retriever bound to the underlying DB."""
        return self._db.as_retriever()


vectorstore = Vectorstore()  # singleton
