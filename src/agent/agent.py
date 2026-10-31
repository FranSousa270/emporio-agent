from google.genai import Client

from src.core.config import get_settings
from src.agent.prompts import SYSTEM_INSTRUCTION
from src.agent.conversation_history import ConversationHistory
from src.integrations.gemini_client import create_gemini_client


class Agent:
    def __init__(self):
        self._settings = get_settings()
        self._client: Client = create_gemini_client()
        self._history = ConversationHistory()

    def respond(self, user_message: str) -> str:
        if not user_message.strip():
            raise ValueError("A mensagem não pode estar vazia.")

        interaction = self._client.interactions.create(
            model=self._settings.gemini_model,
            input=self._history.build_input(user_message),
            system_instruction=SYSTEM_INSTRUCTION,
            store=False,
        )

        self._history.add_turn(
            user_message,
            interaction.steps or [],
        )

        return interaction.output_text or ""

    def close(self) -> None:
        self._client.close()