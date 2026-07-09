import logging
import os

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

DEBUG = False


def header(title):

    linea = "=" * 60

    print()

    print(linea)

    print(f"🚀 {title}")

    print(linea)

    app_logger.info(f"===== {title} =====")


def info(msg):

    print(f"ℹ {msg}")

    app_logger.info(msg)


def success(msg):

    print(f"✅ {msg}")

    app_logger.info(msg)


def warning(msg):

    print(f"⚠ {msg}")

    app_logger.warning(msg)


def error(msg):

    print(f"❌ {msg}")

    app_logger.error(msg)


def debug(*args):

    if DEBUG:

        print("🐞", *args)

        app_logger.debug(" ".join(str(x) for x in args))

def exception(e):

    print(f"💥 {e}")

    app_logger.exception(e)