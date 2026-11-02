from src.services.product_service import ProductService


class ProductTools:
    DEFAULT_LIMIT = 5

    def __init__(self):
        self._product_service = ProductService()

    def search_store_products(self, arguments: dict) -> dict:
        if not isinstance(arguments, dict):
            return {
                "success": False,
                "error": "Os argumentos da consulta são inválidos.",
            }

        query = arguments.get("query")
        page = arguments.get("page", 1)

        if not isinstance(query, str) or not query.strip():
            return {
                "success": False,
                "error": "Informe o nome ou os termos do produto desejado.",
            }

        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            return {
                "success": False,
                "error": "A página deve ser um inteiro maior que zero.",
            }

        try:
            products = self._product_service.search_products(
                query,
                limit=self.DEFAULT_LIMIT + 1,
                page=page,
                page_size=self.DEFAULT_LIMIT,
            )
        except Exception:
            return {
                "success": False,
                "error": "Não foi possível consultar os produtos no momento.",
            }

        has_next_page = len(products) > self.DEFAULT_LIMIT
        products = products[: self.DEFAULT_LIMIT]

        return {
            "success": True,
            "found": bool(products),
            "products": products,
            "page": page,
            "has_next_page": has_next_page,
        }
