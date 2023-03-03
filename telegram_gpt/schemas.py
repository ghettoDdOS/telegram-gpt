"""
Application models schemas
"""

from enum import Enum

from pydantic import BaseModel


class OpenAIUsage(BaseModel):
    """
    OpenAI response usage schema
    """

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenAIRole(str, Enum):
    """
    OpenAI available roles
    """

    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"


class OpenAIMessage(BaseModel):
    """
    OpenAI response message schema
    """

    role: OpenAIRole
    content: str


class OpenAIChoice(BaseModel):
    """
    OpenAI response choice schema
    """

    message: OpenAIMessage
    finish_reason: str | None
    index: int


class OpenAIResponse(BaseModel):
    """
    OpenAI response schema
    """

    id: str
    object: str
    created: int
    model: str
    usage: OpenAIUsage
    choices: list[OpenAIChoice]
