import logging
import os
from datetime import datetime

# text file
def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(name)s - %(message)s",
        encoding='utf-8',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("rpa")
