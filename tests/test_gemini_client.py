from types import SimpleNamespace
from unittest.mock import Mock

from src.integrations import gemini_client


def test_create_gemini_client():
    settings = SimpleNamespace(
        gemini_api_key="test-api-key",
        gemini_model="gemini-3.8-flash",
    )

    mock_client = Mock()
    mock_get_settings = Mock(return_value=settings)
    mock_genai_client = Mock(return_value=mock_client)

    gemini_client.get_settings = mock_get_settings
    gemini_client.genai.Client = mock_genai_client

    client = gemini_client.create_gemini_client()

    assert client is mock_client
    mock_get_settings.assert_called_once()
    mock_genai_client.assert_called_once_with(
        api_key="test-api-key"
    )