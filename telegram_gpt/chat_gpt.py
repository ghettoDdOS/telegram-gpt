"""
App module for wok with OpenAI API
"""

import openai

from telegram_gpt.config import get_openai_request_settings, settings
from telegram_gpt.schemas import OpenAIResponse, OpenAIRole

openai.api_key = settings.OPENAI_API_KEY


def send_chat_gpt_message(text: str) -> OpenAIResponse:
    """
    Send message to ChatGPT

    Args:
        text (str): user message

    Returns:
        OpenAIResponse: response from ChatGPT
    """

    request_config = get_openai_request_settings()

    response = openai.ChatCompletion.create(
        **request_config,
        messages=[
            {
                "role": OpenAIRole.USER,
                "content": text,
            },
        ],
    )

    return OpenAIResponse(**response)
