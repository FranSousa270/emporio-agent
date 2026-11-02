from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import pandas as pd
import pytest

from src.services import auth_service as auth_module
from src.services.auth_service import AuthService
from src.session.session_manager import Session


@pytest.fixture
def auth_service(monkeypatch):
    customers = pd.DataFrame(
        [
            {
                "customer_id": 101,
                "name": "Cliente Teste",
                "email": "cliente@email.com",
            },
            {
                "customer_id": 102,
                "name": "Outro Cliente",
                "email": "outro@email.com",
            },
        ]
    )

    monkeypatch.setattr(
        auth_module,
        "load_csv",
        lambda dataset: customers.copy(),
    )

    monkeypatch.setattr(
        auth_module.secrets,
        "randbelow",
        lambda limit: 123456,
    )

    return AuthService()


@pytest.fixture
def session():
    return Session()


def test_request_code_for_registered_customer(
    auth_service,
    session,
    capsys,
):
    result = auth_service.request_code(
        session,
        "cliente@email.com",
    )

    captured = capsys.readouterr()

    assert result is True
    assert "[AUTH] Código de autenticação: 123456" in captured.out
    assert session.authenticated is False
    assert session.customer_id is None


def test_request_code_with_email_case_insensitive(
    auth_service,
    session,
):
    result = auth_service.request_code(
        session,
        "  CLIENTE@EMAIL.COM  ",
    )

    assert result is True


def test_request_code_for_nonexistent_customer(
    auth_service,
    session,
):
    result = auth_service.request_code(
        session,
        "inexistente@email.com",
    )

    assert result is False
    assert session.session_id not in auth_service._challenges


def test_request_code_with_empty_email(
    auth_service,
    session,
):
    result = auth_service.request_code(
        session,
        "   ",
    )

    assert result is False
    assert session.session_id not in auth_service._challenges


def test_verify_correct_code(
    auth_service,
    session,
):
    auth_service.request_code(
        session,
        "cliente@email.com",
    )

    result = auth_service.verify_code(
        session,
        "123456",
    )

    assert result is True
    assert session.authenticated is True
    assert session.customer_id == 101
    assert session.session_id not in auth_service._challenges


def test_verify_incorrect_code(
    auth_service,
    session,
):
    auth_service.request_code(
        session,
        "cliente@email.com",
    )

    result = auth_service.verify_code(
        session,
        "999999",
    )

    assert result is False
    assert session.authenticated is False
    assert session.customer_id is None
    assert auth_service._challenges[session.session_id].attempts == 1


def test_challenge_removed_after_three_incorrect_attempts(
    auth_service,
    session,
):
    auth_service.request_code(
        session,
        "cliente@email.com",
    )

    for _ in range(3):
        result = auth_service.verify_code(
            session,
            "999999",
        )

        assert result is False

    assert session.session_id not in auth_service._challenges
    assert session.authenticated is False


def test_expired_code_cannot_be_used(
    auth_service,
    session,
    monkeypatch,
):
    auth_service.request_code(
        session,
        "cliente@email.com",
    )

    future_time = datetime.now(timezone.utc) + timedelta(minutes=6)

    monkeypatch.setattr(
        auth_service,
        "_now",
        lambda: future_time,
    )

    result = auth_service.verify_code(
        session,
        "123456",
    )

    assert result is False
    assert session.authenticated is False
    assert session.session_id not in auth_service._challenges


def test_code_cannot_be_reused_for_another_session(
    auth_service,
):
    first_session = Session()
    second_session = Session()

    auth_service.request_code(
        first_session,
        "cliente@email.com",
    )

    result = auth_service.verify_code(
        second_session,
        "123456",
    )

    assert result is False
    assert first_session.authenticated is False
    assert second_session.authenticated is False


def test_authenticated_session_does_not_need_new_code(
    auth_service,
    session,
):
    auth_service.request_code(
        session,
        "cliente@email.com",
    )

    auth_service.verify_code(
        session,
        "123456",
    )

    result = auth_service.verify_code(
        session,
        "999999",
    )

    assert result is True
    assert session.authenticated is True
    assert session.customer_id == 101


def test_authenticated_session_cannot_request_another_code(
    auth_service,
    session,
):
    session.authenticated = True
    session.customer_id = 101

    with pytest.raises(
        ValueError,
        match="A sessão já está autenticada",
    ):
        auth_service.request_code(
            session,
            "cliente@email.com",
        )
