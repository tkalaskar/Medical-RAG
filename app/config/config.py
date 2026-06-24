import os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
HF_TOKEN = os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"
DB_FAISS_PATH=PROJECT_ROOT / "vectorstore" / "db_faiss"
DATA_PATH=PROJECT_ROOT / "data" / "The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf"
CHUNK_SIZE=500
CHUNK_OVERLAP=50