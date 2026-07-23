from domain.executive_service import ExecutiveService


def test_executive_brief():

    service = ExecutiveService(cliente_id=1)

    data = service.get_executive_brief()

    assert data is not None

    assert "summary" in data

    assert "priority" in data

    assert "critical" in data

    assert "stable" in data