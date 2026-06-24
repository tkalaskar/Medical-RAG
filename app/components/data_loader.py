from app.components.pdf_loader import create_text_chuncks, load_pdf
from app.components.vector_store import create_vector_store
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)


def process_and_store_pdfs():
    """Load the configured PDF, split it, and persist a FAISS vector store."""
    try:
        logger.info("Loading PDF files from the specified path.")
        documents = load_pdf()
        if not documents:
            raise RuntimeError("No PDF pages were loaded.")

        logger.info(
            "Loaded %d PDF pages from the specified path.",
            len(documents),
        )

        text_chunks = create_text_chuncks(documents)
        if not text_chunks:
            raise RuntimeError("No text chunks were created from the PDF.")

        vector_store = create_vector_store(text_chunks)

        if vector_store is None:
            raise RuntimeError("create_vector_store() returned None")

        if isinstance(vector_store, list):
            raise RuntimeError(
                "create_vector_store() returned a list instead of a FAISS "
                f"store: {vector_store}"
            )

        logger.info("Vector store created successfully.")
        return vector_store

    except Exception as e:
        error_message = CustomException.get_detailed_error_message(
            "Failed to process and store PDF files.",
            e,
        )
        logger.error(str(error_message))
        raise


if __name__ == "__main__":
    print("Starting data loader...")
    result = process_and_store_pdfs()
    print("Data loader finished. Result type:", type(result))
