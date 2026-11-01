from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class Session:
    session_id: str = field(default_factory=lambda: str(uuid4()))

    authenticated: bool = False
    customer_id: str | int | None = None

    product_search_context: dict[str, Any] | None = None
    order_search_context: dict[str, Any] | None = None

    pending_requests: list[dict[str, Any]] = field(default_factory=list)


class SessionManager:
    def __init__(self):
        self._sessions: dict[str, Session] = {}

    def create_session(self) -> Session:
        session = Session()

        self._sessions[session.session_id] = session

        return session

    def get_session(self, session_id: str) -> Session:
        session = self._sessions.get(session_id)

        if session is None:
            raise ValueError("Sessão não encontrada.")

        return session

    def close_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise ValueError("Sessão não encontrada.")

        del self._sessions[session_id]
