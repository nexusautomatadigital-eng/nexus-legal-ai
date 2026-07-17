from domain.proceso_service import ProcesoService

service = ProcesoService()

procesos = service.get_procesos(cliente_id=83)

print()
print("=" * 70)
print("TOTAL:", len(procesos))
print("=" * 70)

for proceso in procesos:
    print(f"Número: {proceso.numero}")
    print(f"Cliente: {proceso.cliente}")
    print(f"Plan: {proceso.plan}")
    print(f"Health Score: {proceso.health.score}")
    print(f"Estado: {proceso.health.estado}")
    print(f"Publicaciones: {proceso.actividad.publicaciones}")
    print(f"Actuaciones: {proceso.actividad.actuaciones}")
    print(f"Documentos: {proceso.actividad.documentos}")
    print("-" * 70)