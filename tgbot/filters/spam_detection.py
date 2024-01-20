from aiogram import types
from aiogram.filters import Filter

from tgbot.utils.mistral_client import check_spam


class SpamFilter(Filter):
    async def __call__(self, message: types.Message, mistral_client) -> bool | None:
        if message.text:
            is_spam = await check_spam(mistral_client, message.text)
            return is_spam
