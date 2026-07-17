import os
import psycopg2
import json
import hashlib

print("🚨 DB.PY VERSION 11 JUNIO 2026")
print(__file__)

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from services.hash_service import (
    generar_hash_proceso,
    generar_hash_actuacion,
    generar_hash_documento
)

import streamlit as st
import psycopg2

env_path = Path(__file__).resolve().parent.parent / '.env'

load_dotenv(dotenv_path=env_path)


# ==========================================

# GET CONNECTION

# ==========================================

from database.connection import get_connection

    

# ==========================================
# SAVE PROCESO V2
# ==========================================

def save_proceso_v2(payload):

    print("🔥🔥🔥 DB SAVE_PROCESO_V2 EJECUTANDO")

    print("DEBUG 1")

    conn = get_connection()

    print("DEBUG 2")

    cur = conn.cursor()

    print("DEBUG 3")

    try:

        # ==========================================
        # VALIDAR SI YA EXISTE
        # ==========================================

        numero_proceso = str(
            payload.get("numero_proceso")
        ).strip()

        hash_proceso = generar_hash_proceso(
            payload
        )

        print("🔥 HASH INPUTS:")
        print(payload.get("numero_proceso"))
        print(payload.get("jurisdiccion"))
        print(payload.get("fuente"))

        print("🔥 HASH GENERADO:")
        print(hash_proceso)

        print("DEBUG HASH_PROCESO:", hash_proceso)

        print("DEBUG INSERT VALUES:")
        print(payload.get("numero_proceso"))
        print(payload.get("fuente"))
        print(hash_proceso)

        print(payload)   
        
        cur.execute("""
                    
            select
                id,
                numero_proceso,
                hash_consulta,
                hash_proceso

            from procesos_v2

            where hash_proceso = %s
            
            limit 1

        """, (

            hash_proceso,
            

        ))

        existente = cur.fetchone()

        print("DEBUG EXISTENTE:", existente)
        
        if existente:

            print("⚠️ PROCESO YA EXISTE")

            return existente[0]

        # ==========================================
        # INSERT PARAMS
        # ==========================================

        print("🔥 INSERT PARAMS:")

        params = (

            payload.get("cliente_id"),
            payload.get("numero_proceso"),
            payload.get("fuente"),   
            payload.get("jurisdiccion"),
            payload.get("especialidad"),
            payload.get("despacho"),
            payload.get(
                "estado_proceso",
                "ACTIVO"
            ),
            payload.get(
                "fecha_consulta"
            ) or payload.get(
                "metadata",
                {}
            ).get(
                "fecha_consulta"
            ),
            
            payload.get(
                "hash_consulta",
                hash_proceso[:32]
            ),

            hash_proceso,

            json.dumps(
                payload.get(
                    "metadata",
                    {}
                )
            )

        )

        # ==========================================
        # INSERT PROCESO
        # ==========================================

        cur.execute("""

            insert into procesos_v2 (

                cliente_id,
                numero_proceso,
                fuente,
                jurisdiccion,
                especialidad,
                despacho,
                estado_proceso,
                ultima_revision,
                hash_consulta,
                hash_proceso,
                metadata

            )

            values (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s

            )

            returning id

        """, params)

        proceso_id = cur.fetchone()[0]

        conn.commit()

        print("✅ PROCESO_V2 GUARDADO")

        print(f"✅ PROCESO ID V2: {proceso_id}")

        return proceso_id

    except Exception as e:

        conn.rollback()

        print(f"❌ ERROR PROCESO_V2: {e}")

        # ==========================================
        # RECUPERAR PROCESO EXISTENTE
        # ==========================================

        try:

            recovery_cur = conn.cursor()

            recovery_cur.execute("""

                select id

                from procesos_v2

                where numero_proceso = %s

                limit 1

            """, (

                numero_proceso,

            ))

            existente = recovery_cur.fetchone()

            print("DEBUG RECOVERY:", existente)

            if existente:

                print("♻️ RECUPERANDO PROCESO EXISTENTE")

                return existente[0]

        except Exception as e2:

            print(f"❌ ERROR RECOVERY: {e2}")

        return None
      

    finally:

        cur.close()

        conn.close()


