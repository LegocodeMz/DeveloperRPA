import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://rpa.xidondzo.com/")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "20"))
    OUTPUT_PATH = os.getenv("OUTPUT_PATH", "./output")
    LOG_PATH = os.getenv("LOG_PATH", "./logs")
