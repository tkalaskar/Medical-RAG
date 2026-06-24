import os

HF_TOEKN = os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"
DB_FAISS_PATH="vectorstore/db_faiss"
DATA_PATH="data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf"
CHUNK_SIZE=500
CHUNK_OVERLAP=50