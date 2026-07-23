from domain.executive_service import ExecutiveService

service = ExecutiveService(cliente_id=83)

brief = service.get_executive_brief()

print("=" * 70)

print("EXECUTIVE BRIEF")

print("=" * 70)

for k, v in brief.items():

    print(f"{k}: {v}")