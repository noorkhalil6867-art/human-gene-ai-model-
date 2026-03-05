import logging
from datetime import datetime

def setup_logger(log_file="scrape.log"):
    logger = logging.getLogger("gene_scraper")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger

def now_iso():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
logger = setup_logger()
def log_info(message):
    logger.info(message)
def log_error(message):
    logger.error(message)
def log_debug(message):
    logger.debug(message)
def log_warning(message):
    logger.warning(message)
def log_critical(message):
    logger.critical(message)
def log_exception(message):
    logger.exception(message) 