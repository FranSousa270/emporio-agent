import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str


def get_settings() -> Settings:
    api_key = os.getenv("GEMINI_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL")

    if not api_key:
        raise ValueError("A variável GEMINI_API_KEY não foi configurada.")

    return Settings(gemini_api_key=api_key, gemini_model=gemini_model)
