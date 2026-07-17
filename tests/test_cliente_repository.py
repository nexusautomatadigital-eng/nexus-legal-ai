from domain.repositories.cliente_repository import ClienteRepository

repo = ClienteRepository()

cliente = repo.get_by_usuario("diego")

print()
print("=" * 70)
print(cliente)
print("=" * 70)