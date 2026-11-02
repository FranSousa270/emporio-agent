from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "csv"

CSV_FILES = {
    "products": "products.csv",
    "categories": "categories.csv",
    "customers": "customers.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "promotions": "promotions.csv",
}


def load_csv(dataset: str) -> pd.DataFrame:
    filename = CSV_FILES.get(dataset)

    if filename is None:
        raise ValueError(f"Dataset não encontrado: {dataset}")

    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_all_csv() -> dict[str, pd.DataFrame]:
    return {dataset: load_csv(dataset) for dataset in CSV_FILES}
