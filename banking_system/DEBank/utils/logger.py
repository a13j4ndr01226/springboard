import logging
import os

# Create the logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/bank_system.log"),
        logging.StreamHandler()  # Also logs to terminal
    ]
)

logger = logging.getLogger(__name__)
