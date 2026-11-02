import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4


class ComplaintTools:
    REQUIRED_FIELDS = (
        "customer_name",
        "phone",
        "email",
        "product_name",
        "purchase_date",
        "description",
    )

    def __init__(self, file_path: Path | None = None):
        project_root = Path(__file__).resolve().parents[2]
        self._file_path = file_path or project_root / "data" / "complaints.json"

    def register_customer_complaint(self, arguments: dict) -> dict:
        if not isinstance(arguments, dict):
            return {
                "success": False,
                "error": "Os dados da reclamação são inválidos.",
            }

        complaint_data = {}

        for field in self.REQUIRED_FIELDS:
            value = arguments.get(field)

            if not isinstance(value, str) or not value.strip():
                return {
                    "success": False,
                    "error": "Preencha todos os dados obrigatórios da reclamação.",
                }

            complaint_data[field] = value.strip()

        order_number = arguments.get("order_number", "")

        if not isinstance(order_number, str):
            return {
                "success": False,
                "error": "O número do pedido informado é inválido.",
            }

        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

            if self._file_path.exists():
                with self._file_path.open("r", encoding="utf-8") as file:
                    complaints = json.load(file)

                if not isinstance(complaints, list):
                    raise ValueError("Formato inválido do arquivo de reclamações.")
            else:
                complaints = []

            now = datetime.now().astimezone()
            protocol = f"REC-{now:%Y%m%d}-{uuid4().hex[:6].upper()}"

            complaint = {
                "protocol": protocol,
                **complaint_data,
                "order_number": order_number.strip(),
                "status": "pending_review",
                "created_at": now.isoformat(timespec="seconds"),
            }

            complaints.append(complaint)

            with self._file_path.open("w", encoding="utf-8") as file:
                json.dump(complaints, file, ensure_ascii=False, indent=2)

            return {
                "success": True,
                "protocol": protocol,
                "status": "pending_review",
                "message": (
                    "A reclamação foi registrada localmente e aguarda "
                    "análise da equipe responsável. Nenhuma notificação "
                    "externa foi enviada."
                ),
            }

        except (OSError, json.JSONDecodeError, ValueError):
            return {
                "success": False,
                "error": (
                    "Não foi possível salvar a reclamação no momento. "
                    "Nenhum protocolo deve ser confirmado ao cliente."
                ),
            }
