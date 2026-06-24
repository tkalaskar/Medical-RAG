import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

HF_TOKEN = (
    os.environ.get("HF_TOKEN")
    or os.environ.get("HUGGINGFACEHUB_API_TOKEN")
)
HUGGINGFACE_REPO_ID = os.environ.get(
    "HUGGINGFACE_REPO_ID",
    "Qwen/Qwen2.5-7B-Instruct",
)
DB_FAISS_PATH = PROJECT_ROOT / "vectorstore" / "db_faiss"
DATA_PATH = PROJECT_ROOT / "data" / "The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
