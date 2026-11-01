from collections.abc import Mapping

REQUIRED_DATASETS = (
    "products",
    "categories",
    "customers",
    "orders",
    "order_items",
    "promotions",
)

REQUIRED_COLUMNS = {
    "products": {
        "product_id",
        "name",
        "price_brl",
        "category_id",
        "stock_quantity",
        "status",
    },
    "categories": {
        "category_id",
        "name",
    },
    "customers": {
        "customer_id",
        "name",
    },
    "orders": {
        "order_id",
        "customer_id",
        "status",
        "order_date",
    },
    "order_items": {
        "order_id",
        "product_id",
        "quantity",
    },
    "promotions": {
        "promotion_id",
        "product_id",
        "discount_percent",
        "is_active",
    },
}


def find_missing_datasets(
    datasets: Mapping[str, object],
) -> list[str]:
    return [dataset for dataset in REQUIRED_DATASETS if dataset not in datasets]


def find_missing_columns(
    datasets: Mapping[str, object],
) -> dict[str, list[str]]:
    missing_columns = {}

    for dataset, required_columns in REQUIRED_COLUMNS.items():
        if dataset not in datasets:
            continue

        dataframe = datasets[dataset]

        available_columns = set(dataframe.columns)

        missing = required_columns - available_columns

        if missing:
            missing_columns[dataset] = sorted(missing)

    return missing_columns


def validate_dataset_structure(
    datasets: Mapping[str, object],
) -> dict[str, object]:
    return {
        "missing_datasets": find_missing_datasets(datasets),
        "missing_columns": find_missing_columns(datasets),
    }
