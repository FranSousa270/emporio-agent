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


def create_model_step(text):
    step = Mock()

    step.model_dump.return_value = {
        "type": "model_output",
        "content": [
            {
                "type": "text",
                "text": text,
            }
        ],
    }

    return step


def test_agent_initialization(mock_agent_dependencies):
    mock_client, mock_get_settings, mock_create_client = (
        mock_agent_dependencies
    )

    agent = agent_module.Agent()

    assert agent._client is mock_client
    mock_get_settings.assert_called_once()
    mock_create_client.assert_called_once()


def test_agent_responds_with_gemini(mock_agent_dependencies):
    mock_client, _, _ = mock_agent_dependencies

    mock_client.interactions.create.return_value = (
        SimpleNamespace(
            output_text="Olá! Sou o assistente virtual.",
            steps=[
                create_model_step(
                    "Olá! Sou o assistente virtual."
                )
            ],
        )
    )

    agent = agent_module.Agent()

    response = agent.respond("Olá!")

    assert response == "Olá! Sou o assistente virtual."

    mock_client.interactions.create.assert_called_once_with(
        model="gemini-3.8-flash",
        input=[
            {
                "type": "user_input",
                "content": [
                    {
                        "type": "text",
                        "text": "Olá!",
                    }
                ],
            }
        ],
        system_instruction=SYSTEM_INSTRUCTION,
        store=False,
    )


def test_agent_preserves_conversation_history(
    mock_agent_dependencies,
):
    mock_client, _, _ = mock_agent_dependencies

    first_response = SimpleNamespace(
        output_text="Olá! Como posso ajudar?",
        steps=[
            create_model_step("Olá! Como posso ajudar?")
        ],
    )

    second_response = SimpleNamespace(
        output_text="Temos diversos modelos disponíveis.",
        steps=[
            create_model_step(
                "Temos diversos modelos disponíveis."
            )
        ],
    )

    mock_client.interactions.create.side_effect = [
        first_response,
        second_response,
    ]

    agent = agent_module.Agent()

    agent.respond("Olá!")

    response = agent.respond("Quais modelos vocês têm?")

    assert response == "Temos diversos modelos disponíveis."

    second_call = (
        mock_client.interactions.create.call_args_list[1]
    )

    sent_history = second_call.kwargs["input"]

    assert len(sent_history) == 3
    assert sent_history[0]["type"] == "user_input"
    assert sent_history[1]["type"] == "model_output"
    assert sent_history[2]["type"] == "user_input"

    assert (
        sent_history[2]["content"][0]["text"]
        == "Quais modelos vocês têm?"
    )


def test_agent_rejects_empty_message(mock_agent_dependencies):
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


def test_agent_history_is_isolated_between_instances(
    mock_agent_dependencies,
):
    mock_client, _, _ = mock_agent_dependencies

    mock_client.interactions.create.side_effect = [
        SimpleNamespace(
            output_text="Olá!",
            steps=[create_model_step("Olá!")],
        ),
        SimpleNamespace(
            output_text="Olá novamente!",
            steps=[create_model_step("Olá novamente!")],
        ),
    ]

    first_agent = agent_module.Agent()
    second_agent = agent_module.Agent()

    first_agent.respond("Olá!")
    second_agent.respond("Olá novamente!")

    assert first_agent._history.get_history() != (
        second_agent._history.get_history()
    )


def test_agent_does_not_save_history_when_api_fails(
    mock_agent_dependencies,
):
    mock_client, _, _ = mock_agent_dependencies

    mock_client.interactions.create.side_effect = RuntimeError(
        "API indisponível"
    )

    agent = agent_module.Agent()

    with pytest.raises(RuntimeError):
        agent.respond("Olá!")

    assert agent._history.get_history() == []


def test_agent_clear_history(mock_agent_dependencies):
    mock_client, _, _ = mock_agent_dependencies

    mock_client.interactions.create.return_value = (
        SimpleNamespace(
            output_text="Olá!",
            steps=[create_model_step("Olá!")],
        )
    )

    agent = agent_module.Agent()
    agent.respond("Olá!")

    agent._history.clear()

    assert agent._history.get_history() == []