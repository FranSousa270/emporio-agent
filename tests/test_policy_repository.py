
import json

import pytest

from src.repositories import policy_repository


@pytest.fixture
def valid_policy_data():
    return {
        "document": {
            "title": "Manual de Políticas e Procedimentos",
            "version": "2.1",
        },
        "policies": [
            {
                "id": "business_hours",
                "title": "Horário de funcionamento",
                "rules": [
                    "A loja funciona de segunda a sexta-feira."
                ],
            }
        ],
    }


@pytest.fixture
def policies_file(tmp_path, monkeypatch, valid_policy_data):
    file_path = tmp_path / "policies.json"

    file_path.write_text(
        json.dumps(valid_policy_data, ensure_ascii=False),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        policy_repository,
        "POLICIES_PATH",
        file_path,
    )

    return file_path


def test_load_policies_returns_valid_data(policies_file):
    data = policy_repository.load_policies()

    assert data["document"]["title"] == (
        "Manual de Políticas e Procedimentos"
    )
    assert data["policies"][0]["id"] == "business_hours"


def test_load_policies_raises_when_file_is_missing(
    tmp_path,
    monkeypatch,
):
    missing_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        policy_repository,
        "POLICIES_PATH",
        missing_file,
    )

    with pytest.raises(FileNotFoundError):
        policy_repository.load_policies()


def test_load_policies_raises_for_invalid_json(
    policies_file,
):
    policies_file.write_text(
        '{"document": ',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="JSON inválido"):
        policy_repository.load_policies()


def test_load_policies_raises_when_root_is_not_object(
    policies_file,
):
    policies_file.write_text(
        json.dumps(["invalid"]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="objeto JSON"):
        policy_repository.load_policies()


def test_load_policies_raises_when_document_is_missing(
    policies_file,
):
    policies_file.write_text(
        json.dumps({"policies": []}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="document"):
        policy_repository.load_policies()


def test_load_policies_raises_when_policies_is_not_a_list(
    policies_file,
):
    policies_file.write_text(
        json.dumps({
            "document": {},
            "policies": {},
        }),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="lista 'policies'"):
        policy_repository.load_policies()


def test_load_policies_raises_when_policy_id_is_missing(
    policies_file,
    valid_policy_data,
):
    valid_policy_data["policies"][0].pop("id")

    policies_file.write_text(
        json.dumps(valid_policy_data),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="ID inválido"):
        policy_repository.load_policies()


def test_load_policies_raises_when_policy_ids_are_duplicated(
    policies_file,
    valid_policy_data,
):
    duplicated_policy = {
        **valid_policy_data["policies"][0],
    }

    valid_policy_data["policies"].append(duplicated_policy)

    policies_file.write_text(
        json.dumps(valid_policy_data),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicado"):
        policy_repository.load_policies()


def test_load_policies_raises_when_rules_are_invalid(
    policies_file,
    valid_policy_data,
):
    valid_policy_data["policies"][0]["rules"] = "não é uma lista"

    policies_file.write_text(
        json.dumps(valid_policy_data),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="regras inválidas"):
        policy_repository.load_policies()
