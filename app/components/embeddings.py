import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH,override=True)


def get_embeddings():
    try:
        token = os.getenv("HF_TOKEN")
        if not token:
            raise RuntimeError("HF_TOKEN environment variable is not set. Please set it in the .env file or your environment.")
        token = token.strip()
        logger.info("Initializing HuggingFaceHubEmbeddings with the specified model.")

        model = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
        logger.info("HuggingFaceHubEmbeddings model initialized successfully.")
        return model
    except Exception as e:
        error_message = CustomException.get_detailed_error_message(f"Failed to initialize HuggingFaceHubEmbeddings with the specified model.",e)
        logger.error(str(error_message))
        raise
