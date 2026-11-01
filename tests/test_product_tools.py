from unittest.mock import Mock

import pytest

from src.tools.product_tools import ProductTools


@pytest.fixture
def product_tools():
    tools = ProductTools()
    tools._product_service = Mock()
    return tools


def test_search_store_products_returns_products(product_tools):
    expected_products = [
        {
            "product_id": 81,
            "name": "Yamaha C40 Nylon Natural",
            "price_brl": 599.90,
            "stock_quantity": 12,
        }
    ]

    product_tools._product_service.search_products.return_value = expected_products

    result = product_tools.search_store_products({"query": "Yamaha C40"})

    assert result == {
        "success": True,
        "found": True,
        "products": expected_products,
    }

    product_tools._product_service.search_products.assert_called_once_with(
        "Yamaha C40",
        limit=5,
    )


@pytest.mark.parametrize(
    "arguments",
    [
        None,
        [],
        {},
        {"query": ""},
        {"query": "   "},
        {"query": 123},
    ],
)
def test_search_store_products_rejects_invalid_arguments(
    product_tools,
    arguments,
):
    result = product_tools.search_store_products(arguments)

    assert result["success"] is False
    assert "error" in result

    product_tools._product_service.search_products.assert_not_called()


def test_search_store_products_returns_not_found(product_tools):
    product_tools._product_service.search_products.return_value = []

    result = product_tools.search_store_products({"query": "produto inexistente"})

    assert result == {
        "success": True,
        "found": False,
        "products": [],
    }


def test_search_store_products_handles_service_error(product_tools):
    product_tools._product_service.search_products.side_effect = RuntimeError(
        "Detalhe interno"
    )

    result = product_tools.search_store_products({"query": "Yamaha C40"})

    assert result["success"] is False
    assert result["error"] == ("Não foi possível consultar os produtos no momento.")
    assert "Detalhe interno" not in str(result)
