from typing import Any


class ConversationHistory:
    def __init__(self):
        self._steps: list[dict[str, Any]] = []

    def build_input(self, user_message: str) -> list[dict[str, Any]]:
        if not user_message.strip():
            raise ValueError("A mensagem não pode estar vazia.")

        return [
            *self._steps,
            {
                "type": "user_input",
                "content": [
                    {
                        "type": "text",
                        "text": user_message,
                    }
                ],
            },
        ]

    def add_turn(self, user_message: str, model_steps: list[Any]) -> None:
        if not user_message.strip():
            raise ValueError("A mensagem não pode estar vazia.")

        self._steps.append({
            "type": "user_input",
            "content": [
                {
                    "type": "text",
                    "text": user_message,
                }
            ],
        })

        for step in model_steps:
            self._steps.append(step.model_dump())

    def get_history(self) -> list[dict[str, Any]]:
        return list(self._steps)

    def clear(self) -> None:
        self._steps.clear()