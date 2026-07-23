from domain.proceso_service import ProcesoService

service = ProcesoService()

procesos = service.get_procesos(cliente_id=83)

print()
print("=" * 70)
print(f"TOTAL: {len(procesos)}")
print("=" * 70)

for proceso in procesos:

    print(f"ID: {proceso.id}")
    print(f"Número: {proceso.numero_proceso}")
    print(f"Despacho: {proceso.despacho}")
    print(f"Especialidad: {proceso.especialidad}")
    print(f"Estado: {proceso.estado_proceso}")
    print(f"Fuente: {proceso.fuente}")
    print(f"Activo: {proceso.activo}")

    print("-" * 70)