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
        "page": 1,
        "has_next_page": False,
    }

    product_tools._product_service.search_products.assert_called_once_with(
        "Yamaha C40",
        limit=6,
        page=1,
        page_size=5,
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
        "page": 1,
        "has_next_page": False,
    }


def test_search_store_products_handles_service_error(product_tools):
    product_tools._product_service.search_products.side_effect = RuntimeError(
        "Detalhe interno"
    )

    result = product_tools.search_store_products({"query": "Yamaha C40"})

    assert result["success"] is False
    assert result["error"] == ("Não foi possível consultar os produtos no momento.")
    assert "Detalhe interno" not in str(result)


def test_search_store_products_indicates_next_page(product_tools):
    products = [
        {
            "product_id": product_id,
            "name": f"Violão Modelo {product_id}",
            "price_brl": 500.00,
            "stock_quantity": 10,
        }
        for product_id in range(1, 7)
    ]

    product_tools._product_service.search_products.return_value = products

    result = product_tools.search_store_products({"query": "violão"})

    assert result["success"] is True
    assert result["found"] is True
    assert len(result["products"]) == 5
    assert result["has_next_page"] is True
    assert result["page"] == 1
    assert [product["product_id"] for product in result["products"]] == [1, 2, 3, 4, 5]


def test_search_store_products_indicates_last_page(product_tools):
    products = [
        {
            "product_id": 6,
            "name": "Violão Modelo 6",
            "price_brl": 500.00,
            "stock_quantity": 10,
        }
    ]

    product_tools._product_service.search_products.return_value = products

    result = product_tools.search_store_products({"query": "violão", "page": 2})

    assert result["success"] is True
    assert result["found"] is True
    assert len(result["products"]) == 1
    assert result["has_next_page"] is False
    assert result["page"] == 2


def test_search_store_products_rejects_invalid_page(product_tools):
    result = product_tools.search_store_products({"query": "violão", "page": 0})

    assert result == {
        "success": False,
        "error": "A página deve ser um inteiro maior que zero.",
    }

    product_tools._product_service.search_products.assert_not_called()
