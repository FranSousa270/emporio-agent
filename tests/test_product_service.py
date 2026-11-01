import pandas as pd
import pytest
from unittest.mock import patch

from src.services.product_service import ProductService


@pytest.fixture
def products():
    return pd.DataFrame(
        [
            {
                "product_id": 1,
                "name": "Violão Acústico",
                "description": "Violão com cordas de nylon",
                "price_brl": 599.90,
                "stock_quantity": 10,
                "status": "active",
                "specs": '{"strings": "nylon"}',
            },
            {
                "product_id": 2,
                "name": "Guitarra Elétrica",
                "description": "Guitarra para apresentações",
                "price_brl": 1200.00,
                "stock_quantity": 0,
                "status": "active",
                "specs": '{"electronics": "yes"}',
            },
            {
                "product_id": 3,
                "name": "Baixo Descontinuado",
                "description": "Baixo elétrico",
                "price_brl": 900.00,
                "stock_quantity": 5,
                "status": "discontinued",
                "specs": "{}",
            },
        ]
    )


@pytest.fixture
def promotions():
    return pd.DataFrame(
        [
            {
                "promotion_id": 10,
                "product_id": 1,
                "discount_percent": 10,
                "description": "Oferta especial",
                "is_active": 1,
            },
            {
                "promotion_id": 11,
                "product_id": 2,
                "discount_percent": 20,
                "description": "Oferta sem estoque",
                "is_active": 1,
            },
            {
                "promotion_id": 12,
                "product_id": 3,
                "discount_percent": 15,
                "description": "Oferta descontinuada",
                "is_active": 1,
            },
        ]
    )


@pytest.fixture
def service(products, promotions):
    with patch(
        "src.services.product_service.load_csv",
        side_effect=lambda dataset: {
            "products": products,
            "promotions": promotions,
        }[dataset],
    ):
        return ProductService()


def test_search_products_finds_name_match(service):
    results = service.search_products("violão acústico")

    assert len(results) == 1
    assert results[0]["product_id"] == 1


def test_search_products_ignores_accents_and_case(service):
    results = service.search_products("VIOLAO")

    assert results
    assert results[0]["product_id"] == 1


def test_search_products_excludes_inactive_products(service):
    results = service.search_products("baixo")

    assert results == []


def test_search_products_returns_empty_for_blank_query(service):
    assert service.search_products("   ") == []


def test_search_products_respects_limit(service):
    results = service.search_products("violão guitarra", limit=1)

    assert len(results) <= 1


def test_search_products_rejects_non_positive_limit(service):
    with pytest.raises(ValueError, match="maior que zero"):
        service.search_products("violão", limit=0)


def test_product_without_promotion_has_pix_discount(service, products, promotions):
    promotions = promotions[promotions["product_id"] != 1]

    with patch(
        "src.services.product_service.load_csv",
        side_effect=lambda dataset: {
            "products": products,
            "promotions": promotions,
        }[dataset],
    ):
        service_without_promotion = ProductService()

    result = service_without_promotion.search_products("violão")[0]

    assert result["price_brl"] == 599.90
    assert result["pix_price_brl"] == 569.91
    assert result["final_price_brl"] == 599.90
    assert result["promotion"] is None


def test_active_promotion_applies_discount_without_pix(service):
    result = service.search_products("violão")[0]

    assert result["promotion"]["discount_percent"] == 10
    assert result["final_price_brl"] == 539.91
    assert result["pix_price_brl"] is None


def test_product_without_stock_is_not_available(service):
    result = service.search_products("guitarra")[0]

    assert result["available"] is False
    assert result["stock_quantity"] == 0
    assert result["promotion"] is None
    assert result["pix_price_brl"] == 1140.0
    assert result["final_price_brl"] == 1200.0


def test_product_specs_are_parsed(service):
    result = service.search_products("violão")[0]

    assert result["specs"] == {"strings": "nylon"}
