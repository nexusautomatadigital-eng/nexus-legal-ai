import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from config import *
from styles import load_css


# Nuevos componentes del Command Center
from dashboard.components import greeting
from dashboard.components import status_overview
from core.session_service import SessionService

from components.priority_card import render_priority_card

# Dominio
from domain.executive_service import ExecutiveService

# ==========================================================
# INICIALIZACIÓN
# ==========================================================

def render_command_center():

    load_css()

    context = SessionService.get_context()

    executive = ExecutiveService(context.cliente_id)


    # ==========================================================
    # HOME DEL CLIENTE
    # ==========================================================

    greeting.render(context.nombre)


    # ==========================================================
    # ESTADO GENERAL
    # (Temporal)
    # ==========================================================

    status_overview.render(
        criticos=1,
        importantes=2,
        estables=8,
    )


    # ==========================================================
    # PRIORIDAD DEL DÍA
    # ==========================================================

    priority = executive.get_priority()

    render_priority_card(priority)