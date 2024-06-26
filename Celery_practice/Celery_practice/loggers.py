import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file = logging.FileHandler("logs.logs_all.log")
file.setLevel(logging.DEBUG)
file.setFormatter(formatter)

error_file = logging.FileHandler("logs.logs_error.log")
error_file.setLevel(logging.ERROR)
error_file.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file)
logger.addHandler(error_file)
