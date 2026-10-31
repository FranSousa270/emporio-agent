from google.genai import Client

from src.core.config import get_settings
from src.agent.prompts import SYSTEM_INSTRUCTION
from src.integrations.gemini_client import create_gemini_client


class Agent:
    def __init__(self):
        self._settings = get_settings()
        self._client: Client = create_gemini_client()

    def respond(self, user_message: str) -> str:
        if not user_message.strip():
            raise ValueError("A mensagem não pode estar vazia.")

        interaction = self._client.interactions.create(
            model=self._settings.gemini_model,
            input=user_message,
            system_instruction=SYSTEM_INSTRUCTION,
            store=False,
        )

        return interaction.output_text or ""

    def close(self) -> None:
        self._client.close()