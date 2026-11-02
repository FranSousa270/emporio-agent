import json
import pytest
from src.tools.complaint_tools import ComplaintTools


@pytest.fixture
def complaint_data():
    return {
        "customer_name": "Teste Júnior da Silva",
        "phone": "21-99900-2120",
        "email": "teste@gmail.com",
        "product_name": "Yamaha C40",
        "purchase_date": "13/10/2026",
        "description": "O instrumento perde a afinação pouco tempo após ser afinado.",
    }


def test_register_customer_complaint_saves_record(
    tmp_path,
    complaint_data,
):
    file_path = tmp_path / "complaints.json"
    tools = ComplaintTools(file_path=file_path)

    result = tools.register_customer_complaint(complaint_data)

    assert result["success"] is True
    assert result["protocol"].startswith("REC-")
    assert result["status"] == "pending_review"

    saved_complaints = json.loads(file_path.read_text(encoding="utf-8"))

    assert len(saved_complaints) == 1
    assert saved_complaints[0]["protocol"] == result["protocol"]
    assert saved_complaints[0]["customer_name"] == complaint_data["customer_name"]
    assert saved_complaints[0]["product_name"] == complaint_data["product_name"]
    assert saved_complaints[0]["status"] == "pending_review"
    assert saved_complaints[0]["order_number"] == ""


def test_register_customer_complaint_preserves_existing_records(
    tmp_path,
    complaint_data,
):
    file_path = tmp_path / "complaints.json"
    tools = ComplaintTools(file_path=file_path)

    first_result = tools.register_customer_complaint(complaint_data)
    second_result = tools.register_customer_complaint(complaint_data)

    saved_complaints = json.loads(file_path.read_text(encoding="utf-8"))

    assert first_result["success"] is True
    assert second_result["success"] is True
    assert len(saved_complaints) == 2
    assert first_result["protocol"] != second_result["protocol"]


def test_register_customer_complaint_rejects_missing_required_field(
    tmp_path,
    complaint_data,
):
    file_path = tmp_path / "complaints.json"
    tools = ComplaintTools(file_path=file_path)
    complaint_data.pop("email")

    result = tools.register_customer_complaint(complaint_data)

    assert result["success"] is False
    assert not file_path.exists()


def test_register_customer_complaint_rejects_invalid_arguments(tmp_path):
    tools = ComplaintTools(file_path=tmp_path / "complaints.json")

    result = tools.register_customer_complaint(None)

    assert result["success"] is False


def test_register_customer_complaint_handles_invalid_existing_file(
    tmp_path,
    complaint_data,
):
    file_path = tmp_path / "complaints.json"
    file_path.write_text("{json inválido", encoding="utf-8")
    tools = ComplaintTools(file_path=file_path)

    result = tools.register_customer_complaint(complaint_data)

    assert result["success"] is False
    assert "protocol" not in result
