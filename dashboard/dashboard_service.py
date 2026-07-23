from services.db import get_connection


class DashboardService:

    def __init__(self):

        self.conn = get_connection()

    def get_total_procesos(self):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM procesos_v2

        """)

        total = cursor.fetchone()[0]

        cursor.close()

        return total

    def get_total_clientes(self):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM clientes

        """)

        total = cursor.fetchone()[0]

        cursor.close()

        return total