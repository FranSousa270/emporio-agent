from unittest.mock import patch

import pytest

from src.services.policy_service import PolicyService


@pytest.fixture
def policies():
    return [
        {
            "id": "business_hours",
            "category": "hours",
            "title": "Horário de funcionamento",
            "rules": ["Atendimento de segunda a sexta-feira, das 09:00 às 18:00."],
        },
        {
            "id": "warranty",
            "category": "warranty",
            "title": "Garantia de produtos",
            "rules": [
                "A garantia legal contra defeitos é de 90 dias.",
                "A garantia do fabricante varia conforme o produto.",
            ],
        },
        {
            "id": "delivery",
            "category": "shipping",
            "title": "Entrega e frete",
            "rules": ["O prazo de entrega depende da modalidade de envio."],
        },
    ]


@pytest.fixture
def service(policies):
    with patch(
        "src.services.policy_service.load_policies",
        return_value={"policies": policies},
    ):
        return PolicyService()


def test_get_policy_returns_matching_policy(service):
    policy = service.get_policy("warranty")

    assert policy is not None
    assert policy["title"] == "Garantia de produtos"


def test_get_policy_is_case_insensitive(service):
    policy = service.get_policy("WARRANTY")

    assert policy is not None
    assert policy["id"] == "warranty"


def test_get_policy_returns_none_when_not_found(service):
    assert service.get_policy("unknown_policy") is None


def test_search_policies_finds_matching_terms(service):
    results = service.search_policies("garantia defeitos")

    assert results
    assert results[0]["id"] == "warranty"


def test_search_policies_ignores_accents_and_case(service):
    results = service.search_policies("GARANTÍA")

    assert results
    assert results[0]["id"] == "warranty"


def test_search_policies_returns_empty_for_blank_query(service):
    assert service.search_policies("   ") == []


def test_search_policies_respects_limit(service):
    results = service.search_policies("garantia entrega", limit=1)

    assert len(results) <= 1


def test_search_policies_rejects_non_positive_limit(service):
    with pytest.raises(ValueError, match="maior que zero"):
        service.search_policies("garantia", limit=0)


def test_search_policies_returns_empty_when_no_terms_match(service):
    assert service.search_policies("astronauta submarino") == []


def test_search_policies_prioritizes_title_matches(service):
    results = service.search_policies("Qual é a garantia legal para defeitos?")

    assert results
    assert results[0]["id"] == "warranty"


def test_search_policies_ignores_common_words(service):
    results = service.search_policies("qual é o prazo da garantia")

    assert results
    assert results[0]["id"] == "warranty"


def test_search_policies_returns_empty_when_query_has_only_stopwords(service):
    assert service.search_policies("qual é o que") == []
