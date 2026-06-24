import os
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

logger = get_logger(__name__)
DATA_PATH = Path(DATA_PATH).expanduser().resolve()
def load_pdf(file_path:str=DATA_PATH):
    try:
        if not os.path.exists(file_path):
            raise CustomException(f"Data path not found: {file_path}")

        logger.info(f"Loading PDF file from path: {file_path}")

        loader = PyPDFLoader(str(file_path))

        documents = loader.load()

        if not documents:
            logger.warning(f"No documents found in the specified path: {file_path}")
        else:
            logger.info(f"Loaded {len(documents)} documents from the specified path: {file_path}")

        return documents
    
    except Exception as e:
        error_message = CustomException.get_detailed_error_message(f"Failed to load PDF file from path: {file_path}",e)
        logger.error(str(error_message))
        return []

def create_text_chuncks(documents):
    try:
        if not documents:
            raise CustomException(f"No documents found")

        logger.info(f"Splitting documents into chunks with size {CHUNK_SIZE} and overlap {CHUNK_OVERLAP}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

        text_chunks = text_splitter.split_documents(documents)

        logger.info(f"Created {len(text_chunks)} text chunks from the documents")
        return text_chunks

    except Exception as e:
        error_message = CustomException.get_detailed_error_message(f"Failed to create text chunks from the documents",e)
        logger.error(str(error_message))
        return []