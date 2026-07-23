import streamlit as st
import requests
from dashboard.services.proceso_service import ProcesoService


def render_onboarding(
    conn,
    cursor,
    cliente_logueado,
    email_cliente,
    whatsapp_cliente,
    plan_cliente,
    total_procesos,
    limite_plan,
):
    """
    Flujo de onboarding del primer proceso.

    (Implementación temporal.
    En el siguiente paso moveremos el código.)
    """
  
# =========================================
# AGREGAR PROCESO
# =========================================
    
    st.subheader("➕ Agregar Proceso")

    with st.form(
        "nuevo_proceso",
        clear_on_submit=True
):

        numero_proceso = st.text_input(
        
            "Número proceso judicial"
        )

        numero_proceso = numero_proceso.strip()

        agregar = st.form_submit_button(
            "Agregar Proceso"
        )

        if agregar:

            if not numero_proceso.strip():

                st.warning(
                    "⚠️ Ingrese un proceso"
                )

            else:

                if total_procesos >= limite_plan:

                    st.error(
                        f"❌ Tu plan {plan_cliente} permite máximo {limite_plan} procesos"
                    )

                else:

                    service = ProcesoService()

                    resultado = service.agregar_proceso(
                        cliente_logueado,
                        numero_proceso,                  
                    )
                                       
                    if not resultado["ok"]:                      
                        st.warning(resultado["mensaje"])
                        st.stop()
                        

                    else:

                        st.session_state.primer_proceso = True

                                                
                        placeholder = st.empty()

                        with placeholder.container():

                            st.info("""
                        🤖 Nexus está analizando tu proceso.

                        ⏳ Consultando Rama Judicial

                        ⏳ Consultando Publicaciones Procesales

                        ⏳ Consultando SAMAI

                        ⏳ Generando historial procesal

                        Tiempo estimado: 30 a 60 segundos.
                        """)

                        # ======================================
                        # DISPARAR NEXUS ENGINE INMEDIATO
                        # ======================================

                        try:

                            print("🚀 INICIANDO DISPATCH")

                            github_token = st.secrets["GITHUB_TOKEN"]
                            print("TOKEN OK")

                            github_user = st.secrets["GITHUB_USER"]
                            print("USER OK")

                            github_repo = st.secrets["GITHUB_REPO"]
                            print("REPO OK")

                        except Exception as e:

                            print("ERROR:", e)

                        try:

                            print("🚀 INICIANDO DISPATCH GITHUB")

                            github_token = st.secrets["GITHUB_TOKEN"]

                            github_user = st.secrets["GITHUB_USER"]

                            github_repo = st.secrets["GITHUB_REPO"]

                            print("USER:", github_user)

                            print("REPO:", github_repo)

                            url = f"https://api.github.com/repos/{github_user}/{github_repo}/actions/workflows/nexus_engine.yml/dispatches"

                            headers = {

                                "Authorization": f"Bearer {github_token}",

                                "Accept": "application/vnd.github+json"

                            }

                            data = {

                                "ref": "main"

                            }

                            response = requests.post(

                                url,

                                headers=headers,

                                json=data

                            )

                            if response.status_code == 204:

                                st.success(
                                    "🚀 Nexus Engine iniciado correctamente"
                                )

                                st.info("""
                                🔎 Nexus está procesando el expediente.

                                La consulta puede tardar entre 30 y 90 segundos.

                                Puede seguir navegando mientras Nexus recopila información de:

                                ✓ Rama Judicial

                                ✓ Publicaciones Procesales

                                ✓ SAMAI

                                ✓ Historial Procesal
                                """)

                            else:

                                st.error(
                                    f"Error GitHub: {response.status_code}"
                                )

                            print("GitHub Status:", response.status_code)

                            print("GitHub Response:", response.text)

                        except Exception as e:

                            print("ERROR GITHUB:", e)

                            st.error(
                                f"Error GitHub Actions: {e}"
                            )
                                       