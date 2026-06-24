import os
import sys
import logging
from datetime import datetime

from pathlib import Path

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE=os.path.join(LOGS_DIR,f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,

)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logging.getLogger(name)