
import json

from google.genai import Client, errors

from src.agent.prompts import SYSTEM_INSTRUCTION
from src.agent.conversation_history import ConversationHistory
from src.core.config import get_settings
from src.integrations.gemini_client import create_gemini_client
from src.schemas.policy_schema import POLICY_SEARCH_TOOL
from src.schemas.product_schema import PRODUCT_SEARCH_TOOL
from src.tools.policy_tools import PolicyTools
from src.tools.product_tools import ProductTools


class Agent:
    MAX_TOOL_ROUNDS = 5

    def __init__(self):
        self._settings = get_settings()
        self._client: Client = create_gemini_client()
        self._history = ConversationHistory()
        self._policy_tools = PolicyTools()
        self._product_tools = ProductTools()
        self._tools = [
            POLICY_SEARCH_TOOL,
            PRODUCT_SEARCH_TOOL,
        ]

    def _execute_tool_call(
        self,
        name: str,
        arguments: dict,
    ) -> dict:
        if not isinstance(arguments, dict):
            return {
                "success": False,
                "error": "Os argumentos da consulta são inválidos.",
            }

        try:
            if name == "search_store_policies":
                return self._policy_tools.search_store_policies(arguments)

            if name == "search_store_products":
                return self._product_tools.search_store_products(arguments)

            return {
                "success": False,
                "error": "A ferramenta solicitada não está disponível.",
            }
        except Exception:
            return {
                "success": False,
                "error": "Não foi possível executar a consulta no momento.",
            }

    def respond(self, user_message: str) -> str:
        if not user_message.strip():
            raise ValueError("A mensagem não pode estar vazia.")

        input_history = self._history.build_input(user_message)
        turn_steps = []
        interaction = None
        pending_tool_calls = False

        for _ in range(self.MAX_TOOL_ROUNDS):
            try:
                interaction = self._client.interactions.create(
                    model=self._settings.gemini_model,
                    input=list(input_history),
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=self._tools,
                    store=False,
                )
            except errors.APIError as error:
                if error.code == 429:
                    return (
                        "O limite de uso da API Gemini foi atingido. "
                        "Verifique as cotas do projeto e tente novamente "
                        "quando houver disponibilidade."
                    )

                return (
                    "Não foi possível consultar o assistente neste momento. "
                    "Tente novamente mais tarde."
                )
            

            function_calls = [
                step
                for step in (interaction.steps or [])
                if step.type == "function_call"
            ]

            for step in interaction.steps or []:
                step_data = step.model_dump()
                turn_steps.append(step_data)
                input_history.append(step_data)

            if not function_calls:
                pending_tool_calls = False
                break

            pending_tool_calls = True

            for step in function_calls:
                result = self._execute_tool_call(
                    name=step.name,
                    arguments=step.arguments,
                )

                function_result = {
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                result,
                                ensure_ascii=False,
                            ),
                        }
                    ],
                }

                turn_steps.append(function_result)
                input_history.append(function_result)

        if interaction is None:
            return "Não foi possível concluir a interação."

        if pending_tool_calls:
            response = (
                "Não consegui concluir a consulta neste momento. "
                "Tente novamente mais tarde."
            )
        else:
            response = interaction.output_text or (
                "Não foi possível gerar uma resposta neste momento."
            )

        self._history.add_turn(user_message, turn_steps)
        return response

    def close(self) -> None:
        self._client.close()