# ==========================================
# SAVE PUBLICACION V2
# ==========================================

def save_publicacion_v2(

    proceso_id,
    publicacion

):

    conn = get_connection()

    cur = conn.cursor()

    try:

        metadata = publicacion.get(

            "metadata",
               
            {}

        )

        article_id = str(

            metadata.get(

                "article_id"

            )

        )

        fecha_publicacion = metadata.get(
            "fecha_publicacion"
        )

        fecha_estado = metadata.get(
            "fecha_estado"
        )

        url_publicacion = metadata.get(
            "url_publicacion"
        )        

        hash_publicacion = hashlib.sha256(

            article_id.encode()

        ).hexdigest()

        # -----------------------------
        # Ya existe
        # -----------------------------

        cur.execute("""

            select id

            from publicaciones_v2

            where hash_publicacion=%s

            limit 1

        """,(

            hash_publicacion,

        ))

        existe = cur.fetchone()

        if existe:

            print("⚠️ PUBLICACION YA EXISTE")

            return existe[0]
        

        # ==========================================
        # EXTRAER METADATA
        # ==========================================
        
        print("\n===== DEBUG PUBLICACION V2 =====")

        print("ARTICLE:", article_id)

        print("FECHA PUBLICACION:", fecha_publicacion)

        print("FECHA ESTADO:", fecha_estado)

        print("URL:", url_publicacion)

        print("HASH:", hash_publicacion)

        print("PDFS:", len(publicacion.get("documentos", [])))

        # -----------------------------
        # Insert
        # -----------------------------

        cur.execute("""

        insert into publicaciones_v2(

            proceso_id,
            article_id,
            estado_numero,
            fecha_publicacion,
            fecha_estado,
            despacho,
            entidad,
            especialidad,
            municipio,
            departamento,
            resumen,
            url_publicacion,
            tiene_documentos,
            cantidad_documentos,
            metadata,
            hash_publicacion

        )

        values(

            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s

        )

        returning id

        """,(

            proceso_id,

            article_id,

            None,                       # estado_numero (por ahora)

            fecha_publicacion,

            fecha_estado,

            publicacion.get("despacho"),

            None,                       # entidad (por ahora)

            publicacion.get("especialidad"),

            None,                       # municipio (por ahora)

            None,                       # departamento (por ahora)

            publicacion["actuaciones"][0]["detalle"],

            url_publicacion,

            len(publicacion.get("documentos", [])) > 0,

            len(publicacion.get("documentos", [])),

            json.dumps(publicacion),

            hash_publicacion

        ))

        publicacion_id = cur.fetchone()[0]

        conn.commit()

        print("✅ PUBLICACION V2 GUARDADA")

        return publicacion_id

    except Exception as e:

        conn.rollback()

        print(e)

        return None

    finally:

        cur.close()
        conn.close()


# ==========================================
# SAVE ACTUACIONES V2
# ==========================================

