import logging
import os

from core.settings import Settings
from core.constants import *

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            "logs/nexus.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

app_logger = logging.getLogger("NEXUS")


def header(title):

    linea = "=" * 60

    print()

    print(linea)

    print(f"{ICON_INFO} {title}")

    print(linea)

    app_logger.info(f"===== {title} =====")


def info(msg):

    print(f"{ICON_INFO} {msg}")

    app_logger.info(msg)


def success(msg):

    print(f"{ICON_OK} {msg}")

    app_logger.info(msg)


def warning(msg):

    print(f"{ICON_INFO} {msg}")

    app_logger.warning(msg)


def error(msg):

    print(f"{ICON_INFO} {msg}")

    app_logger.error(msg)


def debug(*args):

    if Settings.DEBUG:

        print("{ICON_INFO}", *args)

        app_logger.debug(" ".join(str(x) for x in args))

def exception(e):

    app_logger.exception(e)

def exception(e):

    print(f"{ICON_INFO} {e}")

    app_logger.exception(e)