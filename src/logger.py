import logging
import sys

def setup_logging() -> logging.Logger:
    """
    Настраиваем логгер
    """
    logger = logging.getLogger("For simulation")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt='%(asctime)s   %(message)s', datefmt=' %Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler('simulation.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger