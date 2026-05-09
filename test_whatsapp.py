from twilio.rest import Client

# ======================================
# CREDENCIALES
# ======================================

account_sid = "ACc0d8988b16c736aeb6faa8731065d7fd"

auth_token = "9bc3b5b6e94027dcd7dad5ba692917f9"

client = Client(
    account_sid,
    auth_token
)

# ======================================
# ENVIAR WHATSAPP
# ======================================

message = client.messages.create(

    from_='whatsapp:+14155238886',

    body='🚨 Nexus Legal AI: nueva actuación judicial detectada',

    to='whatsapp:+573138937617'

)

print("✅ WhatsApp enviado")