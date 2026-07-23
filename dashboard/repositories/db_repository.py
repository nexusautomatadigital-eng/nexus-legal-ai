from services.db import get_connection


class DBRepository:
    """
    Repositorio base para PostgreSQL.
    Todos los repositorios heredan de esta clase.
    """

    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()