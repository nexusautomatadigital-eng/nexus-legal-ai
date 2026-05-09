import pandas as pd
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# 1. Leer clientes
df_clientes = pd.read_csv("clientes_procesos.csv")

# 2. Función simulada
def consultar_proceso(numero):
    import random

    estados = [
        "Sin cambios",
        "En trámite",
        "Nueva actuación"
    ]

    return {
        "proceso": numero,
        "estado": random.choice(estados),
        "fecha": "2026-05-06"
    }

# 3. Función para enviar email
def enviar_alerta(cliente, proceso, estado, email):

    configuration = sib_api_v3_sdk.Configuration()

    # 👇 PEGA AQUÍ TU API KEY DE BREVO
    configuration.api_key['api-key'] = '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'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    asunto = f"Cambio en proceso {proceso}"

    html_content = f"""
    <html>
    <body>
        <h2>🚨 Cambio detectado</h2>

        <p>Hola {cliente}</p>

        <p>
        Tu proceso <b>{proceso}</b>
        tiene un nuevo estado:
        </p>

        <h3>{estado}</h3>

    </body>
    </html>
    """

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        sender={
            "email": "nexusautomata.digital@gmail.com",
            "name": "Nexus Automata"
        },
        subject=asunto,
        html_content=html_content
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        print(f"📧 Email enviado a {email}")

    except ApiException as e:
        print("❌ Error enviando email:", e)

# 4. Consultar todos los procesos
resultados = []

for _, row in df_clientes.iterrows():

    data = consultar_proceso(row['proceso'])

    data['cliente'] = row['cliente']
    data['email'] = row['email']

    resultados.append(data)

df_nuevo = pd.DataFrame(resultados)

# 5. Comparar con histórico
if os.path.exists("resultado_procesos.csv"):

    df_anterior = pd.read_csv("resultado_procesos.csv")

    df_merge = df_nuevo.merge(
        df_anterior,
        on="proceso",
        how="left",
        suffixes=("_nuevo", "_anterior")
    )

    cambios = df_merge[
        df_merge["estado_nuevo"] != df_merge["estado_anterior"]
    ]

    if not cambios.empty:

        print("🚨 CAMBIOS DETECTADOS:")
        print(
            cambios[
                ["cliente_nuevo", "proceso", "estado_nuevo"]
            ]
        )

        for _, row in cambios.iterrows():

            enviar_alerta(
                row['cliente_nuevo'],
                row['proceso'],
                row['estado_nuevo'],
                row['email_nuevo']
            )

        cambios.to_csv("alertas.csv", index=False)

    else:
        print("Sin cambios")

else:
    print("Primera ejecución, no hay comparación")

# 6. Guardar nuevo estado
df_nuevo.to_csv("resultado_procesos.csv", index=False)

print("✅ Proceso terminado")