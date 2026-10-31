import pytest

from src.session.session_manager import SessionManager


def test_create_session():
    manager = SessionManager()

    session = manager.create_session()

    assert session.session_id is not None
    assert session.authenticated is False
    assert session.customer_id is None
    assert session.product_search_context is None
    assert session.order_search_context is None
    assert session.pending_requests == []


def test_create_sessions_with_different_ids():
    manager = SessionManager()

    first_session = manager.create_session()
    second_session = manager.create_session()

    assert first_session.session_id != second_session.session_id


def test_get_existing_session():
    manager = SessionManager()

    created_session = manager.create_session()

    retrieved_session = manager.get_session(
        created_session.session_id
    )

    assert retrieved_session is created_session


def test_get_nonexistent_session():
    manager = SessionManager()

    with pytest.raises(ValueError, match="Sessão não encontrada"):
        manager.get_session("invalid-session-id")


def test_close_session():
    manager = SessionManager()

    session = manager.create_session()

    manager.close_session(session.session_id)

    with pytest.raises(ValueError, match="Sessão não encontrada"):
        manager.get_session(session.session_id)


def test_close_nonexistent_session():
    manager = SessionManager()

    with pytest.raises(ValueError, match="Sessão não encontrada"):
        manager.close_session("invalid-session-id")


def test_sessions_have_independent_authentication():
    manager = SessionManager()

    first_session = manager.create_session()
    second_session = manager.create_session()

    first_session.authenticated = True
    first_session.customer_id = 123

    assert first_session.authenticated is True
    assert first_session.customer_id == 123

    assert second_session.authenticated is False
    assert second_session.customer_id is None


def test_sessions_have_independent_search_contexts():
    manager = SessionManager()

    first_session = manager.create_session()
    second_session = manager.create_session()

    first_session.product_search_context = {
        "query": "guitarra",
        "current_page": 1,
    }

    first_session.pending_requests.append({
        "type": "complaint",
    })

    assert first_session.product_search_context is not None
    assert second_session.product_search_context is None

    assert len(first_session.pending_requests) == 1
    assert second_session.pending_requests == []