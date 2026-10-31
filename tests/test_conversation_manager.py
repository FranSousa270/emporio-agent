from unittest.mock import Mock

import pytest

from src.session import conversation_manager as manager_module


@pytest.fixture
def mock_agent(monkeypatch):
    created_agents = []

    def create_agent():
        agent = Mock()
        created_agents.append(agent)
        return agent

    monkeypatch.setattr(
        manager_module,
        "Agent",
        create_agent,
    )

    return created_agents


def test_start_conversation(mock_agent):
    manager = manager_module.ConversationManager()

    session = manager.start_conversation()

    assert session.session_id is not None
    assert manager.get_session(session.session_id) is session
    assert manager.get_agent(session.session_id) is mock_agent[0]   


def test_start_multiple_independent_conversations(mock_agent):
    manager = manager_module.ConversationManager()

    first_session = manager.start_conversation()
    second_session = manager.start_conversation()

    assert first_session.session_id != second_session.session_id

    assert (
        manager.get_agent(first_session.session_id)
        is not manager.get_agent(second_session.session_id)
    )


def test_get_agent_from_nonexistent_session(mock_agent):
    manager = manager_module.ConversationManager()

    with pytest.raises(ValueError, match="Sessão não encontrada"):
        manager.get_agent("invalid-session-id")


def test_close_conversation(mock_agent):
    manager = manager_module.ConversationManager()

    session = manager.start_conversation()

    manager.close_conversation(session.session_id)

    mock_agent[0].close.assert_called_once()

    with pytest.raises(ValueError, match="Sessão não encontrada"):
        manager.get_session(session.session_id)


def test_close_conversation_when_agent_close_fails(mock_agent):
    manager = manager_module.ConversationManager()

    session = manager.start_conversation()

   
    mock_agent[0].close.side_effect = RuntimeError(
    "Erro ao fechar cliente"
)
    with pytest.raises(RuntimeError, match="Erro ao fechar cliente"):
        manager.close_conversation(session.session_id)

    with pytest.raises(ValueError, match="Sessão não encontrada"):
        manager.get_session(session.session_id)


def test_start_conversation_when_agent_initialization_fails(
    monkeypatch,
):
    mock_agent_factory = Mock(
        side_effect=RuntimeError("Falha na inicialização")
    )

    monkeypatch.setattr(
        manager_module,
        "Agent",
        mock_agent_factory,
    )

    manager = manager_module.ConversationManager()

    with pytest.raises(RuntimeError, match="Falha na inicialização"):
        manager.start_conversation()

    assert manager._session_manager._sessions == {}