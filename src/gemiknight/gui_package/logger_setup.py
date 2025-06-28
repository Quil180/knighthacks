import logging
import sys
from io import StringIO

# Memory stream for logs
log_stream = StringIO()

# Get or create the logger
logger = logging.getLogger("web_logger")
logger.setLevel(logging.DEBUG)

# Avoid adding duplicate handlers if re-imported
if not logger.hasHandlers():
    # StreamHandler to memory
    memory_handler = logging.StreamHandler(log_stream)
    memory_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    memory_handler.setFormatter(memory_formatter)
    logger.addHandler(memory_handler)

    # StreamHandler to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)