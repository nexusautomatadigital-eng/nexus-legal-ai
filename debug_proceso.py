from domain.proceso_service import ProcesoService

service = ProcesoService()

df = service.get_procesos_dataframe(83)

print(df)
print()
print(df.columns)
print()
print(df.dtypes)
print()
print(df.empty)