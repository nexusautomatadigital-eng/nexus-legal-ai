from services.db import get_connection


class BaseRepository:

    def __init__(self):

        self.conn = get_connection()