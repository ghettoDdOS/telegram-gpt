"""
App module for work with Telegram API
"""

import logging
from functools import wraps

from telegram import Bot, Update
from telegram.constants import ChatAction, MessageEntityType, ParseMode
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from telegram_gpt.chat_gpt import send_chat_gpt_message
from telegram_gpt.config import settings

MAX_MESSAGE_LENGTH = 4095

_logger = logging.getLogger(__name__)


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action
            )
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)


def _chunk_message(msg: str) -> list[str]:
    if len(msg) > MAX_MESSAGE_LENGTH:
        return [
            msg[chunk_size : chunk_size + MAX_MESSAGE_LENGTH]
            for chunk_size in range(0, len(msg), MAX_MESSAGE_LENGTH)
        ]

    return [msg]


@send_typing_action
async def ask_chat_gpt(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Send user message to ChatGPT and return answer"""

    bot: Bot = await ctx.bot.get_me()

    if bot.username not in update.message.text:
        return

    user_message = update.message.text.lstrip(f"@{bot.username}").strip()
    chat_gpt_response = send_chat_gpt_message(user_message)
    chat_gpt_answer = chat_gpt_response.choices[0].message.content

    message = update.message

    for chunk in _chunk_message(chat_gpt_answer):
        message = await message.reply_text(
            chunk,
            parse_mode=ParseMode.MARKDOWN,
        )


def start_bot() -> None:
    """
    Start bot polling
    """

    token = settings.TELEGRAM_BOT_TOKEN
    application = Application.builder().token(token).build()

    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Entity(MessageEntityType.MENTION),
            ask_chat_gpt,
        )
    )

    _logger.info("Starting bot polling")
    application.run_polling()
