from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.components.embeddings import get_embeddings
from app.common.logger import get_logger
from app.config.config import DB_FAISS_PATH

logger = get_logger(__name__)


def load_vector_store():
    db_path = Path(DB_FAISS_PATH).expanduser().resolve()

    try:
        embedding_model = get_embeddings()

        index_file = db_path / "index.faiss"
        metadata_file = db_path / "index.pkl"

        if not index_file.exists() or not metadata_file.exists():
            logger.warning(
                "FAISS vector store files were not found at: %s",
                db_path,
            )
            return None

        logger.info("Loading FAISS vector store from: %s", db_path)

        vector_store = FAISS.load_local(
            folder_path=str(db_path),
            embeddings=embedding_model,
            allow_dangerous_deserialization=True,
        )

        logger.info("FAISS vector store loaded successfully.")
        return vector_store

    except Exception:
        logger.exception(
            "Failed to load FAISS vector store from: %s",
            db_path,
        )
        raise


def create_vector_store(text_chunks):
    db_path = Path(DB_FAISS_PATH).expanduser().resolve()

    try:
        if not text_chunks:
            raise ValueError("No text chunks were provided.")

        logger.info(
            "Creating FAISS vector store from %d text chunks.",
            len(text_chunks),
        )
        logger.info("FAISS vector store output path: %s", db_path)

        # Explicitly create the destination directory.
        db_path.mkdir(parents=True, exist_ok=True)

        embedding_model = get_embeddings()

        vector_store = FAISS.from_documents(
            documents=text_chunks,
            embedding=embedding_model,
        )

        vector_store.save_local(str(db_path))

        index_file = db_path / "index.faiss"
        metadata_file = db_path / "index.pkl"

        if not index_file.exists():
            raise RuntimeError(f"FAISS index was not created: {index_file}")

        if not metadata_file.exists():
            raise RuntimeError(f"FAISS metadata was not created: {metadata_file}")

        logger.info("FAISS vector store created successfully at: %s", db_path)
        return vector_store

    except Exception:
        logger.exception(
            "Failed to create FAISS vector store at: %s",
            db_path,
        )
        raise