import streamlit as st
import psycopg2
import pandas as pd


# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Nexus Admin",
    layout="wide"
)

# ==========================================
# DB
# ==========================================

# =========================================
# CONEXIÓN SUPABASE
# =========================================

DB_HOST = st.secrets["DB_HOST"]
DB_NAME = st.secrets["DB_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_PORT = st.secrets["DB_PORT"]

try:

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        sslmode="require"
    )

    print("✅ CONEXIÓN EXITOSA")

except Exception as e:

    st.error(f"ERROR CONEXIÓN: {e}")
    st.stop()

# ==========================================
# LOGIN
# ==========================================

st.title("⚖️ Nexus Admin")

usuario = st.text_input("Usuario")
password = st.text_input("Password", type="password")

if st.button("Ingresar"):

    query = """

    SELECT *

    FROM admins

    WHERE usuario = %s
    AND password = %s

    """

    df_admin = pd.read_sql(
        query,
        conn,
        params=(usuario, password)
    )

    if len(df_admin) > 0:

        st.success("Bienvenido Admin")

        # =====================================
        # CLIENTES
        # =====================================

        df_clientes = pd.read_sql("""

        SELECT *

        FROM clientes

        ORDER BY id DESC

        """, conn)

        st.subheader("Clientes Nexus")

        for _, row in df_clientes.iterrows():

            with st.container(border=True):

                col1, col2, col3 = st.columns([3,2,2])

                with col1:

                    st.write(f"👤 Cliente: {row['nombre']}")
                    st.write(f"📧 {row['email']}")
                    st.write(f"📲 {row['whatsapp']}")
                    st.write(f"💎 Plan actual: {row['plan']}")

                with col2:

                    nuevo_plan = st.selectbox(

                        f"Plan {row['id']}",
                        ["FREE", "BASICO", "PREMIUM", "GOLD"]

                    )

                    if st.button(f"Actualizar Plan {row['id']}"):

                        cursor = conn.cursor()

                        cursor.execute("""
                                       
                        UPDATE clientes
                                       
                        SET plan = %s
                                       
                        WHERE id = %s

                        """, (nuevo_plan, row["id"]))

                        conn.commit()

                        st.success("✅ Plan actualizado")

                    with col3:

                        if st.button(f"❌ Eliminar {row['id']}"):

                            cursor = conn.cursor()

                            cursor.execute("""

                            DELETE FROM clientes

                            WHERE id = %s

                            """, (row["id"],))

                            conn.commit()

                            st.success("✅ Cliente eliminado")

    else:

        st.error("Credenciales incorrectas")