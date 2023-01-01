import logging

# adapted from:
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output/56944256#56944256


class ColoredFormatter(logging.Formatter):
    RED = "\033[0;31m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    YELLOW = "\033[0;33m"
    RESET = "\033[0m"

    COLORED_FORMAT = "[%(levelname)-8s]"
    TEXT_FORMAT = "%(asctime)s %(name)-20s %(message)s"

    FORMATS = {
        logging.DEBUG: DARK_GRAY + COLORED_FORMAT + RESET + " " + TEXT_FORMAT,
        logging.INFO: LIGHT_GRAY + COLORED_FORMAT + RESET + " " + TEXT_FORMAT,
        logging.WARNING: YELLOW + COLORED_FORMAT + RESET + " " + TEXT_FORMAT,
        logging.ERROR: RED + COLORED_FORMAT + RESET + " " + TEXT_FORMAT,
        logging.CRITICAL: LIGHT_RED
        + COLORED_FORMAT
        + RESET
        + " "
        + TEXT_FORMAT,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        return formatter.format(record)
