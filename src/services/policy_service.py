
import unicodedata
from typing import Any

from src.repositories.policy_repository import load_policies


class PolicyService:
    def __init__(self):
        data = load_policies()
        self._policies: list[dict[str, Any]] = data["policies"]

    @staticmethod
    def _normalize(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value)

        without_accents = "".join(
            character
            for character in normalized
            if not unicodedata.combining(character)
        )

        return without_accents.casefold().strip()

    def get_policy(self, policy_id: str) -> dict[str, Any] | None:
        normalized_id = self._normalize(policy_id)

        for policy in self._policies:
            if self._normalize(policy["id"]) == normalized_id:
                return policy

        return None

    def search_policies(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            return []

        if limit < 1:
            raise ValueError("O limite deve ser maior que zero.")

        query_terms = set(self._normalize(query).split())

        if not query_terms:
            return []

        matches: list[tuple[int, int, dict[str, Any]]] = []

        for index, policy in enumerate(self._policies):
            searchable_text = " ".join([
                policy.get("id", ""),
                policy.get("category", ""),
                policy.get("title", ""),
                *policy.get("rules", []),
            ])

            policy_terms = set(
                self._normalize(searchable_text).split()
            )

            score = len(query_terms & policy_terms)

            if score > 0:
                matches.append((score, index, policy))

        matches.sort(key=lambda item: (-item[0], item[1]))

        return [
            policy
            for _, _, policy in matches[:limit]
        ]
