from core.session import SessionService


class AppController:

    def __init__(self):

        self.context = SessionService.get_context()

    def is_logged(self):

        return self.context.logueado

    def current_user(self):

        return self.context