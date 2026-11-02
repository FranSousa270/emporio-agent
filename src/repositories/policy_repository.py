import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]

POLICIES_PATH = PROJECT_ROOT / "data" / "policies" / "policies.json"


def load_policies() -> dict[str, Any]:
    if not POLICIES_PATH.exists():
        raise FileNotFoundError(f"Arquivo de políticas não encontrado: {POLICIES_PATH}")

    try:
        with POLICIES_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError("O arquivo de políticas contém JSON inválido.") from error

    if not isinstance(data, dict):
        raise ValueError("A estrutura das políticas deve ser um objeto JSON.")

    document = data.get("document")
    policies = data.get("policies")

    if not isinstance(document, dict):
        raise ValueError("O arquivo deve conter o objeto 'document'.")

    if not isinstance(policies, list):
        raise ValueError("O arquivo deve conter a lista 'policies'.")

    policy_ids: set[str] = set()

    for index, policy in enumerate(policies):
        if not isinstance(policy, dict):
            raise ValueError(f"A política na posição {index} deve ser um objeto.")

        policy_id = policy.get("id")
        title = policy.get("title")
        rules = policy.get("rules")

        if not isinstance(policy_id, str) or not policy_id.strip():
            raise ValueError(f"A política na posição {index} possui um ID inválido.")

        if policy_id in policy_ids:
            raise ValueError(f"ID de política duplicado: {policy_id}")

        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"A política '{policy_id}' possui um título inválido.")

        if not isinstance(rules, list) or not all(
            isinstance(rule, str) and rule.strip() for rule in rules
        ):
            raise ValueError(f"A política '{policy_id}' possui regras inválidas.")

        policy_ids.add(policy_id)

    return data
