from domain.auth_service import AuthService

service = AuthService()

cliente = service.login("diego")

print()
print("=" * 70)

if cliente:
    print("Login OK")
    print(cliente)
    print(cliente.nombre)
    print(cliente.email)
    print(cliente.plan)
else:
    print("Usuario no encontrado")

print("=" * 70)