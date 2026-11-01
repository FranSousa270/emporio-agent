import pandas as pd

from src.validators.data_validator import (
    find_missing_columns,
    find_missing_datasets,
    validate_dataset_structure,
)


def test_find_missing_datasets_when_all_are_present():
    datasets = {
        "products": object(),
        "categories": object(),
        "customers": object(),
        "orders": object(),
        "order_items": object(),
        "promotions": object(),
    }

    result = find_missing_datasets(datasets)

    assert result == []


def test_find_missing_datasets_when_one_is_missing():
    datasets = {
        "products": object(),
        "categories": object(),
        "orders": object(),
        "order_items": object(),
        "promotions": object(),
    }

    result = find_missing_datasets(datasets)

    assert result == ["customers"]


def test_find_missing_datasets_when_multiple_are_missing():
    datasets = {
        "products": object(),
        "orders": object(),
    }

    result = find_missing_datasets(datasets)

    assert result == [
        "categories",
        "customers",
        "order_items",
        "promotions",
    ]


def test_find_missing_columns_when_all_are_present():
    datasets = {
        "products": pd.DataFrame(
            columns=[
                "product_id",
                "name",
                "price_brl",
                "category_id",
                "stock_quantity",
                "status",
            ]
        ),
    }

    result = find_missing_columns(datasets)

    assert result == {}


def test_find_missing_columns_when_columns_are_missing():
    datasets = {
        "products": pd.DataFrame(
            columns=[
                "product_id",
                "name",
                "stock_quantity",
            ]
        ),
    }

    result = find_missing_columns(datasets)

    assert result == {
        "products": [
            "category_id",
            "price_brl",
            "status",
        ]
    }


def test_find_missing_columns_ignores_missing_datasets():
    datasets = {
        "products": pd.DataFrame(
            columns=[
                "product_id",
                "name",
                "price_brl",
                "category_id",
                "stock_quantity",
                "status",
            ]
        ),
    }

    result = find_missing_columns(datasets)

    assert result == {}


def test_validate_dataset_structure_when_all_are_valid():
    datasets = {
        "products": pd.DataFrame(
            columns=[
                "product_id",
                "name",
                "price_brl",
                "category_id",
                "stock_quantity",
                "status",
            ]
        ),
        "categories": pd.DataFrame(columns=["category_id", "name"]),
        "customers": pd.DataFrame(columns=["customer_id", "name"]),
        "orders": pd.DataFrame(
            columns=[
                "order_id",
                "customer_id",
                "status",
                "order_date",
            ]
        ),
        "order_items": pd.DataFrame(columns=["order_id", "product_id", "quantity"]),
        "promotions": pd.DataFrame(
            columns=[
                "promotion_id",
                "product_id",
                "discount_percent",
                "is_active",
            ]
        ),
    }

    result = validate_dataset_structure(datasets)

    assert result == {
        "missing_datasets": [],
        "missing_columns": {},
    }


def test_validate_dataset_structure_when_dataset_is_missing():
    datasets = {
        "products": pd.DataFrame(
            columns=[
                "product_id",
                "name",
                "price_brl",
                "category_id",
                "stock_quantity",
                "status",
            ]
        ),
    }

    result = validate_dataset_structure(datasets)

    assert result["missing_datasets"] == [
        "categories",
        "customers",
        "orders",
        "order_items",
        "promotions",
    ]


def test_validate_dataset_structure_when_column_is_missing():
    datasets = {
        "products": pd.DataFrame(
            columns=[
                "product_id",
                "name",
                "stock_quantity",
            ]
        ),
    }

    result = validate_dataset_structure(datasets)

    assert result["missing_datasets"] == [
        "categories",
        "customers",
        "orders",
        "order_items",
        "promotions",
    ]

    assert result["missing_columns"] == {
        "products": [
            "category_id",
            "price_brl",
            "status",
        ]
    }
