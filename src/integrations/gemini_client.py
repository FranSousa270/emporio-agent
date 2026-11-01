from google import genai
from google.genai import types

from src.core.config import get_settings


def create_gemini_client() -> genai.Client:
    settings = get_settings()

    return genai.Client(
        api_key=settings.gemini_api_key,
        http_options=types.HttpOptions(
            timeout=30_000,
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )
