import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import *

from styles import load_css

from components.executive import render_executive_summary

from components.metrics import render_kpi

from components.navbar import render_navbar

from domain.action_service import ActionService

from components.timeline import render_timeline

from components.actions import render_actions

import streamlit as st

from components.priority_card import render_priority_card

load_css()

render_navbar()

from domain.dashboard_service import DashboardService
from domain.executive_service import ExecutiveService

service = DashboardService()
executive = ExecutiveService()

kpis = executive.get_kpis()

col1, col2 = st.columns(2)

with col1:

    render_kpi(

        "Procesos",

        kpis["procesos"],

        "⚖️",

        "#2563EB"

    )

with col2:

    render_kpi(

        "Publicaciones",

        kpis["publicaciones"],

        "📰",

        "#16A34A"

    )

st.write("")

st.write("Bienvenido al Centro de Operaciones Jurídicas.")

summary = executive.get_summary()

render_executive_summary(summary)

priority = executive.get_priority()

action_service = ActionService()

actions = action_service.get_actions()

left, right = st.columns([1, 1])

with left:

    render_priority_card(priority)

with right:

    render_actions(actions)

st.divider()

events = executive.get_recent_events()

render_timeline(events)
