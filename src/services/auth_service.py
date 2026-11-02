import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from src.repositories.csv_repository import load_csv
from src.session.session_manager import Session


@dataclass
class AuthChallenge:
    customer_id: Any
    code: str
    expires_at: datetime
    attempts: int = 0


class AuthService:
    def __init__(self):
        self._challenges: dict[str, AuthChallenge] = {}
        self._code_ttl = timedelta(minutes=5)
        self._max_attempts = 3

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def request_code(self, session: Session, email: str) -> bool:
        if session.authenticated:
            raise ValueError("A sessão já está autenticada.")

        normalized_email = email.strip().casefold()

        if not normalized_email:
            return False

        self._challenges.pop(session.session_id, None)

        customers = load_csv("customers")

        matching_customers = customers[
            customers["email"].astype("string").str.strip().str.casefold()
            == normalized_email
        ]

        if len(matching_customers) != 1:
            return False

        customer_id = matching_customers.iloc[0]["customer_id"]

        code = f"{secrets.randbelow(1_000_000):06d}"

        self._challenges[session.session_id] = AuthChallenge(
            customer_id=customer_id,
            code=code,
            expires_at=self._now() + self._code_ttl,
        )

        print(f"[AUTH] Código de autenticação: {code}")

        return True

    def verify_code(self, session: Session, code: str) -> bool:
        if session.authenticated:
            return True

        challenge = self._challenges.get(session.session_id)

        if challenge is None:
            return False

        if self._now() >= challenge.expires_at:
            del self._challenges[session.session_id]
            return False

        challenge.attempts += 1

        if code.strip() != challenge.code:
            if challenge.attempts >= self._max_attempts:
                del self._challenges[session.session_id]

            return False

        session.authenticated = True
        session.customer_id = challenge.customer_id

        del self._challenges[session.session_id]

        return True
