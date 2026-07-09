import logging
import os

# =====================================
# CONFIGURACION
# =====================================

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

logger = logging.getLogger("NEXUS")

DEBUG = False


# =====================================
# FUNCIONES
# =====================================

def info(msg):

    logger.info(msg)


def success(msg):

    logger.info("✅ " + str(msg))


def warning(msg):

    logger.warning("⚠ " + str(msg))


def error(msg):

    logger.error("❌ " + str(msg))


def exception(e):

    logger.exception(e)


def header(title):

    linea = "=" * 60

    logger.info("")
    logger.info(linea)
    logger.info("🚀 " + str(title))
    logger.info(linea)


def debug(*args):

    if DEBUG:

        logger.debug(" ".join(map(str, args)))