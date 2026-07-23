from core.session import SessionService


def bootstrap_dev_session():

    context = SessionService.get_context()

    if context.logueado:
        return context

    context.cliente_id = 83
    context.nombre = "Diego Alba"
    context.usuario = "diego"
    context.email = "demo@nexus.ai"
    context.plan = "FREE"
    context.logueado = True

    return context