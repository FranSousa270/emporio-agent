from typing import Any

from src.services.policy_service import PolicyService


class PolicyTools:
    def __init__(self, policy_service: PolicyService | None = None):
        self._policy_service = policy_service or PolicyService()

    def search_store_policies(
        self,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(arguments, dict):
            return {
                "success": False,
                "error": "Os argumentos da consulta são inválidos.",
            }

        query = arguments.get("query")

        if not isinstance(query, str) or not query.strip():
            return {
                "success": False,
                "error": "Informe o assunto da política que deseja consultar.",
            }

        try:
            policies = self._policy_service.search_policies(
                query=query,
                limit=5,
            )
        except Exception:
            return {
                "success": False,
                "error": ("Não foi possível consultar as políticas no momento."),
            }

        if not policies:
            return {
                "success": True,
                "found": False,
                "policies": [],
                "message": (
                    "Nenhuma política correspondente foi encontrada. "
                    "Não presuma regras que não constam no resultado."
                ),
            }

        return {
            "success": True,
            "found": True,
            "policies": [
                {
                    "id": policy["id"],
                    "category": policy.get("category", ""),
                    "title": policy["title"],
                    "rules": policy["rules"],
                    "source": policy.get("source", {}),
                    "requires_human_review": policy.get(
                        "requires_human_review",
                        True,
                    ),
                }
                for policy in policies
            ],
        }
