from domain.priority_service import PriorityService

service = PriorityService()

prioridades = service.get_prioridades()

print()

print("=" * 60)
print("TOTAL PRIORIDADES:", len(prioridades))
print("=" * 60)

for prioridad in prioridades:

    print()

    print("Proceso:", prioridad.numero_proceso)

    print("Cliente:", prioridad.cliente)

    print("Evento:", prioridad.evento)

    print("Impacto:", prioridad.impacto)

    print("Score:", prioridad.score)

    print("Acción:", prioridad.accion)

    print("-" * 60)