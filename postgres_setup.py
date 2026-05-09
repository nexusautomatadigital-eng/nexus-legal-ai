import psycopg2

try:

    conn = psycopg2.connect(

        host="aws-1-us-west-1.pooler.supabase.com",

        database="postgres",

        user="postgres.xnreltwbbledefdygwmc",

        password="n%&GvQFDyL-!2+8",

        port="5432",

        sslmode="require"

    )

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS procesos (

        id SERIAL PRIMARY KEY,

        cliente TEXT,
        email TEXT,
        whatsapp TEXT,
        plan TEXT,

        numero_proceso TEXT,
        fecha_actuacion TEXT,
        juzgado TEXT,
        demandante TEXT,
        demandado TEXT,

        fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    print("✅ Tabla PostgreSQL creada")

    conn.close()

except Exception as e:

    print("❌ Error:", e)