def save_actuaciones_v2(
    proceso_id,
    numero_proceso,
    actuaciones,
    fuente="SAMAI"
):

    conn = get_connection()

    cur = conn.cursor()

    try:

        for act in actuaciones:

            fecha_actuacion = None
            fecha_registro = None

            hash_actuacion = generar_hash_actuacion(
                numero_proceso,
                act
            )

            print("HASH ACTUACION:", hash_actuacion)

            try:

                fecha_actuacion = datetime.strptime(
                    act.get("fecha_actuacion"),
                    "%d/%m/%Y"
                ).date()

            except:
                
                try:

                    fecha_actuacion = datetime.strptime(
                        act.get("fecha_actuacion"),
                        "%Y-%m-%d"
                    ).date()

                except:

                    pass   

            try:

                fecha_registro = datetime.strptime(
                    act.get("fecha_registro"),
                    "%d/%m/%Y"
                ).date()

            except:
                pass

            cur.execute("""

                insert into actuaciones_v2 (

                    proceso_id,
                    fuente,
                    hash_actuacion,
                    tipo_actuacion,
                    fecha_actuacion,
                    fecha_registro,
                    detalle,
                    estado,
                    metadata

                )

                values (

                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s

                )
                
                on conflict (hash_actuacion)
                
                do nothing

            """, (

                proceso_id,
                fuente,
                hash_actuacion,
                act.get("tipo_actuacion"),
                fecha_actuacion,
                fecha_registro,
                act.get("detalle"),
                act.get("estado"),
                json.dumps(act)

            ))

        conn.commit()

        cur.execute("""

            select
                numero_proceso,
                hash_consulta,
                hash_proceso

            from procesos_v2

            where id = %s

        """, (

            proceso_id,

        ))

        resultado = cur.fetchone()

        print("🔥 DB FETCH:")
        print(resultado)

        print("✅ ACTUACIONES_V2 GUARDADAS")

    except Exception as e:

        print(f"❌ ERROR ACTUACIONES_V2: {e}")

        conn.rollback()

    finally:

        cur.close()

        conn.close()


# ==========================================
# SAVE DOCUMENTOS V2
# ==========================================

def save_documentos_v2(
    proceso_id,
    numero_proceso,
    documentos,
    fuente="SAMAI"
):
    print("🔥 SAVE DOCUMENTOS V2")

    print("DOCUMENTOS RECIBIDOS:")

    print(documentos)

    if not documentos:      

        print("⚠️ DOCUMENTOS VACIOS")
        return
    
    print("TOTAL DOCUMENTOS:", len(documentos))

    conn = get_connection()

    cur = conn.cursor()

    try:

        for doc in documentos:

            print("DEBUG DOCUMENTO:")
            print(doc)

            hash_documento = generar_hash_documento(
                numero_proceso,
                doc
            )

            print("HASH DOCUMENTO:", hash_documento)

            cur.execute("""

                insert into documentos_v2 (

                    proceso_id,
                    fuente,
                    nombre_documento,
                    tipo_documento,
                    url_publica,
                    hash_documento,
                    publico,
                    metadata

                )

                values (

                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s

                )
                        
                on conflict (hash_documento)
                do nothing

            """, (

                proceso_id,
                fuente,
                doc.get("nombre"),
                doc.get("tipo_documento"),
                doc.get("url_publica"),
                hash_documento,
                doc.get("publico"),
                json.dumps(doc)

            ))
            
        conn.commit()

        print("✅ DOCUMENTOS_V2 GUARDADOS")

    except Exception as e:

        conn.rollback()

        print(f"❌ ERROR DOCUMENTOS_V2: {e}")

    finally:

        cur.close()

        conn.close()

# ==========================================
# SAVE VIGILANCIA
# ==========================================

def save_vigilancia(

    cliente_id,
    proceso_id

):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select id

            from vigilancias

            where cliente_id = %s

            and proceso_id = %s

            limit 1

        """, (

            cliente_id,
            proceso_id

        ))

        existe = cur.fetchone()

        print("DEBUG VIGILANCIA:", existe)

        if existe:

            print("⚠️ VIGILANCIA YA EXISTE")

            return existe[0]

        cur.execute("""

            insert into vigilancias (

                cliente_id,
                proceso_id

            )

            values (

                %s,
                %s

            )

            returning id

        """, (

            cliente_id,
            proceso_id

        ))

        vigilancia_id = cur.fetchone()[0]

        conn.commit()

        print("✅ VIGILANCIA GUARDADA")

        print(vigilancia_id)

        return vigilancia_id

    except Exception as e:

        conn.rollback()

        print(f"❌ ERROR VIGILANCIA: {e}")

        return None

    finally:

        cur.close()

        conn.close()


# ==========================================
# GET CLIENTE PROCESO
# ==========================================

def get_cliente_proceso(

   numero_proceso_padre

):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            SELECT

                c.id,
                c.nombre,
                c.email,
                c.whatsapp,
                c.plan

            FROM procesos p

            JOIN clientes c

                ON c.nombre = p.cliente

            WHERE p.numero_proceso = %s

            LIMIT 1

        """, (

            numero_proceso_padre,

        ))

        resultado = cur.fetchone()

        print("👤 CLIENTE PROCESO:")

        print(resultado)

        return resultado

    except Exception as e:

        print(f"❌ ERROR CLIENTE PROCESO: {e}")

        return None

    finally:

        cur.close()

        conn.close()

