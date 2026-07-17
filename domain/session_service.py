from services.db import get_connection
from core.session import UserSession


class SessionService:

    def __init__(self):

        self.conn = get_connection()

    def get_session(self, email):

        pass