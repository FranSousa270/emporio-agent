import unicodedata
from typing import Any

from src.repositories.policy_repository import load_policies


class PolicyService:
    STOPWORDS = {
        "a",
        "as",
        "o",
        "os",
        "um",
        "uma",
        "uns",
        "umas",
        "de",
        "da",
        "das",
        "do",
        "dos",
        "em",
        "no",
        "na",
        "nos",
        "nas",
        "ao",
        "aos",
        "com",
        "por",
        "para",
        "qual",
        "quais",
        "que",
        "e",
        "ou",
        "é",
        "ser",
        "são",
        "como",
        "me",
        "minha",
        "meu",
        "minhas",
        "meus",
        "sobre",
        "qual",
        "tem",
        "ter",
    }

    ID_WEIGHT = 4
    TITLE_WEIGHT = 3
    CATEGORY_WEIGHT = 2
    RULE_WEIGHT = 1

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

    @classmethod
    def _tokenize(cls, value: str) -> set[str]:
        normalized = cls._normalize(value)

        return {term for term in normalized.split() if term not in cls.STOPWORDS}

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

        query_terms = self._tokenize(query)

        if not query_terms:
            return []

        matches: list[tuple[int, int, dict[str, Any]]] = []

        for index, policy in enumerate(self._policies):
            policy_id_terms = self._tokenize(policy.get("id", ""))
            title_terms = self._tokenize(policy.get("title", ""))
            category_terms = self._tokenize(policy.get("category", ""))

            rule_terms = self._tokenize(" ".join(policy.get("rules", [])))

            score = sum(
                (
                    self.ID_WEIGHT
                    if term in policy_id_terms
                    else (
                        self.TITLE_WEIGHT
                        if term in title_terms
                        else (
                            self.CATEGORY_WEIGHT
                            if term in category_terms
                            else self.RULE_WEIGHT if term in rule_terms else 0
                        )
                    )
                )
                for term in query_terms
            )

            if score > 0:
                matches.append((score, index, policy))

        matches.sort(key=lambda item: (-item[0], item[1]))

        return [policy for _, _, policy in matches[:limit]]
