from google import genai

from src.core.config import get_settings


def create_gemini_client() -> genai.Client:
    settings = get_settings()

    return genai.Client(
        api_key=settings.gemini_api_key,
    )