
import pandas as pd
import pytest

from src.repositories import csv_repository


def test_load_csv_successfully(tmp_path, monkeypatch):
    file_path = tmp_path / "products.csv"

    expected = pd.DataFrame({
        "product_id": [1, 2],
        "name": ["Guitar", "Keyboard"],
        "price_brl": [1500.0, 2500.0],
    })

    expected.to_csv(file_path, index=False)

    monkeypatch.setattr(csv_repository, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        csv_repository,
        "CSV_FILES",
        {"products": "products.csv"},
    )

    result = csv_repository.load_csv("products")

    pd.testing.assert_frame_equal(result, expected)


def test_load_csv_with_unknown_dataset():
    with pytest.raises(ValueError, match="Dataset não encontrado"):
        csv_repository.load_csv("unknown")


def test_load_csv_with_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(csv_repository, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        csv_repository,
        "CSV_FILES",
        {"products": "products.csv"},
    )

    with pytest.raises(FileNotFoundError, match="Arquivo não encontrado"):
        csv_repository.load_csv("products")


def test_load_all_csv_successfully(tmp_path, monkeypatch):
    products = pd.DataFrame({
        "product_id": [1],
        "name": ["Guitar"],
    })

    categories = pd.DataFrame({
        "category_id": [1],
        "name": ["Strings"],
    })

    products.to_csv(tmp_path / "products.csv", index=False)
    categories.to_csv(tmp_path / "categories.csv", index=False)

    monkeypatch.setattr(csv_repository, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        csv_repository,
        "CSV_FILES",
        {
            "products": "products.csv",
            "categories": "categories.csv",
        },
    )

    result = csv_repository.load_all_csv()

    assert set(result.keys()) == {"products", "categories"}
    assert len(result["products"]) == 1
    assert len(result["categories"]) == 1
