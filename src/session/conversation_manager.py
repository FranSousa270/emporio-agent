from src.agent.agent import Agent
from src.session.session_manager import Session, SessionManager


class ConversationManager:
    def __init__(self):
        self._session_manager = SessionManager()
        self._agents: dict[str, Agent] = {}

    def start_conversation(self) -> Session:
        session = self._session_manager.create_session()

        try:
            agent = Agent()
            self._agents[session.session_id] = agent

        except Exception:
            self._session_manager.close_session(
                session.session_id
            )
            raise

        return session

    def get_session(self, session_id: str) -> Session:
        return self._session_manager.get_session(session_id)

    def get_agent(self, session_id: str) -> Agent:
        self._session_manager.get_session(session_id)

        agent = self._agents.get(session_id)

        if agent is None:
            raise ValueError("Agente da conversa não encontrado.")

        return agent

    def close_conversation(self, session_id: str) -> None:
        self._session_manager.get_session(session_id)

        agent = self._agents.pop(session_id)

        try:
            agent.close()
        finally:
            self._session_manager.close_session(session_id)