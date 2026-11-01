from unittest.mock import Mock

import pytest

from src.agent.conversation_history import ConversationHistory


def test_build_input_with_first_message():
    history = ConversationHistory()

    result = history.build_input("Olá!")

    assert result == [
        {
            "type": "user_input",
            "content": [
                {
                    "type": "text",
                    "text": "Olá!",
                }
            ],
        }
    ]

    assert history.get_history() == []


def test_add_turn_stores_user_and_model_steps():
    history = ConversationHistory()

    model_step = Mock()
    model_step.model_dump.return_value = {
        "type": "model_output",
        "content": [
            {
                "type": "text",
                "text": "Olá! Como posso ajudar?",
            }
        ],
    }

    history.add_turn("Olá!", [model_step])

    result = history.get_history()

    assert len(result) == 2
    assert result[0]["type"] == "user_input"
    assert result[1]["type"] == "model_output"

    model_step.model_dump.assert_called_once()


def test_build_input_preserves_previous_history():
    history = ConversationHistory()

    model_step = Mock()
    model_step.model_dump.return_value = {
        "type": "model_output",
        "content": [{"type": "text", "text": "Resposta 1"}],
    }

    history.add_turn("Mensagem 1", [model_step])

    result = history.build_input("Mensagem 2")

    assert len(result) == 3
    assert result[0]["type"] == "user_input"
    assert result[1]["type"] == "model_output"
    assert result[2]["content"][0]["text"] == "Mensagem 2"


def test_clear_removes_history():
    history = ConversationHistory()

    model_step = Mock()
    model_step.model_dump.return_value = {
        "type": "model_output",
        "content": [],
    }

    history.add_turn("Olá!", [model_step])
    history.clear()

    assert history.get_history() == []


@pytest.mark.parametrize("message", ["", "   "])
def test_build_input_rejects_empty_message(message):
    history = ConversationHistory()

    with pytest.raises(ValueError):
        history.build_input(message)


def test_add_step_stores_function_result():
    history = ConversationHistory()
    step = {
        "type": "function_result",
        "name": "search_store_policies",
        "call_id": "call-123",
        "result": {"found": True},
    }

    history.add_step(step)

    assert history.get_history() == [step]


def test_add_step_rejects_non_dictionary():
    history = ConversationHistory()

    with pytest.raises(TypeError):
        history.add_step("function_result")


def test_add_step_rejects_missing_type():
    history = ConversationHistory()

    with pytest.raises(ValueError):
        history.add_step({"name": "search_store_policies"})


def test_add_turn_stores_dictionary_steps():
    history = ConversationHistory()
    function_result = {
        "type": "function_result",
        "name": "search_store_policies",
        "call_id": "call-123",
        "result": [{"type": "text", "text": '{"found": true}'}],
    }

    history.add_turn("Qual é o prazo da garantia?", [function_result])

    stored_history = history.get_history()

    assert stored_history[0]["type"] == "user_input"
    assert stored_history[1] == function_result
