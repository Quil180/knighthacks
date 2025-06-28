import logging
import sys

def setup_logger():
    # sets up a centralized logger for the application
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout  # log to standard output
    )

    # we can also add a file handler to log to a file, but I dont think we need it right now.
    # file_handler = logging.FileHandler("app.log")
    # file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    # logging.getLogger().addHandler(file_handler)

    logging.info("Logger configured.")
    return logging.getLogger()

# create a logger instance to be imported by other modules
logger = setup_logger()
