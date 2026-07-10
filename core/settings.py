"""
Configuración global de Nexus Automata.
Toda constante del sistema debe vivir aquí.
"""

# ==========================================
# DEBUG
# ==========================================

DEBUG = False

# ==========================================
# TIMEOUTS
# ==========================================

TIMEOUT_PORTAL = 30

TIMEOUT_ELEMENTO = 15

TIMEOUT_SAMAI = 60

# ==========================================
# REINTENTOS
# ==========================================

MAX_REINTENTOS_PORTAL = 3

MAX_REINTENTOS_CAPTCHA = 5

# ==========================================
# OPENAI
# ==========================================

OPENAI_MODEL = "gpt-5"

# ==========================================
# DASHBOARD
# ==========================================

REFRESH_DASHBOARD = 30

# ==========================================
# VERSION
# ==========================================

VERSION = "Nexus 1.0"

# ==========================================
# WEBDRIVER
# ==========================================

WAIT_SHORT = 5

WAIT_MEDIUM = 15

WAIT_LONG = 30

WAIT_EXTRA = 60

# ==========================================
# NEXUS
# ==========================================

APP_NAME = "Nexus Automata"

APP_VERSION = "1.0.0"

BUILD = "Enterprise Preview"

# ==========================================
# CONFIG
# ==========================================

class Settings:

    DEBUG = DEBUG

    WAIT_SHORT = WAIT_SHORT

    WAIT_MEDIUM = WAIT_MEDIUM

    WAIT_LONG = WAIT_LONG

    WAIT_EXTRA = WAIT_EXTRA

    APP_NAME = APP_NAME

    APP_VERSION = APP_VERSION

    BUILD = BUILD

    OPENAI_MODEL = OPENAI_MODEL

    MAX_REINTENTOS_PORTAL = MAX_REINTENTOS_PORTAL