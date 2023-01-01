import logging

from .colored_formatter import ColoredFormatter


class Logger:
    # CRITICAL ERROR WARNING INFO DEBUG
    # TODO: check how to set this globally for all usage
    level = logging.WARNING
    # level = logging.DEBUG

    @staticmethod
    def set_log_level(level: int) -> None:
        Logger.level = level

    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(Logger.level)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            ColoredFormatter(datefmt="%Y-%m-%d %H:%M:%S")
        )
        self._logger.addHandler(console_handler)

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def debug(self, msg: str) -> None:
        self._logger.debug(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)

    def critical(self, msg: str) -> None:
        self._logger.critical(msg)
