import os

import psycopg2

import streamlit as st

from pathlib import Path

from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)


def get_connection():

    try:

        host = st.secrets["SUPABASE_HOST"]
        db = st.secrets["SUPABASE_DB"]
        user = st.secrets["SUPABASE_USER"]
        password = st.secrets["SUPABASE_PASSWORD"]
        port = st.secrets["SUPABASE_PORT"]

        print("🔐 USANDO STREAMLIT SECRETS")

    except Exception:

        host = os.getenv("DB_HOST")
        db = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        port = os.getenv("DB_PORT")

        print("🔐 USANDO VARIABLES")

    return psycopg2.connect(

        host=host,

        database=db,

        user=user,

        password=password,

        port=port,

        sslmode="require"

    )