# ==========================================
# GET PROCESO PADRE V2
# ==========================================

def get_proceso_padre(

    numero_proceso

):  
    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            SELECT id

            FROM procesos

            WHERE numero_proceso = %s

            LIMIT 1

        """, (

            numero_proceso,

        ))

        resultado = cur.fetchone()

        print("📌 PROCESO PADRE:")

        print(resultado)

        return resultado

    except Exception as e:

        print(f"❌ ERROR PROCESO PADRE: {e}")

        return None

    finally:

        cur.close()

        conn.close()

# ==========================================
# GET PROCESO V2
# ==========================================

def get_proceso_v2(

    numero_proceso

):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            SELECT id

            FROM procesos_v2

            WHERE numero_proceso = %s

            LIMIT 1

        """, (

            numero_proceso,

        ))

        resultado = cur.fetchone()

        print("📌 PROCESO V2:")

        print(resultado)

        return resultado

    except Exception as e:

        print(f"❌ ERROR PROCESO V2: {e}")

        return None

    finally:

        cur.close()
        conn.close()


# ==========================================
# GET VIGILANCIAS CLIENTE
# ==========================================

def get_vigilancias_cliente(

    cliente_id

):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select

                v.id,
                v.estado,

                p.numero_proceso,
                p.fuente,
                p.especialidad,
                p.despacho,
                p.ultima_actuacion,
                p.fecha_ultima_actuacion,
                    
                v.ultima_revision

            from vigilancias v

            join procesos_v2 p

                on p.id = v.proceso_id

            where v.cliente_id = %s

            order by v.created_at desc

        """, (

            cliente_id,

        ))

        resultado = cur.fetchall()

        print("🔥 VIGILANCIAS ENCONTRADAS")

        print(resultado)

        return resultado

    except Exception as e:

        print(
            f"❌ ERROR GET_VIGILANCIAS: {e}"
        )

        return []

    finally:

        cur.close()
        conn.close()

# ==========================================
# KPI VIGILANCIAS
# ==========================================

def get_total_vigilancias():

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select count(*)

            from vigilancias

            where estado = 'ACTIVA'

        """)

        return cur.fetchone()[0]

    finally:

        cur.close()
        conn.close()

# ==========================================
# KPI ALERTAS
# ==========================================

def get_total_alertas():

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select count(*)

            from alertas_v2

        """)

        return cur.fetchone()[0]

    finally:

        cur.close()
        conn.close()

# ==========================================
# KPI ACTUACIONES
# ==========================================

def get_total_actuaciones():

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select count(*)

            from actuaciones_v2

        """)

        return cur.fetchone()[0]

    finally:

        cur.close()
        conn.close()

# ==========================================
# KPI DOCUMENTOS
# ==========================================

def get_total_documentos():

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select count(*)

            from documentos_v2

        """)

        return cur.fetchone()[0]

    finally:

        cur.close()
        conn.close()

# ==========================================
# KPI DASHBOARD
# ==========================================

def get_total_vigilancias():

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute("""

            select count(*)

            from vigilancias

            where estado = 'ACTIVA'

        """)

        return cur.fetchone()[0]

    finally:

        cur.close()
        conn.close()