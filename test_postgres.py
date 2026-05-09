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

    print("✅ Conectado PostgreSQL")

    conn.close()

except Exception as e:

    print("❌ Error:", e)