import logging
import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),                        # Console
        logging.FileHandler("app.log", encoding="utf-8")  # File
    ]
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
