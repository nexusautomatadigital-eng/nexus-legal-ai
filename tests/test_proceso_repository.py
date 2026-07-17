from domain.repositories.proceso_repository import ProcesoRepository

repo = ProcesoRepository()

procesos = repo.get_by_cliente(83)

print()

print("=" * 70)

print("TOTAL:", len(procesos))

print("=" * 70)

for p in procesos:

    print(p)