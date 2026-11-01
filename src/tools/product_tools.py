
from src.services.product_service import ProductService


class ProductTools:
    def __init__(self):
        self._product_service = ProductService()

    def search_store_products(self, arguments: dict) -> dict:
        if not isinstance(arguments, dict):
            return {
                "success": False,
                "error": "Os argumentos da consulta são inválidos.",
            }

        query = arguments.get("query")

        if not isinstance(query, str) or not query.strip():
            return {
                "success": False,
                "error": "Informe o nome ou os termos do produto desejado.",
            }

        try:
            products = self._product_service.search_products(query, limit=5)
        except Exception:
            return {
                "success": False,
                "error": "Não foi possível consultar os produtos no momento.",
            }

        return {
            "success": True,
            "found": bool(products),
            "products": products,
        }
