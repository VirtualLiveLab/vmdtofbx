import logging
import logging.handlers
import pathlib

from discord.utils import _ColourFormatter


def getMyLogger(name: str) -> logging.Logger:  # name: __name__
    # make log directory
    pathlib.Path("log").mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    streamHandler = logging.StreamHandler()
    file_handler = logging.handlers.TimedRotatingFileHandler(
        f"./log/{name}.log",
        when="midnight",
        encoding="utf-8",
        backupCount=10,
    )

    # set format
    formatter = _ColourFormatter()
    literal_formatter = logging.Formatter("%(asctime)s:%(levelname)s:\n%(name)s:%(message)s")
    streamHandler.setFormatter(formatter)
    file_handler.setFormatter(literal_formatter)

    # set level
    logger.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)

    # add handler
    if not logger.hasHandlers():
        logger.addHandler(streamHandler)
        logger.addHandler(file_handler)

    return logger
