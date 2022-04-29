""" log hal's activity """

from pathlib import Path

from loguru import logger

# set logs folder path
LOGSPATH = Path.cwd() / "logs"

# register log sinks with loguru logger
logger.add(
    LOGSPATH / "log_{time}.log",
    format="<cyan>[{time:YY-MM-DD HH:mm:ss}]</> <lvl>[{module}] - {message}</>",
    rotation="24 hours",  # current log file closed and new one started every 24 hours
    retention="1 month",  # log files created more than a month ago will be removed
    backtrace=True,
    diagnose=True,
)

logger.debug("Logger activated!")
