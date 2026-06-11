import hashlib


# ==========================================
# HASH GENERAL
# ==========================================

def generar_hash(texto):

    return hashlib.sha256(

        texto.encode("utf-8")

    ).hexdigest()


# ==========================================
# HASH PROCESO
# ==========================================

def generar_hash_proceso(payload):

    texto = f"""

    {payload.get("numero_proceso")}
    {payload.get("jurisdiccion")}
    {payload.get("fuente")}

    """

    return generar_hash(texto)


# ==========================================
# HASH ACTUACION
# ==========================================

def generar_hash_actuacion(
    numero_proceso,
    actuacion
):

    texto = f"""

    {numero_proceso}
    {actuacion.get("fecha_actuacion")}
    {actuacion.get("tipo_actuacion")}
    {actuacion.get("detalle")}

    """

    return generar_hash(texto)


# ==========================================
# HASH DOCUMENTO
# ==========================================

def generar_hash_documento(
    numero_proceso,
    documento
):

    texto = f"""

    {numero_proceso}
    {documento.get("nombre")}
    {documento.get("url")}

    """

    return generar_hash(texto)

