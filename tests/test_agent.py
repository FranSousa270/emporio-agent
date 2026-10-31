from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src.agent import agent as agent_module
from src.agent.prompts import SYSTEM_INSTRUCTION


@pytest.fixture
def mock_agent_dependencies(monkeypatch):
    settings = SimpleNamespace(
        gemini_model="gemini-3.8-flash",
    )

    mock_client = Mock()
    mock_get_settings = Mock(return_value=settings)
    mock_create_client = Mock(return_value=mock_client)

    monkeypatch.setattr(
        agent_module,
        "get_settings",
        mock_get_settings,
    )

    monkeypatch.setattr(
        agent_module,
        "create_gemini_client",
        mock_create_client,
    )

    return mock_client, mock_get_settings, mock_create_client


def test_agent_initialization(mock_agent_dependencies):
    mock_client, mock_get_settings, mock_create_client = (
        mock_agent_dependencies
    )

    agent = agent_module.Agent()

    assert agent._client is mock_client
    mock_get_settings.assert_called_once()
    mock_create_client.assert_called_once()


def test_agent_responds_with_gemini(
    mock_agent_dependencies,
):
    mock_client, _, _ = mock_agent_dependencies

    mock_client.interactions.create.return_value = (
        SimpleNamespace(output_text="Olá! Sou o assistente virtual.")
    )

    agent = agent_module.Agent()

    response = agent.respond("Olá!")

    assert response == "Olá! Sou o assistente virtual."

    mock_client.interactions.create.assert_called_once_with(
        model="gemini-3.8-flash",
        input="Olá!",
        system_instruction=SYSTEM_INSTRUCTION,
        store=False,
    )


def test_agent_rejects_empty_message(
    mock_agent_dependencies,
):
    mock_client, _, _ = mock_agent_dependencies

    agent = agent_module.Agent()

    with pytest.raises(ValueError):
        agent.respond("   ")

    mock_client.interactions.create.assert_not_called()


def test_agent_closes_client(mock_agent_dependencies):
    mock_client, _, _ = mock_agent_dependencies

    agent = agent_module.Agent()
    agent.close()

    mock_client.close.assert_called_once()