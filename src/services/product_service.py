
import json
import unicodedata
from typing import Any
from decimal import Decimal, ROUND_HALF_UP

import pandas as pd

from src.repositories.csv_repository import load_csv


class ProductService:
    STOPWORDS = {
        "a", "as", "o", "os", "um", "uma", "de", "da", "das",
        "do", "dos", "em", "no", "na", "nos", "nas", "com",
        "para", "por", "qual", "quais", "que", "e", "é", "me",
        "tem", "ter", "quero", "procurando", "produto", "produtos",
    }

    NAME_WEIGHT = 3
    DESCRIPTION_WEIGHT = 1
    SPECS_WEIGHT = 1

    def __init__(self):
        self._products = load_csv("products")
        self._promotions = load_csv("promotions")

    @staticmethod
    def _calculate_price(value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)    

    @staticmethod
    def _normalize(value: Any) -> str:
        normalized = unicodedata.normalize("NFKD", str(value))
        without_accents = "".join(
            character
            for character in normalized
            if not unicodedata.combining(character)
        )
        return without_accents.casefold().strip()

    @classmethod
    def _tokenize(cls, value: Any) -> set[str]:
        normalized = cls._normalize(value)
        terms = {
            term.strip(".,!?;:()[]{}\"'")
            for term in normalized.split()
        }
        return {
            term
            for term in terms
            if term and term not in cls.STOPWORDS
        }

    @staticmethod
    def _is_active(value: Any) -> bool:
        if pd.isna(value):
            return False

        if isinstance(value, str):
            return value.strip().casefold() in {"1", "true", "yes", "sim"}

        return value == 1 or value is True

    @staticmethod
    def _parse_specs(value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return value

        if not isinstance(value, str) or not value.strip():
            return {}

        try:
            parsed = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return {}

        return parsed if isinstance(parsed, dict) else {}

    def _get_active_promotion(
        self,
        product_id: Any,
        available: bool,
    ) -> dict[str, Any] | None:
        if not available:
            return None

        promotions = self._promotions[
            (self._promotions["product_id"] == product_id)
            & self._promotions["is_active"].apply(self._is_active)
        ]

        if promotions.empty:
            return None

        promotion = promotions.iloc[0]

        return {
            "promotion_id": int(promotion["promotion_id"]),
            "description": str(promotion["description"]),
            "discount_percent": float(promotion["discount_percent"]),
        }

    def _format_product(self, product: dict[str, Any]) -> dict[str, Any]:
        price = Decimal(str(product["price_brl"]))
        stock = int(product["stock_quantity"])
        available = stock > 0

        promotion = self._get_active_promotion(
            product["product_id"],
            available,
        )

        result = {
            "product_id": int(product["product_id"]),
            "name": str(product["name"]),
            "description": str(product["description"]),
            "price_brl": float(self._calculate_price(price)),
            "stock_quantity": stock,
            "available": available,
            "specs": self._parse_specs(product.get("specs")),
            "promotion": promotion,
            "pix_price_brl": None,
        }

        if promotion:
            discount = Decimal(str(promotion["discount_percent"])) / Decimal("100")
            final_price = self._calculate_price(price * (Decimal("1") - discount))
        else:
            final_price = self._calculate_price(price)
            result["pix_price_brl"] = float(
                self._calculate_price(price * Decimal("0.95"))
            )

        result["final_price_brl"] = float(final_price)

        return result

        

    def search_products(
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

        products = self._products[
            self._products["status"].apply(
                lambda status: self._normalize(status) == "active"
            )
        ]

        matches: list[tuple[int, int, dict[str, Any]]] = []

        for index, (_, row) in enumerate(products.iterrows()):
            product = row.to_dict()

            name_terms = self._tokenize(product["name"])
            description_terms = self._tokenize(product["description"])
            specs_terms = self._tokenize(product.get("specs", ""))

            score = sum(
                self.NAME_WEIGHT if term in name_terms
                else self.DESCRIPTION_WEIGHT
                if term in description_terms
                else self.SPECS_WEIGHT if term in specs_terms
                else 0
                for term in query_terms
            )

            if score > 0:
                matches.append((score, index, product))

        matches.sort(key=lambda item: (-item[0], item[1]))

        return [
            self._format_product(product)
            for _, _, product in matches[:limit]
        ]
