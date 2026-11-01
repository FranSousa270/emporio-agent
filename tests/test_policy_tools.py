
from unittest.mock import Mock

from src.tools.policy_tools import PolicyTools


def make_policy_service():
    service = Mock()
    service.search_policies.return_value = [
        {
            "id": "warranty",
            "category": "warranty",
            "title": "Garantia de produtos",
            "rules": [
                "A garantia legal contra defeitos é de 90 dias."
            ],
            "source": {"section": "7"},
            "requires_human_review": True,
        }
    ]
    return service


def test_search_store_policies_returns_matching_policies():
    service = make_policy_service()
    tools = PolicyTools(policy_service=service)

    result = tools.search_store_policies({
        "query": "garantia defeito"
    })

    assert result["success"] is True
    assert result["found"] is True
    assert result["policies"][0]["id"] == "warranty"
    service.search_policies.assert_called_once_with(
        query="garantia defeito",
        limit=5,
    )


def test_search_store_policies_rejects_non_dictionary_arguments():
    tools = PolicyTools(policy_service=make_policy_service())

    result = tools.search_store_policies("garantia")

    assert result["success"] is False
    assert "error" in result


def test_search_store_policies_rejects_missing_query():
    tools = PolicyTools(policy_service=make_policy_service())

    result = tools.search_store_policies({})

    assert result["success"] is False
    assert "error" in result


def test_search_store_policies_rejects_blank_query():
    tools = PolicyTools(policy_service=make_policy_service())

    result = tools.search_store_policies({"query": "   "})

    assert result["success"] is False
    assert "error" in result


def test_search_store_policies_returns_not_found():
    service = Mock()
    service.search_policies.return_value = []
    tools = PolicyTools(policy_service=service)

    result = tools.search_store_policies({
        "query": "assunto inexistente"
    })

    assert result["success"] is True
    assert result["found"] is False
    assert result["policies"] == []


def test_search_store_policies_handles_service_failure():
    service = Mock()
    service.search_policies.side_effect = RuntimeError(
        "Erro interno de teste"
    )
    tools = PolicyTools(policy_service=service)

    result = tools.search_store_policies({
        "query": "garantia"
    })

    assert result["success"] is False
    assert "error" in result
    assert "Erro interno de teste" not in result["error"]


def test_search_store_policies_limits_results_to_five():
    service = make_policy_service()
    tools = PolicyTools(policy_service=service)

    tools.search_store_policies({"query": "garantia"})

    service.search_policies.assert_called_once_with(
        query="garantia",
        limit=5,
    )
